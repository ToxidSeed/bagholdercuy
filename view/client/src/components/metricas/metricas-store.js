import Metrica from "@/api/metrica"
import { HttpResponseHandler } from "../../common/http-response-handler"
//import GestorObjeto from "../../common/gestor-objeto"
import store from "@/store/store"

import { HttpError } from "../../common/custom-error"
//import { HttpError } from "../../common/custom-error"
import _ from "lodash"


let win_criterios_metricas_diaria = {
    open: false,
    cod_symbol: "",
    nom_symbol: "",
    cod_tipo_periodo: 1,
    nom_tipo_periodo:"",
    fch_desde:"",
    fch_hasta:"",
    opciones_tipos_periodos:[
        {
            codigo: 1,
            nombre: "Rango de fechas"
        },{
            codigo: 2,
            nombre: "Ultimos 100 dias"
        },{
            codigo: 3,
            nombre: "ultimos 365 dias"
        },{
            codigo: 4,
            nombre: "Año en curso"
        }
    ],
    defaults: function(){
        this.defaults_tipo_periodo()
    },
    defaults_tipo_periodo: function(){
        let opcion = _.find(this.opciones_tipos_periodos, elem => elem.codigo = this.cod_tipo_periodo)
        this.cod_tipo_periodo = opcion.codigo
        this.nom_tipo_periodo = opcion.nombre            
    }
}

let win_criterios_metricas_semanal = {
    open: false, 
    cod_symbol: "",
    nom_symbol: "",
    cod_tipo_periodo: 1,
    nom_tipo_periodo: "",
    nom_semana_inicial: "",
    nom_semana_final: "",
    opciones_tipos_periodo: [
        {
            codigo: 1,
            nombre: "Rango de semanas"
        }
    ],
    defaults: function(){
        this.defaults_tipo_periodo()
    },
    defaults_tipo_periodo: function(){
        let opcion = _.find(this.opciones_tipos_periodo, elem => elem.codigo = this.cod_tipo_periodo)        
        this.cod_tipo_periodo = opcion.codigo
        this.nom_tipo_periodo = opcion.nombre        
    }
}

let win_criterios_metricas = {
    open:false,
    cod_symbol:"",
    nom_symbol:"",
    cod_tipo_periodo:1,
    nom_tipo_periodo:"",
    cod_tipo_periodo_met_semanal:1,
    nom_tipo_periodo_met_semanal:"",
    cod_tipo_periodo_met_mensual:1,
    nom_tipo_periodo_met_mensual:"",
    num_semana_desde:"",
    num_semana_hasta:"",
    num_mes_desde:"",
    num_mes_hasta:"",
    fch_desde:"",
    fch_hasta:"",
    opciones_periodo:[
        {
            codigo: 1,
            nombre: "Rango de fechas"
        },{
            codigo: 2,
            nombre: "Ultimos 100 dias"
        },{
            codigo: 3,
            nombre: "ultimos 365 dias"
        },{
            codigo: 4,
            nombre: "Año en curso"
        }
    ],   
    tipos_periodo_met_semanal:[
        {
            codigo:1,
            nombre:"Rango de fechas"
        },{
            codigo:2,
            nombre:"Rango de Semanas"
        },{
            codigo:3,
            nombre:"Ultimas 4 semanas"
        },{
            codigo:4,
            nombre:"Ultimas 52 semanas"
        },{
            codigo:5,
            nombre:"Año en curso"
        }
    ],   
    tipos_periodo_met_mensual:[
        {
            codigo:1,
            nombre:"Rango de fechas"
        },{
            codigo:2,
            nombre:"Rango de meses"
        },{
            codigo:3,
            nombre:"Ultimos 12 meses"
        },{
            codigo:4,
            nombre:"Ultimos 24 meses"
        },{
            codigo:5,
            nombre:"Ultimos 36 meses"
        }
    ],
    defaults: function(){
        this.defaults_tipo_periodo_diario()
        this.defaults_tipo_periodo_semanal()
        this.defaults_tipo_periodo_mensual()
    },
    defaults_tipo_periodo_diario: function(def=1){
        let opcion = _.find(this.opciones_periodo, (elem) => { return elem.codigo == def;})
        console.log(opcion)
        const {codigo, nombre} = opcion
        this.cod_tipo_periodo = codigo
        this.nom_tipo_periodo = nombre
    },
    defaults_tipo_periodo_semanal: function(def=2){        
        let opcion = _.find(this.tipos_periodo_met_semanal, (elem) => { return elem.codigo == def;})
        console.log(opcion)
        const {codigo, nombre} = opcion
        this.cod_tipo_periodo_met_semanal = codigo
        this.nom_tipo_periodo_met_semanal = nombre
    }
    ,
    defaults_tipo_periodo_mensual: function(def=2){        
        let opcion = _.find(this.tipos_periodo_met_mensual, (elem) => { return elem.codigo == def;})
        console.log(opcion)
        const {codigo, nombre} = opcion
        this.cod_tipo_periodo_met_mensual = codigo
        this.nom_tipo_periodo_met_mensual = nombre
    }
}

