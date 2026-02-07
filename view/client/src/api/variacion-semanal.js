import {postconfig} from "@/common/request.js"
import axios from "axios"
//import store from "@/store/store"

class VariacionSemanal{
    build = async function(params){        
        if (!("cod_symbol" in params)){
            throw new Error("No se ha enviado 'cod_symbol' a la peticion")
        }

        let httresp = await axios.post(
            '/reportes/VariacionSemanalBuilder/build',{
                symbol: params.cod_symbol
            },
            postconfig()
        )

        return httresp.data.data                
    }

    get_variacion_semana_actual = async function(params){
        if (params == undefined){
            throw new Error("No se ha enviado ningun parametro")
        }

        return axios.post(
            '/variacionsemanal/VariacionSemanalController/get_variacion_semana_actual',params,
            postconfig()
        )
    }
}

export default VariacionSemanal