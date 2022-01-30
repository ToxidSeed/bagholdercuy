from re import S
from sqlalchemy.sql import elements
from common.Error import Error, is_error
import common.Markets as Markets
from flask import session
from model.Balance import Balance
from model.StockData import StockData
from sqlalchemy import func
from datetime import date
from common.api.MarketAPI import MarketAPI
from common.Response import Response
import common.Converter as Converter
from dateutil.relativedelta import * 
from controller.FundsManager import FundsManager

from app import app, db

from common.StatusMessage import StatusMessage
from model.StockTrade import StockTrade

class OverviewManager:
    CURRENT_BALANCE = 0
    OPTION_ASSET_TYPE = "OPTIONS"
    STOCK_ASSET_TYPE = "STOCK"

    def __init__(self):
        session["user_id"] = 1
        self.user_id = session["user_id"]        
        self.error = Error()

    def get(self, args={}):        
        response_list = []

        #get actual user trades
        trades = self.get_trades()

        #get balance        
        balance_list, error = self._refresh_balance(trades)
        if error is not None:
            return Response().from_error(error)            

        for element, create in balance_list:
            response_list.append(element)

        return Response(input_data=response_list).get()
                    

    def get_trades(self):
        trades = db.session.query(
            StockTrade.user_id,
            StockTrade.asset_type,
            StockTrade.symbol,
            StockTrade.trade_type,
            StockTrade.shares_balance,
            StockTrade.buy_price
        ).filter(
            StockTrade.user_id == self.user_id
        ).all()

        return trades
    
    def _refresh_balance(self, trades=None):
        balance_list = []
        balance, error = self._calc_current_balance(trades)
        if error is not None:
            return (None, error)        

        balance_list.append(balance)       
        
        #save if no balance created
        self._create_new_balance(balance_list)

        return (balance_list,None)

    def _create_new_balance(self, balance_list = []):        
        for element,create in balance_list:
            if create:
                new_balance = Balance(
                    user_id = element["user_id"],
                    profundidad_id = element["profundidad_id"],
                    fec_modificacion = date.today(),
                    inversion_imp = element["inversion_imp"],
                    cash_imp = element["cash_imp"],
                    gain_loss_imp = element["gain_loss_imp"],
                    net_worth_imp = element["net_worth_imp"]
                )
                db.session.add(new_balance)
        db.session.commit()
        
        
    def _calc_current_balance(self, trades=[]):    
        balance = 0
        gp_imp = 0
        net_worth_imp = 0
        inversion_imp = 0
        cash_imp = 0       
        elements = {}

        current_balance = Balance.query.filter(
            Balance.user_id == self.user_id,
            Balance.profundidad_id == OverviewManager.CURRENT_BALANCE
        ).first()

        if current_balance is not None:
            inversion_imp = float(current_balance.inversion_imp)
            cash_imp = float(current_balance.inversion_imp)

        for trade in trades:
            shares_balance = float(trade.shares_balance)   
            buy_price = float(trade.buy_price) 
            quote, error = self._get_last_quote(trade, elements)

            if trade.asset_type.upper() == OverviewManager.OPTION_ASSET_TYPE:
                inversion_imp += shares_balance*buy_price*100
                balance += shares_balance*quote.close*100

            if trade.asset_type.upper() == OverviewManager.STOCK_ASSET_TYPE:
                inversion_imp += shares_balance*buy_price
                balance += shares_balance*quote.close
            
        
        gp_imp = balance - inversion_imp 
        net_worth_imp = balance + cash_imp

        balance_obj = {
            "user_id":self.user_id,
            "profundidad_id":OverviewManager.CURRENT_BALANCE,
            "inversion_imp":inversion_imp,
            "cash_imp":cash_imp,
            "gain_loss_imp":gp_imp,
            "net_worth_imp":net_worth_imp
        }

        return ((balance_obj, True), None)

    def _get_last_quote(self, trade=None, elements={}):
        if trade.symbol not in elements:
            quote, error = MarketAPI().get_last_quote({"symbol":symbol,"asset_type":asset_type})                
            if error is not None:
                return (None, error)
            elements[trade.symbol] = quote
        else:
            quote = elements[trade.symbol]

        return (quote, None)





        

  
            