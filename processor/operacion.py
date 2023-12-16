from common.AppException import AppException

from model.orden import OrdenModel
from model.operacion import OperacionModel
from model.posicion import PosicionModel
from reader.operacion import OperacionReader
from reader.posicion import PosicionReader

from config.app_constants import TIPO_OPERACION_TRANSFERENCIA, TIPO_ORDEN_COMPRA, TIPO_ORDEN_VENTA
from datetime import date, datetime
from operator import methodcaller

from app import db

class OperacionProcessor:   
    def __init__(self):
        self.operaciones_registradas = {}
        self.fechas_desde_recalcular_posicion = []
                
        """    
        posiciones_afectadas: guardara como key del dict id_cuenta-id_symbol-id_contrato_opcion = tupla(posicion, ultima operacion que ha afectado la posicion, fecha reproceso si aplica)
        """
        self.posiciones_afectadas = {} 

        #readers
        self.operacion_reader = OperacionReader()
        self.posicion_reader = PosicionReader()
        
    def procesar_orden(self, orden:OrdenModel, posicion:PosicionModel=None, operacion:OperacionModel=None, num_orden_operacion=None):

        ctd_operacion = (orden.cantidad if orden.cod_tipo_orden == TIPO_ORDEN_COMPRA else orden.cantidad * -1)
        nom_tipo_orden = "Compra" if orden.cod_tipo_orden == TIPO_ORDEN_COMPRA else "Venta"
        dsc_glosa_operacion = f"{nom_tipo_orden}: {ctd_operacion} x {orden.imp_accion}"

        if num_orden_operacion is None:
            num_orden_operacion = self.__get_siguiente_num_orden_operacion(orden.id_cuenta, orden.fch_orden)
        
        #posicion = self.__get_posicion(id_cuenta=orden.id_cuenta, id_symbol=orden.id_symbol, id_contrato_opcion=orden.id_contrato_opcion)
        if operacion is None:
            ctd_nueva_posicion = ctd_operacion if posicion is None else posicion.cantidad
        else:
            ctd_nueva_posicion = operacion.ctd_posicion + ctd_operacion

        oper = OperacionModel(
            id_cuenta = orden.id_cuenta,
            fch_operacion = orden.fch_orden,
            num_orden = num_orden_operacion,
            id_tipo_operacion = orden.cod_tipo_orden,
            id_symbol = orden.id_symbol,
            id_contrato_opcion = orden.id_contrato_opcion,
            cantidad = ctd_operacion,
            ctd_posicion = ctd_nueva_posicion,
            dsc_glosa_operacion = dsc_glosa_operacion,
            fch_registro = date.today()
        )

        db.session.add(oper)
        return oper            

    
class AlteracionPosicion:
    def __init__(self, posicion=None, operaciones=[], fch_reproceso=None, flg_reproceso=None):        
        self.posicion = posicion
        self.operaciones = operaciones        
        self.fch_reproceso = fch_reproceso
        self.flg_reproceso = False
        self.__operacion_previa_alteracion = None

    @property
    def operacion_previa_alteracion(self):
        return self.__operacion_previa_alteracion

    def incluir_operacion(self, operacion:OperacionModel):
        self.operaciones.append(operacion)            

    def incluir_operacion_previa(self, operacion:OperacionModel):
        self.__operacion_previa_alteracion = operacion

    def get_primera_operacion(self):
        if len(self.operaciones) > 0:
            return self.operaciones[0]
        
    def get_ultima_operacion(self):
        if len(self.operaciones) > 0:
            return self.operaciones[len(self.operaciones) - 1]                       

    def get_cambios_posicion(self):
        return (self.posicion, self.get_primera_operacion(), self.get_ultima_operacion(), self.operacion_anterior_alteracion_posicion, self.flg_reproceso)
    
  
