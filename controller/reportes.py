from app import db
from common.AppException import AppException
from common.Formatter import Formatter
from common.Response import Response

from model.StockData import StockData as StockDataModel
from model.variacionsemanal import VariacionSemanalModel
from model.variacionmensual import VariacionMensualModel
from model.variaciondiaria import VariacionDiariaModel
from model.CalendarioSemanal import CalendarioSemanalModel
from model.calendariodiario import CalendarioDiarioModel

from model.seriediaria import SerieDiariaModel

from reader.calendariosemanal import CalendarioSemanalReader
from reader.seriediaria import SerieDiariaReader
from reader.calendariodiario import CalendarioDiarioReader

from sqlalchemy.sql import extract
from sqlalchemy.orm import outerjoin
from sqlalchemy import and_

from controller.base import Base

class VariacionSemanalBuilder(Base):

    def build(self, args={}):        

        symbol = args.get("symbol")

        if symbol is None or symbol =="":
            raise AppException(msg="No se ha ingresado el 'symbol'")

        stmt = db.select(
            VariacionSemanalModel
        ).filter(
            VariacionSemanalModel.symbol == symbol
        ).order_by(
            VariacionSemanalModel.fecha.desc()
        )

        records = db.session.execute(stmt).scalars().all()
        return Response().from_raw_data(records)

class VariacionMensualBuilder(Base):

    def build(self, args={}):

        symbol = args.get('symbol')

        if symbol is None or symbol == "":
            raise AppException(msg="No se ha ingresado el 'symbol'")

        stmt = db.select(
            VariacionMensualModel
        ).where(
            VariacionMensualModel.symbol == symbol
        ).order_by(
            VariacionMensualModel.fch_ini_mes.desc()
        )

        result = db.session.execute(stmt)
        records = result.scalars().all()
        return Response().from_raw_data(records)

class VariacionDiariaBuilder(Base):

    def build(self, args={}):

        symbol = args.get('symbol')        

        if symbol is None or symbol == "":
            raise AppException(msg="No se ha ingresado el 'symbol")

        stmt = db.select(
            extract("year",VariacionDiariaModel.fch_serie).label("anyo"),
            VariacionDiariaModel.symbol,
            VariacionDiariaModel.fch_serie,
            VariacionDiariaModel.imp_cierre_ant,
            VariacionDiariaModel.imp_apertura,
            VariacionDiariaModel.imp_maximo,
            VariacionDiariaModel.imp_minimo,
            VariacionDiariaModel.imp_cierre,
            VariacionDiariaModel.pct_variacion_apertura,
            VariacionDiariaModel.imp_variacion_apertura,
            VariacionDiariaModel.pct_variacion_cierre,
            VariacionDiariaModel.imp_variacion_cierre,
            VariacionDiariaModel.pct_variacion_maximo,
            VariacionDiariaModel.imp_variacion_maximo,
            VariacionDiariaModel.pct_variacion_minimo,
            VariacionDiariaModel.imp_variacion_minimo
        ).where(
            VariacionDiariaModel.symbol == symbol
        ).order_by(
            VariacionDiariaModel.fch_serie.desc()
        )

        result = db.session.execute(stmt)
        records = result.all()
        return Response().from_raw_data(records)

class VariacionSemanalEvolucion(Base):

    def build(self, args={}):

        symbol = args.get('symbol')
        anyo = args.get('anyo')
        semana = args.get('semana')

        if symbol is None or symbol == "":
            raise AppException(msg="No se ha ingresado el 'symbol'")

        if anyo is None or symbol == "":
            raise AppException(msg="No se ha ingresado el 'año'")

        if semana is None or semana == "":
            raise AppException(msg="No se ha ingresado la 'semana'")

        calendario = CalendarioSemanalReader.get_por_num_semana(anyo, semana)
        #calendario = CalendarioDiarioReader.get_fechas_x_semana(anyo, semana)

        stmt = db.select(
            SerieDiariaModel.symbol,
            CalendarioDiarioModel.fch_dia.label('fch_serie'),
            SerieDiariaModel.imp_apertura,
            SerieDiariaModel.imp_maximo,
            SerieDiariaModel.imp_minimo,
            SerieDiariaModel.imp_cierre
        ).select_from(
            CalendarioDiarioModel
        ).outerjoin(
            SerieDiariaModel,
            and_(
                CalendarioDiarioModel.fch_dia == SerieDiariaModel.fch_serie,
                SerieDiariaModel.symbol == symbol
            )
        ).where(            
            CalendarioDiarioModel.flg_fin_semana == 'N',
            CalendarioDiarioModel.num_anyo_semana == anyo,
            CalendarioDiarioModel.num_semana == semana
        )

        result = db.session.execute(stmt)
        records = result.all()
        return Response().from_raw_data(records)

