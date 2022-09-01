from cmath import exp
from app import app, db, localStorage
from model.OptionContract import OptionContractModel
from model.StockSymbol import StockSymbol
from datetime import date, datetime
import common.Converter as Converter
from common.AppException import AppException
from config.general import TMP_OPCIONES_CONTRATO_FILE, NUMERIC_DATE_FORMAT
import json

from common.Response import Response
from sqlalchemy.sql.functions import func

from common.api.iexcloud import iexcloud

class OpcionesContratoManager:
    def __init__(self):
        pass

    def get_options_chain(self, args={}):
        symbol = args["symbol"]
        expiration_date = args["expiration_date"]
        calls = self.get_calls(args=args)
        puts = self.get_puts(args=args)        
                
        data = {
            "calls":Converter.process_list(calls),
            "puts":Converter.process_list(puts),
            "exp_dates":Converter.format(self.get_expiration_dates(args=args)),
            "strikes":Converter.format(self.get_strikes(symbol, expiration_date))
        }
                
        return Response().from_raw_data(data)

    def get_calls(self, args={}):
        contract = args["contract"]

        query = db.session.query(
            OptionContractModel
        ).filter(
            OptionContractModel.side == 'call',
        )

        if contract != "":
            contract = "%{}%".format(contract)

            query = query.filter(
                OptionContractModel.symbol.ilike(contract)
            )       

            return query.all()

        symbol = args["symbol"]
        exp_date = args["expiration_date"]
        strike = args["strike"]

        if symbol != "":
            query = query.filter(
                OptionContractModel.underlying == symbol    
            )

        if exp_date == "":
            query = query.filter(
                OptionContractModel.expiration_date >= date.today().isoformat()
            )
        else:
            query = query.filter(
                OptionContractModel.expiration_date == exp_date
            )

        if strike != "":
            query = query.filter(
                OptionContractModel.strike == strike
            )

        query = query.order_by(OptionContractModel.expiration_date, OptionContractModel.strike)

        return query.all()

    def get_puts(self, args={}):
        contract = args["contract"]

        query = db.session.query(
            OptionContractModel
        ).filter(
            OptionContractModel.side == 'put',
        )

        if contract != "":
            contract = "%{}%".format(contract)

            query = query.filter(
                OptionContractModel.symbol.ilike(contract)
            )       

            return query.all()

        symbol = args["symbol"]
        exp_date = args["expiration_date"]
        strike = args["strike"]

        if symbol != "":
            query = query.filter(
                OptionContractModel.underlying == symbol    
            )

        if exp_date == "":
            query = query.filter(
                OptionContractModel.expiration_date >= date.today().isoformat()
            )
        else:
            query = query.filter(
                OptionContractModel.expiration_date == exp_date
            )

        if strike != "":
            query = query.filter(
                OptionContractModel.strike == strike
            )

        query = query.order_by(OptionContractModel.expiration_date, OptionContractModel.strike)

        return query.all()

    def get_expiration_dates(self, args={}):
        symbol=args["symbol"] #symbol is required
        expiration_date=date.today().isoformat()
        strike=""
        
        query = db.session.query(
            OptionContractModel.expiration_date
        ).distinct(OptionContractModel.expiration_date)

        query = query.filter(               
            OptionContractModel.underlying == symbol
        )
        query = query.filter(OptionContractModel.expiration_date >= expiration_date)

        results = query.all()

        exp_list = []
        for row in results:
            exp_list.append(row.expiration_date)

        return exp_list

    def get_strikes(self, symbol="", exp_date=""):                
        query = db.session.query(
            OptionContractModel.strike
        ).distinct(OptionContractModel.strike)

        query = query.filter(            
            OptionContractModel.underlying == symbol
        )        

        if exp_date == "":
            query = query.filter(            
                OptionContractModel.expiration_date  >= date.today().isoformat()
            )   
        else:
            query = query.filter(            
                OptionContractModel.expiration_date  == exp_date
            )

        query = query.order_by(OptionContractModel.strike)

        results = query.all()

        strikes = []
        for row in results:
            strikes.append(float(row.strike))
        
        return strikes

    def get_resumen_subyacentes(self, args={}):
        result = db.session.query(
            OptionContractModel.underlying,
            func.max(OptionContractModel.register_date).label("fch_registro"),
            func.max(OptionContractModel.expiration_date).label("fch_vencimiento")
        ).group_by(
            OptionContractModel.underlying
        ).all()        

        return Response().from_raw_data(result)

    def get_list_contratos(self, args={}):
        result = db.session.query(
            OptionContractModel.id,
            OptionContractModel.moneda_id,
            OptionContractModel.description.label("descripcion"),
            OptionContractModel.expiration_date.label("fch_expiracion"),
            OptionContractModel.side.label("lado"),
            OptionContractModel.strike.label("strike"),
            OptionContractModel.symbol,
            OptionContractModel.underlying.label("subyacente"),
            OptionContractModel.register_date.label("fch_registro")
        ).order_by(OptionContractModel.expiration_date.desc())\
        .limit(20)\
        .all()

        return Response().from_raw_data(result)



