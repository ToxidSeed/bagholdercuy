from app import db

class TransaccionFondosModel(db.Model):
    __tablename__="tb_transaccion_fondos"

    id = db.Column(db.Integer,primary_key=True)
    fch_transaccion = db.Column(db.Date)
    num_transaccion = db.Column(db.Integer)    
    tipo_trans_id = db.Column(db.Integer)    
    imp_transaccion = db.Column(db.Numeric(15,2))
    mon_trans_id = db.Column(db.String(3))          
    info_adicional = db.Column(db.String)
    usuario_id = db.Column(db.Integer)
    fch_registro = db.Column(db.Date)
    fch_audit = db.Column(db.DateTime)

    def get_conversion(transaccion_id):
        from model.conversionmoneda import ConversionMonedaModel
        conversion = ConversionMonedaModel.query.filter(
            ConversionMonedaModel.transaccion_id == transaccion_id
        ).one()
        return conversion