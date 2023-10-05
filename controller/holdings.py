from app import app, db
import requests, json, csv

from model.posicion import PosicionModel
from model.StockData import StockData
from controller.DataManager import DataManager
from sqlalchemy import func

from common.converter import to_dict, to_bool
from common.Response import Response
from common.StatusMessage import StatusMessage
from common.api.iexcloud import iexcloud
from common.AppException import AppException
from common.api.MarketAPI import MarketAPI

from reader.posicion import PosicionReader

from pytz import HOUR, timezone
from datetime import datetime, date
from config.general import APP_DEC_PREC, MARKET_API_LIST
from config.negocio import TIPO_ACTIVO_EQUITY, TIPO_ACTIVO_ETF, TIPO_ACTIVO_OPT

#from controller.StockDataProvider import StockDataProvider
import common.Markets as Markets
from controller.base import Base


class HoldingsManager(Base):
    def __get_active_holdings(self):
        holdings = db.session.query(
            PosicionModel.cod_symbol,            
            PosicionModel.cod_opcion,
            PosicionModel.cod_tipo_activo,
            func.min(PosicionModel.fch_transaccion).label('holding_since'),
            func.sum(PosicionModel.imp_accion).label("sum_imp_accion"),
            func.sum(PosicionModel.imp_posicion).label("sum_imp_operacion"),
            func.sum(PosicionModel.imp_accion_origen).label("sum_imp_accion_origen"),
            func.sum(PosicionModel.ctd_saldo_posicion).label("sum_shares_balance"),
            func.min(PosicionModel.fch_transaccion).label("min_trade_date")
        ).filter(
            PosicionModel.ctd_saldo_posicion != 0
        ).group_by(
            PosicionModel.cod_symbol,
            PosicionModel.cod_opcion
        )\
        .all()

        return holdings




    


    def get_list(self, args={}):                             
        active_holdings = self.__get_active_holdings()

        #shares_balance * current_price
        results = []
        for elem in active_holdings:         
            cod_instrumento = elem.cod_opcion if elem.cod_tipo_activo == TIPO_ACTIVO_OPT else elem.cod_symbol       
            elem_dict = to_dict(elem) 
            elem_dict['cod_instrumento'] = cod_instrumento
            #vals_adic = self.default_bridge.calc_val_adic(elem)
            bridge = iexcloud_bridge()
            vals_adic = bridge.calc_val_adic(elem_dict)
            elem_dict.update(vals_adic)
            results.append(elem_dict)        
        return Response().from_raw_data(results)

    def __options_price(self,holding={},quote=None):
        sum_shares_balance = float(holding["sum_shares_balance"])
        sum_buy_price_per_trade = float(holding["sum_buy_price_per_trade"])
        avg_buy_price = round(sum_buy_price_per_trade/sum_shares_balance,APP_DEC_PREC)
        
        market_value = round((sum_shares_balance * quote.close)*100, APP_DEC_PREC)
        prev_close = quote.open
        daily_change = round(((quote.close - prev_close)/prev_close)*100,APP_DEC_PREC)

        total_change = round(((quote.close - avg_buy_price)/avg_buy_price)*100,APP_DEC_PREC)
        total_pl = round(market_value - sum_buy_price_per_trade,APP_DEC_PREC)

        #holding["sum_trade_buy_price"] = "{0}(x100)".format(holding["sum_trade_buy_price"]) 
        holding["sum_shares_balance"] = "{0}(x100)".format(int(holding["sum_shares_balance"]))
        holding["avg_buy_price"] = "{:.2f}".format(avg_buy_price)
        holding["daily_change"] = "{:.2f}".format(daily_change)
        holding["total_change"] = "{:.2f}".format(total_change)
        holding["total_pl"] = "{:.2f}".format(total_pl)
        holding["last_price_date"] = quote.price_date            
        holding["last_price"] = "{:.2f}".format(quote.close)
        holding["market_value"] = "{:.2f}".format(market_value)

        return holding

    def __stocks_price(self, holding={}, quote=None):
        sum_shares_balance = holding["sum_shares_balance"]
        sum_buy_price_per_trade = holding["sum_buy_price_per_trade"]
        avg_buy_price = round(sum_buy_price_per_trade/sum_shares_balance,APP_DEC_PREC)
        
        market_value = round(sum_shares_balance * quote.close, APP_DEC_PREC)
        prev_close = quote.prev_close
        daily_change = round(((quote.close - prev_close)/prev_close)*100,APP_DEC_PREC)

        total_change = round(((quote.close - avg_buy_price)/avg_buy_price)*100,APP_DEC_PREC)
        total_pl = round(market_value - sum_buy_price_per_trade,APP_DEC_PREC)

        holding["avg_buy_price"] = avg_buy_price
        holding["daily_change"] = daily_change
        holding["total_change"] = total_change
        holding["total_pl"] = total_pl
        holding["last_price_date"] = quote.price_date            
        holding["last_price"] = quote.close
        holding["market_value"] = market_value

        return holding

