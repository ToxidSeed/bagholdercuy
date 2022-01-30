from sqlalchemy.sql.functions import user
from model.FundsHistory import FundsHistory
from common.Error import Error

class FundsManager:

    INCOME_MOV = 'I'
    OUTCOME_MOV = 'O'

    def __init__(self):
        pass        

    @staticmethod
    def _recalculate_cash(self, user_id=None):
        funds_history = FundsHistory.query.filter(
            FundsHistory.user_id == user_id
        ).all()

        cash_imp = 0

        for fund in funds_history:
            if fund.flg_tipo_movimiento == FundsManager.INCOME_MOV:
                cash_imp+=fund.importe
            if fund.flg_tipo_movimiento == FundsManager.OUTCOME_MOV:
                cash_imp-=fund.importe
            else:
                return (cash_imp, Error(msg="Tipo de movimiento no soportado ({}), revisar los distintos tipos de movimiento registrados".format(fund.flg_tipo_movimiento)))

        return (cash_imp, Error)


    




        