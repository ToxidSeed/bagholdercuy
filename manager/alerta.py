from model.configuracionalerta import ConfiguracionAlertaModel
from model.alerta import AlertaModel
from config.negocio import TIPO_VARIACION_TITULO, TIPO_VARIACION_EJERCICIO
from app import db
from common.AppException import AppException

class AlertaManager:
    def __init__(self):
        self.__ciclos_procesados = {}        

    def generar(self, configuracion_alerta:ConfiguracionAlertaModel):
        ctd_ciclos_abajo, ctd_ciclos_arriba = self.get_ciclos_x_direccion(configuracion_alerta.ctd_ciclos)

        self.eliminar_alertas(configuracion_alerta.id_symbol)        
        self.crear_alertas_para_abajo(ctd_ciclos_abajo=ctd_ciclos_abajo, configuracion_alerta=configuracion_alerta)
        self.crear_alertas_para_arriba(ctd_ciclos_arriba=ctd_ciclos_arriba, configuracion_alerta=configuracion_alerta)        

    def eliminar_alertas(self, id_symbol):
        query = db.delete(
            AlertaModel
        ).where(
            AlertaModel.id_symbol == id_symbol
        )

        db.session.execute(query)        

    def crear_alerta(self, imp_alerta, configuracion_alerta:ConfiguracionAlertaModel):
                
        imp_ejercicio_compra_call, imp_ejercicio_venta_put, imp_ejercicio_venta_call, imp_ejercicio_compra_put = self.calcular_imp_ejercicio(imp_alerta=imp_alerta, configuracion_alerta=configuracion_alerta)

        alerta = AlertaModel(
            id_config_alerta = configuracion_alerta.id_config_alerta,
            id_symbol = configuracion_alerta.id_symbol,
            imp_alerta = imp_alerta,
            imp_ejercicio_compra_call = imp_ejercicio_compra_call,
            imp_ejercicio_venta_put = imp_ejercicio_venta_put,
            imp_ejercicio_venta_call = imp_ejercicio_venta_call,
            imp_ejercicio_compra_put = imp_ejercicio_compra_put,
            num_dias_expiracion_call = configuracion_alerta.num_dias_expiracion_call,
            num_dias_expiracion_put = configuracion_alerta.num_dias_expiracion_put
        )      

        db.session.add(alerta)      

    def get_ciclos_x_direccion(self, ctd_ciclos):
        ctd_ciclos_abajo = ctd_ciclos // 2
        ctd_ciclos_arriba = ctd_ciclos - ctd_ciclos_abajo
        return (ctd_ciclos_abajo, ctd_ciclos_arriba)

    def crear_alertas_para_abajo(self, ctd_ciclos_abajo, configuracion_alerta:ConfiguracionAlertaModel):
        imp_alerta_anterior = None
        for num_ciclo in range(-1, abs(ctd_ciclos_abajo)*-1,-1):
            imp_alerta_anterior = configuracion_alerta.imp_inicio_ciclos if num_ciclo == -1 else imp_alerta_anterior                 

            #una vez itendificada la alerta anterior procedemos a calcular la alerta
            imp_alerta = self.calcular_imp_alerta(imp_alerta_anterior=imp_alerta_anterior, configuracion_alerta=configuracion_alerta, flg_alerta_inferior=True)
            self.crear_alerta(imp_alerta=imp_alerta, configuracion_alerta=configuracion_alerta)
            imp_alerta_anterior = imp_alerta

    def crear_alertas_para_arriba(self, ctd_ciclos_arriba, configuracion_alerta: ConfiguracionAlertaModel):
        imp_alerta_anterior = None
        for num_ciclo in range(0, abs(ctd_ciclos_arriba)):
            #se crea la alerta porque se incluye el inicio de los ciclos
            if num_ciclo == 0:
                imp_alerta = configuracion_alerta.imp_inicio_ciclos
                self.crear_alerta(imp_alerta=imp_alerta, configuracion_alerta=configuracion_alerta)
                imp_alerta_anterior = imp_alerta
                continue

            #para todos los demas                        
            imp_alerta = self.calcular_imp_alerta(imp_alerta_anterior=imp_alerta_anterior, configuracion_alerta=configuracion_alerta, flg_alerta_inferior=False)
            self.crear_alerta(imp_alerta=imp_alerta, configuracion_alerta=configuracion_alerta)
            imp_alerta_anterior = imp_alerta

    def calcular_imp_alerta(self, imp_alerta_anterior, configuracion_alerta: ConfiguracionAlertaModel, flg_alerta_inferior:bool=True):                        
        
        signo_multiplicador = -1 if flg_alerta_inferior is True else 1
        
        if configuracion_alerta.cod_tipo_variacion_titulo == TIPO_VARIACION_TITULO.COD_IMPORTE:            
            imp_alerta_nueva = imp_alerta_anterior + signo_multiplicador * configuracion_alerta.ctd_variacion_titulo                        

        if configuracion_alerta.cod_tipo_variacion_titulo == TIPO_VARIACION_TITULO.COD_PORCENTAJE:            
            imp_alerta_nueva = imp_alerta_anterior + signo_multiplicador * (imp_alerta_anterior * configuracion_alerta.ctd_variacion_titulo)/100
        
        return imp_alerta_nueva        
    
    def get_imp_alerta_anterior(self, num_ciclo, configuracion_alerta:ConfiguracionAlertaModel):
        if num_ciclo < 0:
            num_ciclo_ant = num_ciclo + 1
            alerta_ant = self.__ciclos_procesados.get(num_ciclo_ant)
            imp_alerta_ant = configuracion_alerta.imp_inicio_ciclos if alerta_ant is None else alerta_ant.imp_alerta
            return imp_alerta_ant
    
        if num_ciclo > 0:
            num_ciclo_ant = num_ciclo - 1
            alerta_ant = self.__ciclos_procesados.get(num_ciclo_ant)
            imp_alerta_ant = configuracion_alerta.imp_inicio_ciclos if alerta_ant is None else alerta_ant.imp_alerta
            return imp_alerta_ant
          
    def calcular_imp_ejercicio(self, imp_alerta, configuracion_alerta: ConfiguracionAlertaModel):

        if configuracion_alerta.cod_tipo_variacion_ejercicio == TIPO_VARIACION_EJERCICIO.COD_IMPORTE_FIJO:
            imp_ejercicio_compra_call = configuracion_alerta.imp_fijo_ejercicio_call
            imp_ejercicio_venta_put = configuracion_alerta.imp_fijo_ejercicio_put

            imp_ejercicio_venta_call = configuracion_alerta.imp_fijo_ejercicio_call
            imp_ejercicio_compra_put = configuracion_alerta.imp_fijo_ejercicio_put

            return (imp_ejercicio_compra_call, imp_ejercicio_venta_put, imp_ejercicio_venta_call, imp_ejercicio_compra_put)
        
        if configuracion_alerta.cod_tipo_variacion_ejercicio == TIPO_VARIACION_EJERCICIO.COD_VARIACION_SUBYACENTE:
            imp_ejercicio_compra_call = imp_alerta - abs(configuracion_alerta.imp_variacion_subyacente_call)
            imp_ejercicio_venta_put = imp_alerta - abs(configuracion_alerta.imp_variacion_subyacente_put)

            imp_ejercicio_venta_call = imp_alerta + abs(configuracion_alerta.imp_variacion_subyacente_call)
            imp_ejercicio_compra_put = imp_alerta + abs(configuracion_alerta.imp_variacion_subyacente_put)
            
            return (imp_ejercicio_compra_call, imp_ejercicio_venta_put, imp_ejercicio_venta_call, imp_ejercicio_compra_put)

    