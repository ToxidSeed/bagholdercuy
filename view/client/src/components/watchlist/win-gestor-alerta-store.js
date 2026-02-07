import { TIPO_VARIACION_TITULO} from "@/common/app-constants.js"

import ConfiguracionAlerta from "@/api/configuracion-alerta"
import Symbol from "@/api/symbol"
import GestorObjeto from "@/common/gestor-objeto"

export default {    
    state:{
        open:false,     
        title:"Gestor de alertas",   
        estado:"",        
        configuracion_alerta:{
            id_config_alerta:"",
            id_cuenta:"",
            id_monitoreo:"",
            id_symbol:"",
            imp_inicial_ciclos:"",
            ctd_ciclos:"",
            ctd_variacion_imp_accion:"",
            cod_tipo_variacion_imp_accion:"",

        },
        symbol:{
            id_symbol:"",
            cod_symbol:"",
            nom_symbol:""
        }
    },
    nuevo:function(){
        this.state.open = true
        this.reset()
    },
    reset:function(){
        this.state.id_config_alerta = ""
        this.state.estado ="nuevo"
        this.state.title = "Registro de una configuracion de alerta"

        new GestorObjeto(this.state.configuracion_alerta).reset({
            cod_tipo_variacion_imp_accion: TIPO_VARIACION_TITULO.COD_IMPORTE
        })

        new GestorObjeto(this.state.symbol).reset()        
    },
    editar: async function(id_config_alerta){
        this.state.open = true        
        this.state.estado = "editar"
        this.state.title = "Editando configuracion con id# "+id_config_alerta
        let data = await ConfiguracionAlerta.get_alerta(id_config_alerta) 
        new GestorObjeto(this.state.configuracion_alerta).set_data(data)
        //GestorObjeto.set_data(this.state.configuracion_alerta, data)    
        let symbol = await Symbol.get_symbol(this.state.configuracion_alerta.id_symbol)
        this.set_symbol(symbol)
                
    },
    incluir_alerta: async function(id_monitoreo, id_symbol){        
        this.state.open = true        
        this.state.estado = "incluir_alerta"        
        this.state.configuracion_alerta.id_monitoreo = id_monitoreo
        this.state.configuracion_alerta.id_symbol = id_symbol
        this.state.configuracion_alerta.cod_tipo_variacion_imp_accion = TIPO_VARIACION_TITULO.COD_IMPORTE
        
        let symbol = await Symbol.get_symbol(this.state.configuracion_alerta.id_symbol)        
        this.set_symbol(symbol)
        this.state.title = "Incluir alerta al symbol "+this.state.symbol.cod_symbol
    },
    set_symbol: function(objeto){
        this.state.symbol.id_symbol = objeto.id
        this.state.symbol.cod_symbol = objeto.symbol
        this.state.symbol.nom_symbol = objeto.name
    },
    guardar: async function(){      
        if(this.state.estado == "incluir_alerta"){
            await ConfiguracionAlerta.incluir_en_monitoreo(this.state.configuracion_alerta)
        }
        if(this.state.estado == "nuevo"){
            await ConfiguracionAlerta.registrar(this.state.configuracion_alerta)
        }
        if(this.state.estado == "editar"){
            await ConfiguracionAlerta.actualizar(this.state.configuracion_alerta)
        }        
    },
    cerrar:function(){
        this.state.open = false
        this.reset()
    }
}
