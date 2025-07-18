from app import app, db
from common.AppException import AppException
from common.Response import Response
from model.resumenserie import ResumenSerieModel
from controller.base import Base
from collections import namedtuple
from domain.semana import Semana
from domain.mes import Mes
import utils.calendario as calendario
from common.Formatter import Formatter
from datetime import date

CONST_EST_CORRECTO = "Correcto"
CONST_EST_DEFECTUOSO = "Defectuoso"
CONST_EST_ACTUALIZADO = "Actualizado"
CONST_EST_DESACTUALIZADO = "Desactualizado"

Integridad = namedtuple(
    "Integridad",
    [
        "est_general",
        "est_serie_diaria",
        "est_var_diaria",
        "est_serie_semanal",
        "est_var_semanal",
        "est_serie_mensual",
        "est_var_mensual",
        "num_dias_desde_ult_serie",
    ],
)


class ResumenSerie(Base):
    def get_resumen_serie(self, args=None):
        try:
            formatted_records = []
            records = ResumenSerieModel.get_all()

            for resumen_serie in records:
                integridad = self.eval_integridad(resumen_serie)._asdict()
                resumen_serie_result = Formatter().format(resumen_serie)
                resumen_serie_result.update(integridad)
                formatted_records.append(resumen_serie_result)

            resp = Response().from_raw_data(formatted_records)
            return resp
        except Exception as ex:
            return Response().from_exception(ex)

    def eval_integridad(self, record: ResumenSerieModel):

        est_serie_diaria = self.eval_serie_diaria(record)
        est_var_diaria = self.eval_var_diaria(record)
        est_serie_semanal = self.eval_serie_semanal(record)
        est_var_semanal = self.eval_var_semanal(record)
        est_serie_mensual = self.eval_serie_mensual(record)
        est_var_mensual = self.eval_var_mensual(record)

        evals = [
            est_serie_diaria,
            est_var_diaria,
            est_serie_semanal,
            est_var_semanal,
            est_serie_mensual,
            est_var_mensual,
        ]

        res_integridad = Integridad(
            est_general=self.eval_estado_general(evals, record),
            est_serie_diaria=est_serie_diaria,
            est_var_diaria=est_var_diaria,
            est_serie_semanal=est_serie_semanal,
            est_var_semanal=est_var_semanal,
            est_serie_mensual=est_serie_mensual,
            est_var_mensual=est_var_mensual,
            num_dias_desde_ult_serie=(
                calendario.get_ultimo_dia_util() - record.fch_ultima_serie_diaria
            ).days,
        )
        return res_integridad

    def eval_estado_general(self, evals, resumen_serie: ResumenSerieModel):
        if CONST_EST_DEFECTUOSO in evals:
            return CONST_EST_DEFECTUOSO

        if calendario.get_ultimo_dia_util() > resumen_serie.fch_ultima_serie_diaria:
            return CONST_EST_DEFECTUOSO
        else:
            return CONST_EST_ACTUALIZADO

        return CONST_EST_CORRECTO

    def eval_serie_diaria(self, record: ResumenSerieModel):
        fch_hoy = date.today()
        if (
            record.fch_primera_serie_diaria == record.fch_ultima_serie_diaria
            and record.num_series_diarias > 1
        ):
            return CONST_EST_DEFECTUOSO
        elif calendario.get_ultimo_dia_util() > record.fch_ultima_serie_diaria:
            return CONST_EST_DESACTUALIZADO
        else:
            return CONST_EST_CORRECTO

    def eval_var_diaria(self, record: ResumenSerieModel):

        if record.num_series_diarias != record.num_var_diarias:
            return CONST_EST_DEFECTUOSO

        if record.fch_primera_serie_diaria != record.fch_primera_var_diaria:
            return CONST_EST_DEFECTUOSO

        return CONST_EST_CORRECTO

    def eval_serie_semanal(self, record: ResumenSerieModel):

        sem_primera_serie_diaria = Semana.from_fecha(record.fch_primera_serie_diaria)
        sem_primera_serie_semanal = Semana.from_fecha(record.fch_primera_serie_semanal)

        if sem_primera_serie_diaria != sem_primera_serie_semanal:
            return CONST_EST_DEFECTUOSO

        sem_ultima_serie_diaria = Semana.from_fecha(record.fch_ultima_serie_diaria)
        sem_ultima_serie_semanal = Semana.from_fecha(record.fch_ultima_serie_semanal)

        if sem_ultima_serie_diaria != sem_ultima_serie_semanal:
            return CONST_EST_DEFECTUOSO

        return CONST_EST_CORRECTO

    def eval_var_semanal(self, record: ResumenSerieModel):

        sem_primera_serie_diaria = Semana.from_fecha(record.fch_primera_serie_diaria)
        sem_primera_var_semanal = Semana.from_fecha(record.fch_primera_var_semanal)

        if sem_primera_serie_diaria != sem_primera_var_semanal:
            return CONST_EST_DEFECTUOSO

        sem_ultima_serie_diaria = Semana.from_fecha(record.fch_ultima_serie_diaria)
        sem_ultima_serie_semanal = Semana.from_fecha(record.fch_ultima_var_semanal)

        if sem_ultima_serie_diaria != sem_ultima_serie_semanal:
            return CONST_EST_DEFECTUOSO

        return CONST_EST_CORRECTO

    def eval_serie_mensual(self, record: ResumenSerieModel):

        mes_primera_serie_diaria = Mes.from_fecha(record.fch_primera_serie_diaria)
        mes_primera_serie_mensual = Mes.from_fecha(record.fch_primera_serie_mensual)

        if mes_primera_serie_diaria != mes_primera_serie_mensual:
            return CONST_EST_DEFECTUOSO

        mes_ultima_serie_diaria = Mes.from_fecha(record.fch_ultima_serie_diaria)
        mes_ultima_serie_mensual = Mes.from_fecha(record.fch_ultima_serie_mensual)

        if mes_ultima_serie_diaria != mes_ultima_serie_mensual:
            return CONST_EST_DEFECTUOSO

        return CONST_EST_CORRECTO

    def eval_var_mensual(self, record: ResumenSerieModel):

        mes_primera_serie_diaria = Mes.from_fecha(record.fch_primera_serie_diaria)
        mes_primera_var_mensual = Mes.from_fecha(record.fch_primera_var_mensual)

        if mes_primera_serie_diaria != mes_primera_var_mensual:
            return CONST_EST_DEFECTUOSO

        mes_ultima_serie_diaria = Mes.from_fecha(record.fch_ultima_serie_diaria)
        mes_ultima_serie_mensual = Mes.from_fecha(record.fch_ultima_var_mensual)

        if mes_ultima_serie_diaria != mes_ultima_serie_mensual:
            return CONST_EST_DEFECTUOSO

        return CONST_EST_CORRECTO
