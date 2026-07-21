from cmath import exp
from app import app, db

from controller.base import Base
from model.contrato_opcion import ContratoOpcionModel
from model.StockSymbol import StockSymbol
import common.converter as converter
from common.AppException import AppException
from common.Response import Response
from api.marketdata import MarketDataAPI
from reader.contratoopcion import ContratoOpcionReader
from parser.opcionescontrato import OpcionesContratoParser, SymbolLoaderParser
from domain.fecha import Fecha
from processor.opcion import OpcionProcessor, OpcionLoader
from datetime import date, datetime
import json, os
from sqlalchemy.sql.functions import func

class ContratoOpcionController(Base):
    
    def get_options_chain(self, args={}):
        parser = OpcionesContratoParser()
        params = parser.parse_args_get_options_chain(args=args)

        cod_symbol = params["cod_symbol"]
        fch_expiracion = params["fch_expiracion"]
        imp_ejercicio = params.get("imp_ejercicio")

        calls = ContratoOpcionReader.get_calls(cod_subyacente=cod_symbol, fch_expiracion=fch_expiracion, imp_ejercicio=imp_ejercicio)
        puts = ContratoOpcionReader.get_puts(cod_subyacente=cod_symbol, fch_expiracion=fch_expiracion, imp_ejercicio=imp_ejercicio)

        call_exp_dates = [call.fch_vencimiento for call in calls]
        put_exp_dates = [put.fch_vencimiento for put in puts]

        exp_dates = call_exp_dates + put_exp_dates
        exp_dates = list(set(exp_dates))
        exp_dates.sort()

        call_strikes = [call.imp_strike for call in calls]
        put_strikes = [put.imp_strike for put in puts]

        strikes = call_strikes + put_strikes
        strikes = list(set(strikes))
        strikes.sort()

        data = {
            "calls": calls,
            "puts": puts,
            "exp_dates": exp_dates,
            "strikes": strikes
        }

        """                
        data = {
            "calls": calls,
            "puts": puts,
            "exp_dates": ContratoOpcionReader.get_fechas_expiracion(cod_subyacente=cod_symbol, imp_ejercicio=imp_ejercicio),
            "strikes": ContratoOpcionReader.get_imp_ejercicios(cod_subyacente=cod_symbol, fch_expiracion=fch_expiracion)
        }
        """
                
        return Response().from_raw_data(data)

    def get_calls(self, args={}):
        contract = args["contract"]

        calls = ContratoOpcionReader.get_contratos(sentidos=["call"],
                                                   cod_subyacente=args.get("cod_symbol"),
                                                   fch_expiracion=args.get("expiration_date"),
                                                   imp_ejercicio=args.get("strike")
                                                   )

        """
        if contract != "":
            contract = "%{}%".format(contract)

            query = query.filter(
                ContratoOpcionModel.cod_symbol.ilike(contract)
            )       

            return query.all()
        """

        #query = query.order_by(ContratoOpcionModel.fch_vencimiento, ContratoOpcionModel.imp_strike)

        return calls
    def get_puts(self, args={}):
        #contract = args["contract"]

        puts = ContratoOpcionReader.get_contratos(sentidos=["put"],
                                                   cod_subyacente=args.get("cod_symbol"),
                                                   fch_expiracion=args.get("expiration_date"),
                                                   imp_ejercicio=float(args.get("strike"))
                                                   )

        #query = query.order_by(ContratoOpcionModel.fch_vencimiento, ContratoOpcionModel.imp_strike)

        return puts

    def get_expiration_dates(self, args={}):
        symbol=args["symbol"] #symbol is required
        expiration_date=date.today().isoformat()
        strike=""
        
        query = db.session.query(
            ContratoOpcionModel.fch_vencimiento
        ).distinct(ContratoOpcionModel.fch_vencimiento)

        query = query.filter(               
            ContratoOpcionModel.cod_symbol_subyacente == symbol
        )
        query = query.filter(ContratoOpcionModel.fch_vencimiento >= expiration_date)

        results = query.all()

        exp_list = []
        for row in results:
            exp_list.append(row.expiration_date)

        return exp_list

    def get_strikes(self, symbol="", exp_date=""):                
        query = db.session.query(
            ContratoOpcionModel.imp_strike
        ).distinct(ContratoOpcionModel.imp_strike)

        query = query.filter(            
            ContratoOpcionModel.cod_symbol_subyacente == symbol
        )        

        if exp_date == "":
            query = query.filter(            
                ContratoOpcionModel.fch_vencimiento  >= date.today().isoformat()
            )   
        else:
            query = query.filter(            
                ContratoOpcionModel.fch_vencimiento  == exp_date
            )

        query = query.order_by(ContratoOpcionModel.imp_strike)

        results = query.all()

        strikes = []
        for row in results:
            strikes.append(float(row.strike))
        
        return strikes

    def get_resumen_subyacentes(self, args={}):
        result = db.session.query(
            ContratoOpcionModel.cod_symbol_subyacente,
            func.max(ContratoOpcionModel.fch_registro).label("fch_registro"),
            func.max(ContratoOpcionModel.fch_vencimiento).label("fch_vencimiento")
        ).group_by(
            ContratoOpcionModel.cod_symbol_subyacente
        ).all()        

        return Response().from_raw_data(result)

    def get_contratos(self, args={}):
        parser = OpcionesContratoParser()
        params = parser.parse_args_get_contratos(args=args)

        id_contrato_opcion = params.get("id_contrato_opcion")
        cod_subyacente = params.get("cod_symbol")
        sentidos = params.get("sentidos")
        fch_expiracion = params.get("fch_expiracion")
        imp_ejercicio = params.get("imp_ejercicio")

        results = ContratoOpcionReader.get_contratos(id_contrato_opcion=id_contrato_opcion, cod_subyacente=cod_subyacente, sentidos=sentidos, fch_expiracion=fch_expiracion, imp_ejercicio=imp_ejercicio, limit=200)

        return Response().from_raw_data(results)

    def guardar(self, args={}):
        try:
            opcion = self.__collect_guardar(args)
            OpcionProcessor().guardar(opcion)
            db.session.commit()
            return Response(msg="Se ha guardado correctamente la opcion")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)


    def __collect_guardar(self, args={}):
        opcion = ContratoOpcionModel()

        cod_symbol = args.get("cod_symbol")
        sentido = args.get("sentido")
        cod_subyacente = args.get("cod_subyacente")
        fch_expiracion = args.get("fch_expiracion")
        imp_ejercicio = args.get("imp_ejercicio")
        ctd_tamano_contrato = args.get("ctd_tamano_contrato")
        cod_moneda = args.get("cod_moneda")

        if cod_symbol in [None, ""]:
            raise AppException(msg="No se ha enviado el symbol")

        opcion.cod_symbol = cod_symbol
        
        if sentido.upper() not in ["CALL", "PUT"]:
            raise AppException(msg="el sentido {0} no es valido".format(sentido))

        opcion.tipo_opcion = sentido.upper()

        if cod_subyacente in [None, ""]:
            raise AppException(msg="No se ha enviado el 'cod_subyacente'")
        
        opcion.cod_symbol_subyacente = cod_subyacente

        if fch_expiracion in [None, ""]:
            raise AppException(msg="No se ha enviado 'fch_expiracion'")

        opcion.fch_vencimiento = date.fromisoformat(fch_expiracion)

        if imp_ejercicio in [None, "",0]:
            raise AppException(msg="No se ha enviado 'imp_ejercicio'")

        opcion.imp_strike = float(imp_ejercicio)

        if ctd_tamano_contrato in [None, "", 0]:
            raise AppException(msg="No se ha indicado el tamaño del contrato")

        opcion.tam_contrato = int(ctd_tamano_contrato)

        if cod_moneda in [None, ""]:
            raise AppException(msg="No se ha indicado la moneda")

        opcion.cod_moneda = cod_moneda
        opcion.fch_audit = datetime.now()
        opcion.fch_registro = datetime.now()

        return opcion
    
