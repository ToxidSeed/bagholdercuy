import GestorObjeto from '../../common/gestor-objeto'
import VariacionSemanal from "../../api/variacion-semanal"
import Symbol from "@/api/symbol"
import store from "@/store/store"

let panel_evolucion_semanal = {
    state:{
        cod_symbol:"",
        nom_symbol:"",
        anyo:"",
        semana:""
    },
    set_properties: function(payload){
        let gestorObjeto = new GestorObjeto(this.state)
        gestorObjeto.set_campos(payload)
    },
    completar_symbol: function(cod_symbol){
        let symbol_api = Symbol
        let request = symbol_api.get_symbol_x_codigo(cod_symbol)
        request.then(httpresp => {
            let appdata = httpresp.data.data
            this.state.nom_symbol = appdata.name                    
        })
        //this.state.nom_symbol = symbol_data.name
    }
}

let win_filtros_variacion_semanal = {
    state:{
        filtros:{},
        nom_symbol:""
    }
}

let table_variacion_semanal = {
    state:{
        filtros:{
            cod_symbol: ""
        },
        nom_symbol: "",
        data: []
    },
    reset: function(){
        this.state.filtros.cod_symbol = ""
        this.state.nom_symbol = ""
        this.state.data = ""
    },
    set_filtros: function(params){
        let gestorObjeto = new GestorObjeto(this.state.filtros)
        gestorObjeto.set_campos(params)
    },
    set_properties: function(payload){
        let gestorObjeto = new GestorObjeto(this.state)
        gestorObjeto.set_campos(payload)
    },
    get_datos_variacion: async function(params){
        try{
            //antes que nada reseteamos los datos
            this.state.data = []
            
            //si no esta el cod_symbol fallar
            if (!("cod_symbol" in params)){
                return;
            }

            this.state.filtros.cod_symbol = params.cod_symbol


            let VariacionSemanalAPI = new VariacionSemanal()
            let data = await VariacionSemanalAPI.build(params)            
            for (let element of data){
                element.imp_cierre_ant = element.imp_cierre_ant.toFixed(2)
                element.imp_maximo = element.imp_maximo.toFixed(2)
                element.imp_minimo = element.imp_minimo.toFixed(2)
                element.imp_cierre = element.imp_cierre.toFixed(2)
                element.pct_variacion_cierre = element.pct_variacion_cierre.toFixed(2)
                element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(2)
                element.pct_variacion_maximo = element.pct_variacion_maximo.toFixed(2)
                element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(2)
                element.pct_variacion_minimo = element.pct_variacion_minimo.toFixed(2)
                element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(2)
                this.state.data.push(element)                    
            }
        }catch(err){
            store.dispatch("incluir_msg",err.message)
        }
    }
}

export default {
    win_filtros_variacion_semanal: win_filtros_variacion_semanal,
    table_variacion_semanal: table_variacion_semanal,     
    panel_evolucion_semanal: panel_evolucion_semanal   
}