let table_metricas_var_positiva = {
    data: [],
    total: 0,
    count: 0
}
let table_metricas_semanal_var_positiva = {
    data: [],
    total: 0,
    count: 0
}

let table_metricas_var_negativa = {
    data:[],
    total: 0,
    count:0
}

let table_metricas_semanal_var_negativa = {
    data:[],
    total: 0,
    count:0
}

let table_metricas_mensual_var_positiva = {
    data:[],
    total: 0,
    count:0   
}

let table_metricas_mensual_var_negativa = {
    data:[],
    total: 0,
    count:0   
}

let panel_metricas = {
    cod_symbol:"",
    nom_symbol:"",
    fch_desde:"",
    fch_hasta:""
}

let metricas = {    
    state:{
        table_metricas_var_positiva: table_metricas_var_positiva,
        table_metricas_var_negativa: table_metricas_var_negativa,
        table_metricas_semanal_var_positiva: table_metricas_semanal_var_positiva,
        table_metricas_semanal_var_negativa: table_metricas_semanal_var_negativa,
        table_metricas_mensual_var_positiva: table_metricas_mensual_var_positiva,
        table_metricas_mensual_var_negativa: table_metricas_mensual_var_negativa,
        win_criterios_metricas: win_criterios_metricas,
        win_criterios_metricas_diaria: win_criterios_metricas_diaria,
        win_criterios_metricas_semanal: win_criterios_metricas_semanal,
        panel_metricas: panel_metricas
    }
    /*get_metricas_diarias_de_cierres_positivos: async function(params){
        try{

            let metrica_api = new Metrica()
            let response = metrica_api.get_metricas_diarias_de_cierres_positivos(params)
            response.then(httpresp => {
                try{
                    HttpResponseHandler.throwIfError(httpresp)

                    let data = httpresp.data.data                                  
                    
                    for (let element of data){                    
                        element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(3)                    
                        element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(3)
                        element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(3)
                        element.imp_variacion_maximo_minimo = element.imp_variacion_maximo_minimo.toFixed(3)
                    }
                    
                    this.state.table_metricas_var_positiva.data = data
                    this.state.table_metricas_var_positiva.count = data.count                
                    this.state.table_metricas_var_positiva.total = data.total

                }catch(err){
                    if (err instanceof HttpError){
                        store.dispatch("incluir_httpresp", err.httpresponse)
                    }
                }
            })

        }catch(err){
            console.log(err)
        }
    }*/,
    get_metricas_diarias_de_cierres_negativos: async function(params){
        try{

            let metrica_api = new Metrica()
            let response = metrica_api.get_metricas_diarias_de_cierres_negativos(params)
            response.then(httpresp => {
                try{
                    HttpResponseHandler.throwIfError(httpresp)

                    let data = httpresp.data.data                                  
                    
                    for (let element of data){                    
                        element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(3)                    
                        element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(3)
                        element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(3)
                        element.imp_variacion_maximo_minimo = element.imp_variacion_maximo_minimo.toFixed(3)
                    }
                    
                    this.state.table_metricas_var_negativa.data = data
                    this.state.table_metricas_var_negativa.count = data.count                
                    this.state.table_metricas_var_negativa.total = data.total

                }catch(err){
                    if (err instanceof HttpError){
                        store.dispatch("incluir_httpresp", err.httpresponse)
                    }
                }
            })

        }catch(err){
            console.log(err)
        }
    },
    get_metricas_semanales_de_cierres_positivos: async function(params){
        try{
            let metrica_api = new Metrica()
            let response = metrica_api.get_metricas_semanales_de_cierres_positivos(params)
            response.then(httpresp => {
                try{
                    HttpResponseHandler.throwIfError(httpresp)
                    let data = httpresp.data.data

                    for (let element of data){
                        element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(3)
                        element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(3)
                        element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(3)
                        //element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(3)
                    }
                    this.state.table_metricas_semanal_var_positiva.data = data    
                    console.log(this.table_metricas_semanal_var_positiva)                
                }catch(err){                    
                    if (err instanceof HttpError){
                        store.dispatch("incluir_httpresp", err.httpresponse)
                    }
                    console.log(err)
                }
            })
        }catch(err){
            if (err instanceof HttpError){
                store.dispatch("incluir_httpresp", err.httpresponse)
            }
        }
    },
    get_metricas_semanales_de_cierres_negativos: async function(params){
        try{
            let metrica_api = new Metrica()
            let response = metrica_api.get_metricas_semanales_de_cierres_negativos(params)
            response.then(httpresp => {
                try{
                    HttpResponseHandler.throwIfError(httpresp)
                    let data = httpresp.data.data

                    for (let element of data){
                        element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(3)
                        element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(3)
                        element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(3)
                    }
                    this.state.table_metricas_semanal_var_negativa.data = data    
                }catch(err){
                    if (err instanceof HttpError){
                        store.dispatch("incluir_httpresp", err.httpresponse)
                    }
                    console.log(err)
                }
            })
        }catch(err){
            if (err instanceof HttpError){
                store.dispatch("incluir_httpresp", err.httpresponse)
            }
        }
    }
}

export default metricas