class SymbolLoader(Base):    

    def get_contratos(self, symbol="",fch_exp=""):                 
        data = iexcloud().get_contracts(symbol, fch_expiracion=fch_exp)        
        return data

    def get_symbol(self, symbol=""):
        sym = db.session.query(
            StockSymbol
        ).filter(
            StockSymbol.symbol == symbol
        ).first()

        if sym is None:
            raise AppException(msg="El symbol {0} no existe en la base de datos".format(symbol))

        return sym         

    def get_contrato(self, symbol=""):
        contrato = ContratoOpcionModel.query.filter(
            ContratoOpcionModel.cod_symbol == symbol
        ).first()

        return contrato

    def load(self, args={}) :
        parser = SymbolLoaderParser()
        params = parser.parse_args_load(args=args)

        # contrato = ContratoOpcionReader.get_contrato(cod_symbol=params.get("cod_symbol"))
        # if contrato

        # contratos = self.get_contratos(symbol, fch_expiracion)

        contratos = MarketData().get_options_chain(cod_subyacente=params.get("cod_symbol"), fch_expiracion=params.get("fch_expiracion"))

        for elem in contratos:
            contrato = ContratoOpcionReader.get_contrato(cod_symbol=params.get("cod_symbol"))
            if contrato is None:
                #adding the details
                oc = ContratoOpcionModel(     
                    #moneda_id = symbolobj.moneda_id,
                    tam_contrato=100,
                    #currency = elem["currency"],
                    #descripcion = elem["description"],
                    fch_vencimiento=datetime.utcfromtimestamp(elem["expiration"]),
                    tipo_opcion=elem["side"].upper(),
                    imp_strike=elem["strike"],
                    cod_symbol=elem["optionSymbol"],
                    cod_symbol_subyacente=elem["underlying"],
                    fch_registro=datetime.now(),
                    fch_audit=datetime.now()
                )
                db.session.add(oc)
                db.session.flush()
        db.session.commit()
        return Response(msg="Se han cargado correctamente los symbol de los contratos para {}".format(params.get("cod_symbol"))).get()