class EvolucionSemanalSeries(Base):
    def __init__(self):        
        self.row_template = {}
        self.semana = None
        self.series = []
        self.filas = []
        

    def build(self, args={}):

        symbol = args.get('symbol')
        anyo = args.get('anyo')
        semana = args.get('semana')

        if symbol is None or symbol == "":
            raise AppException(msg="No se ha ingresado el 'symbol'")

        if anyo is None or symbol == "":
            raise AppException(msg="No se ha ingresado el 'año'")

        if semana is None or semana == "":
            raise AppException(msg="No se ha ingresado la 'semana'")

        self.semana = CalendarioSemanalReader.get_por_num_semana(anyo, semana)
        #fechas = Formatter().format(self.semana)

        self.series = self.__get_series_semana(symbol, self.semana)
        self.__crear_filas(symbol)

        response = {
            "semana":self.semana,
            "series":self.filas
        }

        return Response().from_raw_data(response)
    
    def __get_series_semana(self, symbol, semana:CalendarioSemanalModel):
        return SerieDiariaReader.get_series_entre_fechas(symbol, semana.fch_inicio, semana.fch_fin)
    
    def __crear_filas(self, symbol):
        filas = []
        for valor in ["apertura","maximo","minimo","cierre"]:
            row = {
                "valor":valor,
                "symbol":symbol,
                "imp_lunes":0,            
                "imp_martes":0,
                "imp_miercoles":0,
                "imp_jueves":0,
                "imp_viernes":0, 
                "dia_max":None,
                "dia_min":None
            } 
            self.__completar_campos(row)
            self.filas.append(row)            
    
    def __completar_campos(self, pre_fila):                

        valor = pre_fila.get('valor')
        dia_max = None
        dia_min = None

        for serie in self.series:
            imp_lunes = self.__get_importe_x_fecha(valor, serie, self.semana.fch_lunes)  
            imp_martes = self.__get_importe_x_fecha(valor, serie, self.semana.fch_martes)      
            imp_miercoles = self.__get_importe_x_fecha(valor, serie, self.semana.fch_miercoles)    
            imp_jueves = self.__get_importe_x_fecha(valor, serie, self.semana.fch_jueves)    
            imp_viernes = self.__get_importe_x_fecha(valor, serie, self.semana.fch_viernes)    

            if imp_lunes is not None:
                pre_fila["imp_lunes"] = imp_lunes    

            if imp_martes is not None:
                pre_fila["imp_martes"] = imp_martes

            if imp_miercoles is not None:
                pre_fila["imp_miercoles"] = imp_miercoles

            if imp_jueves is not None:
                pre_fila["imp_jueves"] = imp_jueves

            if imp_viernes is not None:
                pre_fila["imp_viernes"] = imp_viernes

            if serie.maxrow == 1 and dia_max is None:
                dia_max = serie.fch_serie.weekday() + 1
            
            if serie.minrow == 1 and dia_min is None:
                dia_min = serie.fch_serie.weekday() + 1

        if pre_fila.get("valor") == 'maximo':
            pre_fila["dia_max"] = dia_max
        
        if pre_fila.get("valor") == 'minimo':
            pre_fila["dia_min"] = dia_min
         
    def __get_importe_x_fecha(self, valor, serie:SerieDiariaModel, fecha):
        importe = None

        if serie.fch_serie == fecha:                        
            importe = float(getattr(serie, 'imp_'+valor))
        
        return importe

    





        