class ResumenController(Base):
    def __init__(self):
        pass

 
class iexcloud_bridge:
    def __init__(self):
        #self.apiobj = MarketAPI().get_api()
        self.api = iexcloud()
        self.opciones = {}

    def calc_val_adic(self, holding=None):        
        vals = {}
        cod_tipo_activo = holding.get('cod_tipo_activo')

        if cod_tipo_activo in [TIPO_ACTIVO_EQUITY,TIPO_ACTIVO_ETF]:
            vals = self.__calc_val_equity(holding)
        if cod_tipo_activo == TIPO_ACTIVO_OPT:
            vals = self.__calc_val_opciones(holding)

        return vals

    def __calc_val_opciones(self, holding=None):
        cotizacion = self.__get_cotizacion_opcion(holding.get('cod_opcion'))
        
        if cotizacion is None:
            return          
        else:
            imp_apertura, imp_cierre, fch_cierre = cotizacion  

        sum_shares_balance = float(holding["sum_shares_balance"])
        sum_imp_operacion = float(holding["sum_imp_operacion"])            
        avg_buy_price = round(sum_imp_operacion/sum_shares_balance,APP_DEC_PREC)        
        market_value = round(sum_shares_balance * imp_cierre, APP_DEC_PREC)        
        daily_change = round(((imp_cierre - imp_apertura)/imp_apertura)*100,APP_DEC_PREC)
        total_change = round(((imp_cierre - avg_buy_price)/avg_buy_price)*100,APP_DEC_PREC)
        total_pl = round(market_value - sum_imp_operacion,APP_DEC_PREC)

        campos_calculados = {
            "avg_buy_price" : avg_buy_price,
            "daily_change" : daily_change,
            "total_change":total_change,
            "total_pl":total_pl,
            "last_price_date": fch_cierre,
            "last_price":imp_cierre,
            "market_value":market_value
        }

        return campos_calculados


    def __get_cotizacion_opcion(self, cod_opcion):        
        opciones_api = self.api.get_option_eod_data(cod_opcion)
        for elem in opciones_api:
            cod_opcion_api = elem.get('id')
            if cod_opcion_api not in self.opciones:
                self.opciones[cod_opcion_api] = (elem.get('open'), elem.get('close'), elem.get('lastTradeDate'))
        
        if cod_opcion not in self.opciones:
            return None
        else:
            return self.opciones[cod_opcion]

    def __calc_val_equity(self, holding=None):        
        imp_open, imp_close,prev_close, close_date = self.get_quote(holding.get('cod_instrumento').upper())

        sum_shares_balance = float(holding["sum_shares_balance"])
        sum_imp_operacion = float(holding["sum_imp_operacion"])            
        avg_buy_price = round(sum_imp_operacion/sum_shares_balance,APP_DEC_PREC)        
        market_value = round(sum_shares_balance * imp_close, APP_DEC_PREC)        
        daily_change = round(((imp_close - prev_close)/prev_close)*100,APP_DEC_PREC)
        total_change = round(((imp_close - avg_buy_price)/avg_buy_price)*100,APP_DEC_PREC)
        total_pl = round(market_value - sum_imp_operacion,APP_DEC_PREC)
        
        vals = {
            "avg_buy_price" : avg_buy_price,
            "daily_change" : daily_change,
            "total_change":total_change,
            "total_pl":total_pl,
            "last_price_date": close_date,
            "last_price":imp_close,
            "market_value":market_value
        }

        return vals

    def get_quote(self, symbol=""):
        args = {
            "symbol":symbol
        }

        print(datetime.now())
        quote = self.api.get_quote(args)
        print(datetime.now())

        imp_open = quote.get("open")
        if imp_open is None:
            imp_open = quote.get("iexOpen")

        imp_close = quote.get("close")        
        if imp_close is None:
            imp_close = quote.get("iexRealtimePrice")
        
        imp_prev_close = quote.get("previousClose")

        close_date = quote.get("closeTime")
        if close_date is None:
            close_date = quote.get("latestUpdate")

        return (imp_open, imp_close,imp_prev_close, close_date)