class CsvLoader(Base):
    def __init__(self):
        self.fichero_ruta = None

    def procesar(self, args={}):        
        try:
            tmp_fichero = args.get("files").get("fichero")
            self.__guardar_fichero_temporal(tmp_fichero)
            opcion_loader = self.__collect_procesador(args=args)
            opcion_loader.procesar()
            db.session.commit()
            return Response(msg="Se ha procesado correctamente el fichero con los codigos de opcion")
        except Exception as e:
            db.session.rollback()
            return Response().from_raw_data(e)
        

    def __guardar_fichero_temporal(self, tmp_fichero=None):
        tmp_dir = config.get("rutas","tmp_dir")
        fch_actual_iso = date.today().isoformat()
        fichero_nombre = "tmp_cod_symbol_{0}_{1}.csv".format(self.usuario.id, fch_actual_iso)
        self.fichero_ruta = os.path.join(tmp_dir,fichero_nombre)
        tmp_fichero.save(self.fichero_ruta)

    def __collect_procesador(self, args={}):
        params = args.get("form")        
        opcion_loader = OpcionLoader()
        opcion_loader.fichero = self.fichero_ruta
        cod_moneda = params.get("cod_moneda")
        if cod_moneda in [None, ""]:
            raise AppException(msg="No se ha ingresado la moneda")

        opcion_loader.cod_moneda = cod_moneda

        ctd_multiplicador = params.get("ctd_multiplicador")
        if ctd_multiplicador in [None, "", 0]:
            raise AppException(msg="No se ha ingresado el multiplicador")
        
        opcion_loader.ctd_multiplicador = ctd_multiplicador

        formato_cod_opcion = params.get("formato_cod_opcion")
        if formato_cod_opcion in [None, ""]:
            raise AppException(msg="No se ha ingresado el formato del codigo de la opcion")

        opcion_loader.formato_cod_opcion = formato_cod_opcion

        flg_excluir_errores = params.get("flg_excluir_errores")
        if flg_excluir_errores in [None, ""]:
            raise AppException(msg="No se ha ingresado el indicador para excluir errores")

        opcion_loader.flg_excluir_errores = flg_excluir_errores
        return opcion_loader


