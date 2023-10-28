from re import S
from app import app, db

from common.AppException import AppException
from common.Formatter import Formatter
from common.Response import Response
from common.Error import Error

from domain.semana import CodigoSemana

#from model.StockTrade import StockTrade
from model.StockSymbol import StockSymbol
from model.orden import OrdenModel
from model.transaccion import TransaccionModel
from model.TipoModel import TipoModel

from reader.transaccion import TransaccionReader
from reader.calendariodiario import CalendarioDiarioReader
from reader.operacion import OperacionReader

from parser.operacion import OperacionParser

from datetime import datetime, date, time, timedelta
from sqlalchemy import desc
from sqlalchemy.orm import join
import sqlalchemy.sql.functions as func
from sqlalchemy.sql import extract
from controller.base import Base


class OperacionManager(Base):        
    def __init__(self):
        pass

    def _get_handler(self, asset_type="equity"):
        return self.handlers[asset_type]

    def get_operaciones(self, args={}):        
        args = OperacionParser.get_operaciones(args=args)
        id_cuenta = args.get("id_cuenta")
        orden_resultados = args.get("orden_resultados")
        id_symbol = args.get("id_symbol")
        flg_opciones = args.get("flg_opciones")
        id_contrato_opcion = args.get("id_contrato_opcion")
        records = OperacionReader.get_operaciones(id_cuenta, id_symbol=id_symbol, flg_opciones=flg_opciones, id_contrato_opcion=id_contrato_opcion, orden_resultados=orden_resultados)
        return Response().from_raw_data(records)

    def get_rentabilidad_diaria(self, args={}):        
        args = OperacionParser.parse_args_get_rentabilidad_diaria(args=args)         
        id_cuenta = args.get("id_cuenta")
        fch_desde = args.get("fch_desde")
        fch_hasta = args.get("fch_hasta")
        records = TransaccionReader.get_rentabilidad_diaria(id_cuenta, fch_desde, fch_hasta)
        return Response().from_raw_data(records)   

    def get_rentabilidad_mensual(self, args={}):
        args = OperacionParser.parse_args_get_rentabilidad_mensual(args=args)
        id_cuenta = args.get("id_cuenta")
        cod_mes_desde = args.get("cod_mes_desde")
        cod_mes_hasta = args.get("cod_mes_hasta")
        flg_ascendente = args.get("flg_ascendente")
        records = TransaccionReader.get_rentabilidad_mensual(id_cuenta=id_cuenta,cod_mes_desde=cod_mes_desde, cod_mes_hasta=cod_mes_hasta, flg_ascendente=flg_ascendente )
        
        records_output = []
        for elemento in records:
            desc_mes_transaccion = "{0}/{1}".format(str(elemento.cod_mes_transaccion)[:4], str(elemento.cod_mes_transaccion)[-2:])            
            elemento = Formatter().format(elemento)
            elemento["desc_mes_transaccion"] = desc_mes_transaccion
            records_output.append(elemento)            

        return Response().from_raw_data(records_output)
    
    def get_rentabilidad_anual(self, args={}):
        args = OperacionParser.parse_args_get_rentabilidad_anual(args=args)
        id_cuenta = args.get("id_cuenta")
        anyo_desde = args.get("num_anyo_desde")
        anyo_hasta = args.get("num_anyo_hasta")
        orden_resultado = args.get("orden_resultado")
        records = TransaccionReader.get_rentabilidad_anual(id_cuenta=id_cuenta, anyo_desde=anyo_desde, anyo_hasta=anyo_hasta , orden=orden_resultado)
        return Response().from_raw_data(records)

    def get_rentabilidad_semanal(self, args={}):
        args = OperacionParser.parse_args_get_rentabilidad_semanal(args=args)
        id_cuenta = args.get("id_cuenta")
        cod_semana_desde = args.get("cod_semana_desde")
        cod_semana_hasta = args.get("cod_semana_hasta")
        flg_ascendente = args.get("flg_ascendente")
        records = TransaccionReader.get_rentabilidad_semanal(id_cuenta=id_cuenta, cod_semana_desde=cod_semana_desde, cod_semana_hasta=cod_semana_hasta, flg_ascendente=flg_ascendente)

        output = []
        for element in records:
            desc_semana_transaccion = CodigoSemana(element.cod_semana_transaccion).format()
            element = Formatter().format(element)
            element["desc_semana_transaccion"] = desc_semana_transaccion
            output.append(element)

        return Response().from_raw_data(output)            

    def get_rentabilidad_ult30dias(self, args={}): 
        id_cuenta = args.get("id_cuenta")               
        fechas = {}
        rows = []

        d = timedelta(days=30)
        fch_actual = date.today()    
        fch_desde = fch_actual - d        
        
        records = TransaccionReader.get_rentabilidad_dias_calendarios(id_cuenta, fch_desde=fch_desde, fch_hasta=fch_actual)

        for elem in records:
            rows.append({
                "fch_transaccion":elem.fch_transaccion,
                "imp_rentabilidad": 0 if elem.imp_rentabilidad is None else elem.imp_rentabilidad
            })

        return Response().from_raw_data(rows)

    def get_rentabilidades_x_periodo(self, args={}):
        records = []
        id_cuenta = args.get("id_cuenta")        

        #rentabilidad ultimo dia
        rent_ultdia = TransaccionReader.get_rentabilidad_ultdia(id_cuenta=id_cuenta)

        if rent_ultdia is not None:
            records.append({
                "periodo":"Dia - {0}".format(rent_ultdia.fch_transaccion.strftime("%d/%m/%Y")),
                "imp_rentabilidad": rent_ultdia.imp_rentabilidad
            })
        else:
            records.append({
                "periodo":"Dia - {0}".format("00/00/0000"),
                "imp_rentabilidad": 0
            })

        #rentabilidad ultima semana
        anyo, semana, imp_rentabilidad = TransaccionReader.get_rentabilidad_ultsemana(id_cuenta=id_cuenta)
        records.append({
            "periodo": "Semana - {0}/{1}".format(anyo, semana),
            "imp_rentabilidad": imp_rentabilidad
        })

        #rentabilidad ultimo mes
        anyo, mes, imp_rentabilidad = TransaccionReader.get_rentabilidad_ultmes(id_cuenta=id_cuenta)
        records.append({
            "periodo": "Mes - {0}/{1}".format(anyo, mes),
            "imp_rentabilidad": imp_rentabilidad
        })

        #rentabilidad ultimo anyo
        anyo, imp_rentabilidad = TransaccionReader.get_rentabilidad_ultanyo(id_cuenta=id_cuenta)
        records.append({
            "periodo": "Año - {0}".format(anyo),
            "imp_rentabilidad": imp_rentabilidad
        })

        return Response().from_raw_data(records)

