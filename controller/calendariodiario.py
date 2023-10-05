from app import db
from controller.base import Base
from common.Response import Response
from datetime import datetime, date, timedelta
from model.calendariodiario import CalendarioDiarioModel

from reader.calendariodiario import CalendarioDiarioReader

class CalendarioDiarioLoader(Base):
    INIDATETIME = datetime.fromisoformat("1950-01-01")
    ENDDATETIME = datetime.fromisoformat("2050-12-31")

    def procesar(self, args={}):
        try:
            current_date = self.INIDATETIME

            while(self.ENDDATETIME >= current_date):
                self.__add_nueva_fecha(current_date)                
                current_date = self.__get_sig_fecha(current_date)
            
            db.session.commit()
            return Response(msg="Se ha cargado correctamente el calendario diario")            
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def __add_nueva_fecha(self, fecha:date):
        (num_anyo_semana, num_semana, num_dia_semana) = fecha.isocalendar()
        fch_semana = date.fromisocalendar(num_anyo_semana, num_semana, 1)
        cod_semana = "{0}{1}".format(num_anyo_semana, str(num_semana).zfill(2))

        flg_fin_semana = 'N'
        if num_dia_semana in [6,7]:
            flg_fin_semana = 'S'

        nu = CalendarioDiarioModel(
            fch_dia=fecha,
            anyo=fecha.year,
            mes=fecha.month,
            dia=fecha.day,
            cod_semana = cod_semana,
            fch_semana = fch_semana,
            num_anyo_semana= num_anyo_semana,  
            num_semana = num_semana,        
            num_dia_semana= num_dia_semana,
            flg_fin_semana = flg_fin_semana
        )
        db.session.add(nu)

    def __get_sig_fecha(self, fecha:date):
        delta = timedelta(days=1)
        nu_fecha = fecha + delta
        return nu_fecha

class CalendarioDiarioManager(Base):
    
    def get_datos_fecha(self, args={}):
        fch_dia = args.get("fch_dia")
        calendario = CalendarioDiarioReader.get(fch_dia)
        return Response().from_raw_data(calendario)