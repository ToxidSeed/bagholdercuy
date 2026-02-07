from model.posicion import PosicionModel
from model.operacion import OperacionModel
from datetime import date

from app import db

class PosicionProcessor:
    def cambiar_posicion(self, posicion:PosicionModel, operacion:OperacionModel):
        #si la posicion no es nueva se actualiza
        posicion.cantidad = posicion.cantidad + operacion.cantidad
        posicion.id_ultima_operacion = operacion.id_operacion

        #si es nueva se inserta uno nuevo
        if posicion.id_posicion is None:
            db.session.add(posicion)

    def crear_posicion_de_operacion(self, operacion:OperacionModel):
        posicion = PosicionModel(
            id_cuenta = operacion.id_cuenta,
            id_symbol = operacion.id_symbol,
            id_contrato_opcion = operacion.id_contrato_opcion,
            id_ultima_operacion = operacion.id_operacion,
            cantidad = operacion.cantidad,
            fch_registro = date.today(),
            fch_ultima_actualizacion = date.today()
        )
        
        db.session.add(posicion)
    
    
        

