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
        
        /*.then(httpresp => {
            let appresp = httpresp.data
            this.data = []
            
            appresp.data.forEach(element => {
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
                this.data.push(element)                    
            })
        })*/
    }
}

export default VariacionSemanal