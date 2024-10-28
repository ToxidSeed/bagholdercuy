import {postconfig} from "@/common/request.js"
import axios from "axios"

class Metrica{
    get_variaciones_x_symbol = function(params){
        return axios.post("/metrica/MetricaController/get_variaciones_x_symbol",params,postconfig())
    }
    get_metricas_diarias_de_cierres_positivos = function(params){
        return axios.post("/metrica/MetricaController/get_metricas_diarias_de_cierres_positivos", params, postconfig())
    }
    get_metricas_diarias_de_cierres_negativos = function(params){
        return axios.post("/metrica/MetricaController/get_metricas_diarias_de_cierres_negativos", params, postconfig())
    }
    get_metricas_semanales_de_cierres_positivos = function(params){
        return axios.post("/metrica/MetricaController/get_metricas_semanales_de_cierres_positivos", params, postconfig())
    }
    get_metricas_semanales_de_cierres_negativos = function(params){
        return axios.post("/metrica/MetricaController/get_metricas_semanales_de_cierres_negativos", params, postconfig())
    }
    get_metricas_mensuales_de_cierres_positivos = function(params){
        return axios.post("/metrica/MetricaController/get_metricas_mensuales_de_cierres_positivos", params, postconfig())
    }
    get_metricas_mensuales_de_cierres_negativos = function(params){
        return axios.post("/metrica/MetricaController/get_metricas_mensuales_de_cierres_negativos", params, postconfig())
    }
}

export default Metrica;