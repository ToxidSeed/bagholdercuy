from datetime import date


def get_fch_inicio_semana(fecha):
    num_anyo, num_semana, num_dia_semana = fecha.isocalendar()
    return date.fromisocalendar(num_anyo, num_semana, 1)
 