class RegistroMultipleOperacionesManager:
    def __init__(self):
        self.operaciones_registradas = {}
        self.fechas_desde_recalcular_posicion = []
                        
        self.posiciones_afectadas = {} 

        #readers
        self.operacion_reader = OperacionReader()
        self.posicion_reader = PosicionReader()

    def get_posiciones_afectadas(self):
        
        cambios_posiciones =  map(methodcaller("get_cambios_posicion"),list(self.posiciones_afectadas.values()))
        return cambios_posiciones
        

    def registrar(self, operacion:OperacionModel):
        if operacion.id_operacion is not None:
            raise AppException(msg="Error al enviar una operacion con id")  

        #establecer posicion afectada              
        alteracion = self.__establecer_afectacion_posicion(operacion=operacion)

        #obtenemos la posicion anterior
        operacion_anterior = self.get_operacion_anterior(alteracion_posicion=alteracion, operacion=operacion)

        #establecer indicador de reproceso
        self.establecer_reproceso(alteracion=alteracion, operacion=operacion)

        #establecer numeracion de operacion
        self.__establecer_numeracion(operacion_anterior=operacion_anterior, operacion=operacion)        

        #establecer variacion de la posicion
        self.__establecer_var_posicion(afectacion=alteracion, operacion_anterior=operacion_anterior, operacion=operacion)        
        
        db.session.add(operacion)

        #guardamos en la memoria de las operaciones registradas
        alteracion.incluir_operacion(operacion=operacion)
        return operacion    

    def __establecer_afectacion_posicion(self, operacion:OperacionModel) -> AlteracionPosicion:
        cod_posicion = self.__cod_posicion(operacion=operacion)

        #buscar en memoria
        alteracion = self.posiciones_afectadas.get(cod_posicion)
        if alteracion is not None:
            return alteracion
        
        #buscar en almacen
        posicion = self.posicion_reader.get_posicion(id_cuenta=operacion.id_cuenta, id_symbol=operacion.id_symbol, id_contrato_opcion=operacion.id_contrato_opcion)
        if posicion is not None:
            alteracion = AlteracionPosicion(posicion=posicion)
            self.posiciones_afectadas[cod_posicion] = alteracion
            return alteracion            
        
        #Si no hay en almacen ni en memoria
        alteracion = AlteracionPosicion(posicion=None)
        self.posiciones_afectadas[cod_posicion] = alteracion
        return alteracion
    
    def establecer_reproceso(self, alteracion:AlteracionPosicion, operacion:OperacionModel):
        posicion = alteracion.posicion
        if alteracion.flg_reproceso is True:
            return
        
        if posicion is None:
            return
        
        ultima_operacion_almacen = self.operacion_reader.get(id_operacion=posicion.id_ultima_operacion)
        if ultima_operacion_almacen is None:
            raise AppException(msg=f"No se ha encontrado la operacion con id: {posicion.id_ultima_operacion}")
                    
        if ultima_operacion_almacen.fch_operacion > operacion.fch_operacion:
            alteracion.flg_reproceso = True
            return
        
                              
    def __establecer_numeracion(self, operacion_anterior:OperacionModel, operacion:OperacionModel):        

        if operacion_anterior is None:
            operacion.num_operacion = 1
            return 1
                      
        num_operacion = operacion_anterior.num_operacion + 1
        operacion.num_operacion = num_operacion
        return num_operacion        
    
    def get_operacion_anterior(self, alteracion_posicion:AlteracionPosicion, operacion:OperacionModel) -> OperacionModel:
        #        
        if alteracion_posicion.get_ultima_operacion() is not None:
            return alteracion_posicion.get_ultima_operacion()

        #buscamos en el almacen la ultima operacion:
        operacion_anterior = self.operacion_reader.get_ultima_operacion_hasta_fecha(id_cuenta=operacion.id_cuenta, id_symbol=operacion.id_symbol, id_contrato_opcion=operacion.id_contrato_opcion, fch_operacion=operacion.fch_operacion)        

        #incluimos la operacion previa a la alteracion de la posicion en el presente proceso
        alteracion_posicion.incluir_operacion_previa(operacion=operacion_anterior)
        return operacion_anterior
    
    def __establecer_var_posicion(self, afectacion:AlteracionPosicion, operacion_anterior:OperacionModel,  operacion:OperacionModel):
        #Si hay que reprocesar no se calcula nada
        if afectacion.flg_reproceso is True:
            return
                
        #Si no hay reproceso y la posicion anterior en la fecha no existe, se toma el dato de la posicion
        if operacion_anterior is None:            
            operacion.num_variacion_posicion = 1
            operacion.ctd_posicion = operacion.cantidad
            return
        
        #si la operacion anterior existe y no es un reproceso
        if operacion_anterior is not None:
            operacion.num_variacion_posicion = operacion_anterior.num_variacion_posicion + 1
            operacion.ctd_posicion = operacion_anterior.ctd_posicion + operacion.cantidad           
            return

        return None                

    def __cod_posicion(self, operacion:OperacionModel):
        return "-".join(map(str,[operacion.id_cuenta, operacion.id_symbol, operacion.id_contrato_opcion]))

class ReprocesarOperacionesManager:
    def __init__(self):
        self.operaciones_reader = OperacionReader()

    def reprocesar(self, id_cuenta, id_symbol, id_contrato_opcion, fch_reproceso):
        #obtener operaciones
        operaciones = self.operaciones_reader.get_operaciones_x_posicion_desde_fecha(id_cuenta, id_symbol, id_contrato_opcion, fch_operacion=fch_reproceso)
        for operacion in operaciones:
            pass

    def __calcular_datos_posicion(self):
        pass


#escenarios: 
"""
 1. si hay que reprocesar si o si existen otras operaciones:
 2. Si es la primera operacion para esa fecha pero ya hay operaciones en fechas siguientes
 3. Si no es la primera operacion para esa fecha

"""        
        
        
    

        
