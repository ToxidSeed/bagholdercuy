from datetime import date

def get_fch_inicio_mes(fecha):
    anyo = fecha.year
    mes = fecha.month
    day = 1
        
    return date(anyo, mes, day)
 