class SymbolLoader:
    def __init__(self):
        pass

    def get_contratos(self, symbol="",fch_exp=""):         
        filename = localStorage.getItem(TMP_OPCIONES_CONTRATO_FILE)
        if filename is not None:
            try:
                return self.get_contratos_de_tmp(filename)
            except FileNotFoundError:
                filename = ""
            
        #si no existe como fichero temporal se procede a obtener de la API
        args = {
            "symbol":symbol
        }

        data = iexcloud().get_contracts(args)
        filename = "{0}_CONTRATOSOPCIONES.json".format(symbol)
        localStorage.setItem(TMP_OPCIONES_CONTRATO_FILE,filename)
        self.guardar_fichero_temp(filename, json.dumps(data))
        return data

    def get_contratos_de_tmp(self, filename=""):
        with open('tmp/'+filename) as f:
            contratos = f.read()
        return contratos

    def guardar_fichero_temp(self, filename="", data=""):
        with open('tmp/'+filename,'w') as f:
            f.write(data)   

    def get_symbol(self, symbol=""):
        sym = db.session.query(
            StockSymbol
        ).filter(
            StockSymbol.symbol == symbol
        ).first()

        if sym is None:
            raise AppException(msg="El symbol {0} no existe en la base de datos".format(symbol))

        return sym         

    def get_contrato(self, symbol=""):
        contrato = OptionContractModel.query.filter(
            OptionContractModel.symbol == symbol
        ).first()

        return contrato

    def load(self, args={}) :
        symbol=args.get("symbol")
        if symbol is None or symbol == "":
            raise AppException(msg="No se ha ingresado el symbol")

        symbolobj = self.get_symbol(symbol)
        
        fch_exp = args.get("fch_exp")
        if fch_exp is not None and fch_exp != "":
            fch_ex_date = datetime.strptime(fch_exp,NUMERIC_DATE_FORMAT)

        contratos = self.get_contratos(symbol, fch_exp)
        contratos = json.loads(contratos)
        for elem in contratos:
            contrato_symbol = elem.get("symbol")
            contrato = self.get_contrato(contrato_symbol)   
            if contrato is None:
                #adding the details
                oc = OptionContractModel(     
                    moneda_id = symbolobj.moneda_id,               
                    contract_size = elem["contractSize"],
                    currency = elem["currency"],
                    description = elem["description"],
                    expiration_date = elem["expirationDate"],
                    side = elem["side"],
                    strike = elem["strike"],
                    symbol = elem["symbol"],
                    underlying = elem["underlying"],
                    register_date = date.today(),
                    fch_audit = datetime.now()
                )
                db.session.add(oc)
        db.session.commit()
        return Response(msg="Se han cargado correctamente los symbol de los contratos para {}".format(symbol)).get()