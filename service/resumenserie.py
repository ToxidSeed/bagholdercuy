from reader.seriediaria import SerieDiariaReader
from reader.variaciondiaria import VariacionDiariaReader
from reader.seriesemanal import SerieSemanalReader
from reader.variacionsemanal import VariacionSemanalReader
from reader.seriemensual import SerieMensualReader
from reader.variacionmensual import VariacionMensualReader
from model.resumenserie import ResumenSerieModel
from datetime import date, datetime
from app import db

class ResumenSerieService:
    def guardar(self, cod_symbol):
        record = ResumenSerieModel.get_record(cod_symbol)
        if record:
            self.upd_resumen_serie(cod_symbol, record)
        else:
            self.ins_resumen_serie(cod_symbol)

    def ins_resumen_serie(self, cod_symbol):
        stats_serie_diaria = SerieDiariaReader.get_estadisticas(cod_symbol)
        stats_var_diaria = VariacionDiariaReader.get_estadisticas(cod_symbol)
        stats_serie_semanal = SerieSemanalReader.get_estadisticas(cod_symbol)
        stats_var_semanal = VariacionSemanalReader.get_estadisticas(cod_symbol)
        stats_serie_mensual = SerieMensualReader.get_estadisticas(cod_symbol)
        stats_var_mensual = VariacionMensualReader.get_estadisticas(cod_symbol)

        nu_record = ResumenSerieModel(
            cod_symbol=cod_symbol,
            fch_primera_serie_diaria=stats_serie_diaria.min_fch_serie,
            fch_ultima_serie_diaria=stats_serie_diaria.min_fch_serie,
            num_series_diarias=stats_serie_diaria.cantidad,

            fch_primera_var_diaria=stats_var_diaria.min_fch_variacion,
            fch_ultima_var_diaria=stats_var_diaria.max_fch_variacion,
            num_var_diarias=stats_var_diaria.cantidad,

            fch_primera_serie_semanal=stats_serie_semanal.fch_semana_min,
            fch_ultima_serie_semanal=stats_serie_semanal.fch_semana_max,          
            num_series_semanales=stats_serie_semanal.cantidad,

            fch_primera_var_semanal=stats_var_semanal.fch_semana_min,
            fch_ultima_var_semanal=stats_var_semanal.fch_semana_max,
            num_var_semanales=stats_var_semanal.cantidad,

            fch_primera_serie_mensual=stats_serie_mensual.min_fch_mes,
            fch_ultima_serie_mensual=stats_serie_mensual.max_fch_mes,
            num_series_mensuales=stats_serie_mensual.cantidad,

            fch_primera_var_mensual=stats_var_mensual.min_fch_mes,
            fch_ultima_var_mensual=stats_var_mensual.max_fch_mes,
            num_vars_mensuales=stats_var_mensual.cantidad,

            fch_registro=date.today(),
            fch_actualizacion=datetime.now()
        )

        db.session.add(nu_record)

    def upd_resumen_serie(self, cod_symbol, resumen_serie:ResumenSerieModel):
        stats_serie_diaria = SerieDiariaReader.get_estadisticas(cod_symbol)
        stats_var_diaria = VariacionDiariaReader.get_estadisticas(cod_symbol)
        stats_serie_semanal = SerieSemanalReader.get_estadisticas(cod_symbol)
        stats_var_semanal = VariacionSemanalReader.get_estadisticas(cod_symbol)
        stats_serie_mensual = SerieMensualReader.get_estadisticas(cod_symbol)
        stats_var_mensual = VariacionMensualReader.get_estadisticas(cod_symbol)

        resumen_serie.fch_primera_serie_diaria=stats_serie_diaria.min_fch_serie
        resumen_serie.fch_ultima_serie_diaria=stats_serie_diaria.min_fch_serie
        resumen_serie.num_series_diarias=stats_serie_diaria.cantidad

        resumen_serie.fch_primera_var_diaria=stats_var_diaria.min_fch_variacion
        resumen_serie.fch_ultima_var_diaria=stats_var_diaria.max_fch_variacion
        resumen_serie.num_var_diarias = stats_var_diaria.cantidad

        resumen_serie.fch_primera_serie_semanal=stats_serie_semanal.fch_semana_min
        resumen_serie.fch_ultima_serie_semanal=stats_serie_semanal.fch_semana_max
        resumen_serie.num_series_semanales=stats_serie_semanal.cantidad

        resumen_serie.fch_primera_var_semanal=stats_var_semanal.fch_semana_min
        resumen_serie.fch_ultima_var_semanal=stats_var_semanal.fch_semana_max
        resumen_serie.num_var_semanales=stats_var_semanal.cantidad

        resumen_serie.fch_primera_serie_mensual=stats_serie_mensual.min_fch_mes
        resumen_serie.fch_ultima_serie_mensual=stats_serie_mensual.max_fch_mes
        resumen_serie.num_series_mensuales=stats_serie_mensual.cantidad

        resumen_serie.fch_primera_var_mensual=stats_var_mensual.min_fch_mes
        resumen_serie.fch_ultima_var_mensual=stats_var_mensual.max_fch_mes
        resumen_serie.num_vars_mensuales=stats_var_mensual.cantidad

        resumen_serie.fch_actualizacion=datetime.now()

        