class PosicionAccionesReporter(Base):
    def __init__(self):
        self.api = iexcloud()

    def get_posiciones(self, args={}):
        posiciones = PosicionReader.get_pos_abiertas_agrup_x_accion(self.usuario.id)
        return Response().from_raw_data(posiciones)

class PosicionOpcionReporter(Base):

    def __init__(self):
        self.cotizaciones_api = {}
        self.api = iexcloud()
        self.records = []
        self.expiraciones = []

    def get_posiciones_opcion(self, args={}):        
        cod_subyacente = args.get('cod_subyacente')
        cod_opcion = args.get('cod_opcion')
        anyo_expiracion = args.get('anyo_expiracion')
        mes_expiracion = args.get('mes_expiracion')
        dia_expiracion = args.get('dia_expiracion')
        flg_call = to_bool(args.get('flg_call'))
        flg_put = to_bool(args.get('flg_put'))

        cod_subyacente = None if cod_subyacente in ["",None] else cod_subyacente
        cod_opcion = None if cod_opcion in ["",None] else cod_opcion
        anyo_expiracion = None if anyo_expiracion in ["",None] else anyo_expiracion
        mes_expiracion = None if mes_expiracion in ["", None] else mes_expiracion
        dia_expiracion = None if dia_expiracion in ["", None] else dia_expiracion

        posiciones = PosicionReader.get_pos_abiertas_agrup_x_opcion(self.usuario.id, cod_subyacente=cod_subyacente, cod_opcion=cod_opcion
        , anyo_expiracion=anyo_expiracion, mes_expiracion=mes_expiracion, dia_expiracion=dia_expiracion, flg_call=flg_call, flg_put=flg_put)
        for record in posiciones:
            self.__calc_valores_adicionales(record)

        return Response().from_raw_data(self.records)

    def __calc_valores_adicionales(self, record):
        elem = to_dict(record)
        cod_opcion = record.cod_opcion

        #cotizacion = self.__get_cotizacion(cod_opcion)                
        cotizacion = None
        
        sentido = 'call' if cod_opcion[-9:-8] == 'C'else 'put'        
        elem["cod_subyacente"] = cod_opcion[:-17]        
        elem["fch_expiracion"] = cod_opcion[-17:-9]
        elem["imp_ejercicio"] = float(cod_opcion[-6:])/1000
        elem["cod_tipo_opcion"] = cod_opcion[-9:-8]

        if cotizacion is None:            
            #elem["imp_valor_subyacente"] = 0
            elem["imp_valor_posicion"] = 0
            elem["imp_ganancia_perdida"] = 0
        else:
            imp_apertura, imp_cierre, fch_cierre = cotizacion
            #elem["imp_valor_subyacente"] = imp_cierre
            elem["imp_valor_posicion"] = float(record.ctd_saldo_posicion) * imp_cierre
            elem["imp_ganancia_perdida"] = float(record.imp_posicion_incial) - elem.get('imp_valor_posicion')
        
        self.records.append(elem)

    def __get_cotizacion(self, cod_opcion):   
        cod_subyacente, fch_expiracion_yyyymmdd = self.__descomponer_cod_opcion(cod_opcion)          

        if cod_opcion in self.cotizaciones_api:
            return self.cotizaciones_api[cod_opcion]

        fch_expiracion = datetime.strptime(fch_expiracion_yyyymmdd,"%Y%m%d").date()
        fch_actual = date.today()

        if fch_actual > fch_expiracion:
            return None
        
        records = self.__get_expiraciones_subyacente(cod_opcion=cod_opcion)

        for row in records:
            cod_opcion_api = row.get('id')
            if cod_opcion_api not in self.cotizaciones_api:
                self.cotizaciones_api[cod_opcion_api] = (row.get('open'), row.get('close'), row.get('lastTradeDate'))
        
        if cod_opcion in self.cotizaciones_api:
            return self.cotizaciones_api[cod_opcion]
        else:
            return None

    def __get_expiraciones_subyacente(self, cod_opcion):
        records = []
        cod_sub_expiracion = cod_opcion[:-9]

        if cod_sub_expiracion not in self.expiraciones:
            records = self.api.get_option_eod_data(cod_opcion)
            self.expiraciones.append(cod_sub_expiracion)

        return records

    def __descomponer_cod_opcion(self, cod_opcion):
        cod_subyacente = cod_opcion[:-17]
        fch_expiracion = cod_opcion[-17:-9]        
        return (cod_subyacente, fch_expiracion)