class EliminadorEntryPoint:
    def __init__(self):
        pass

    def procesar(self, args={}):
        try:
            self._validar(args)
            opers = self._collect(args)
            eliminador = Eliminador()
            eliminador.procesar(opers)
            db.session.commit()
            return Response(msg="Las Operaciones se han eliminado correctamente").get()
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def _validar(self, args={}):
        errors = []
        if "del_opers" not in args:
            errors.append("El parámetro 'del_opers' no ha sido enviado")
        
        if len(errors) > 0:
            raise AppException(msg="Se han encontrado errores de validación",errors=errors)

    def _collect(self, args={}):
        return args["del_opers"]    
        

class BuscadorOperaciones:
    def __init__(self):
        pass

    def obt_historial_oper(self, args={}):
        try:
            query = db.session.query(
                StockTrade.id,
                StockTrade.num_operacion,
                StockTrade.order_id,
                StockTrade.num_orden,
                StockTrade.asset_type,
                StockTrade.symbol,
                StockTrade.trade_type,
                TipoModel.tipo_nombre.label("tipo_oper_nombre"),
                StockTrade.cantidad,
                StockTrade.saldo,
                StockTrade.trade_date,
                StockTrade.trade_month,
                StockTrade.imp_accion,
                StockTrade.imp_operacion,
                StockTrade.imp_accion_origen,
                StockTrade.realized_gl                
            ).outerjoin(TipoModel, StockTrade.trade_type == TipoModel.tipo_id)
            query = query.order_by(StockTrade.trade_date.desc(),StockTrade.symbol.asc(),StockTrade.num_operacion.desc())
            data = query.all()
            return Response(raw_data=data).get()
        except Exception as e:
            return Response().from_exception(e)




