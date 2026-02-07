from datetime import date, timedelta
VIERNES = 5
SABADO = 6
DOMINGO = 7


def get_ultimo_dia_util():
    hoy = date.today()    
    ayer = hoy - timedelta(days=1)
    anyo, semana, dia = ayer.isocalendar()
    if dia in [SABADO, DOMINGO]:
        fch_ult_dia_util = date.fromisocalendar(anyo, semana, VIERNES)
    else:
        fch_ult_dia_util = ayer

    return fch_ult_dia_util