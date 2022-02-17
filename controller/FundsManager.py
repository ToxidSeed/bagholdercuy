from sqlalchemy.sql.functions import user
from sqlalchemy import func
from model.FundsHistory import FundsHistory
from common.Error import Error
from common.Response import Response
from datetime import date
from app import db

class FundsManager:
    TYPE_INCOME = 'I'
    TYPE_OUTCOME = 'O'

    def __init__(self):
        pass

    def get_funds(self, args={}):
        funds = db.session.query(FundsHistory.moneda_symbol,func.sum(FundsHistory.importe)).group_by(FundsHistory.moneda_symbol).all()

        return Response().from_raw_data(funds)


class Deposit:
    def __init__(self):
        pass

    def do(self, args={}):
        error = self.__val_add_fund(args)
        if error is not None:
            return Response().from_error(error)

        #add fund        
        new_deposit = FundsHistory(
            fec_registro = date(),
            estado_id = 0,
            tipo_transaccion = FundsManager.TYPE_INCOME,
            importe = args["importe"],
            moneda_symbol = args["moneda_symbol"],
            concepto = ""
        )

        try:
            db.session.add(new_deposit)
            db.session.commit()
            return Response(msg="Se ha depositado correctamente").get()
        except:
            db.session.rollback()
            return Response(success=False, msg="Se ha depositado correctamente").get()


    def __val_add_fund(self, args={}):
        error = Error()
        if "moneda_symbol" not in args:
            error.add("El parámetro 'moneda_symbol' no se encuentra en la petición")

        if "importe" not in args:
            error.add("El parámetro 'importe' no se encuentra en la petición")

            importe = float(args["importe"])
            if importe <= 0:
                error.add("El importe ingresados es menor o igual a 0")

        if error.has_errors():
            return error
        else:
            return None



    




        