from datetime import datetime, date, timedelta
from model.CalendarioSemanal import CalendarioSemanal as CalendarioSemanalModel
from common.Response import Response
from app import db

class CalendarioSemanalManager:
    INIDATETIME = datetime.fromisoformat("1950-01-01")
    ENDDATETIME = datetime.fromisoformat("2050-12-31")
    def __init__(self):
        pass

    def load(self, args={}):
        try:        
            (startDate, endDate) = self.calc_primera_semana()
            
            while(not self.es_semana_final(startDate,endDate)):
                (startDate, endDate) = self.calc_siguiente_semana(startDate, endDate)
                (year, week, weekday) = startDate.isocalendar()

                new_entry = CalendarioSemanalModel(
                    fch_semana = startDate.date(),
                    anyo = year,
                    semana = week,
                    fch_inicio = startDate.date(),
                    fch_fin = endDate.date()
                )
                db.session.add(new_entry)
            
            db.session.commit()
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