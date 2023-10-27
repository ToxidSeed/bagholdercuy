from model.posicion import PosicionModel
from model.operacion import OperacionModel

from app import db

class PosicionProcessor:
    def cambiar_posicion(self, posicion:PosicionModel, operacion:OperacionModel):
        #si la posicion no es nueva se actualiza
        posicion.cantidad = posicion.cantidad + operacion.cantidad
        posicion.id_ultima_operacion = operacion.id_operacion

        #si es nueva se inserta uno nuevo
        if posicion.id_posicion is None:
            db.session.add(posicion)
        
    
    
        

