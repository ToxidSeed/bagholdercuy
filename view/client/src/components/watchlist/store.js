import Monitoreo from "@/api/monitoreo"
import Cotizacion from "@/api/cotizacion"
import Vue from 'vue'

let table_monitoreo = {
    state:{
        params:{},
        monitoreo_activo_data:[]
    },
    get_monitoreo_activo: async function(params){                  
        if (params == undefined){
            this.state.params = {}
        }else{
            this.state.params = params
        }
        
        this.state.monitoreo_activo_data = await new Monitoreo().get_monitoreo_activo(
            this.state.params 
        )       
        this.aplicar_cotizacion()                 
    },
    refresh: async function(){
        this.state.monitoreo_activo_data = await new Monitoreo().get_monitoreo_activo(
            this.state.params 
        )       
        this.aplicar_cotizacion()                 
    },
    aplicar_cotizacion:async function(){                  
        await Promise.all(this.state.monitoreo_activo_data.map(async (element) => {
            let cotizacion = await Cotizacion.get_cotizacion(element.cod_symbol)                
            Vue.set(element, 'imp_actual', cotizacion.imp_cierre)
            Vue.set(element, 'imp_cierre_anterior', cotizacion.imp_cierre_anterior)            
        }))        
    }
}

let panel_watchlist = {
    state:{},
    registrar: async function(params){
        await new Monitoreo().registrar(params)
    }
}

export default {
    table_monitoreo: table_monitoreo,
    panel_watchlist: panel_watchlist
}