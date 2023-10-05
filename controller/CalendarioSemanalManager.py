from datetime import datetime, date, timedelta
from model.CalendarioSemanal import CalendarioSemanalModel
from common.Response import Response
from app import db
from controller.base import Base

class CalendarioSemanalManager(Base):
    INIDATETIME = datetime.fromisoformat("1950-01-01")
    ENDDATETIME = datetime.fromisoformat("2050-12-31")    

    def load(self, args={}):
        try:        
            (startDate, endDate) = self.calc_primera_semana()
            
            self.__eliminar()
            while(not self.es_semana_final(startDate,endDate)):
                (startDate, endDate) = self.calc_siguiente_semana(startDate, endDate)
                (year, week, weekday) = startDate.isocalendar()
                fch_lunes = date.fromisocalendar(year, week, 1)
                fch_martes = date.fromisocalendar(year, week, 2)
                fch_miercoles = date.fromisocalendar(year, week, 3)
                fch_jueves = date.fromisocalendar(year, week, 4)
                fch_viernes = date.fromisocalendar(year, week, 5)

                new_entry = CalendarioSemanalModel(
                    fch_semana = startDate.date(),
                    anyo = year,
                    semana = week,
                    fch_inicio = startDate.date(),
                    fch_fin = endDate.date(),
                    fch_lunes = fch_lunes,
                    fch_martes = fch_martes,
                    fch_miercoles = fch_miercoles,
                    fch_jueves = fch_jueves,
                    fch_viernes = fch_viernes
                )
                db.session.add(new_entry)
            
            db.session.commit()
            return Response(msg="Se ha cargado correctamente el calendario semanal")
        except Exception as e:
            db.session.rollback()
            return Response().from_exception(e)

    def es_semana_final(self, startDate, endDate):
        if self.ENDDATETIME >= startDate and self.ENDDATETIME <= endDate:
            return True
        else:
            return False    

    def calc_primera_semana(self):
        delta_to_ini = timedelta(days = self.INIDATETIME.isoweekday() - 1)
        startDate = self.INIDATETIME - delta_to_ini
        endDate = startDate + timedelta(days=6)
        return (startDate, endDate)

    def calc_siguiente_semana(self, prevStartDate, prevEndDate):
        startDate = prevEndDate + timedelta(days=1)
        endDate = startDate + timedelta(days=6)
        return (startDate, endDate)

    def __eliminar(self):
        stmt = db.delete(
            CalendarioSemanalModel
        )

        result = db.session.execute(stmt)
    