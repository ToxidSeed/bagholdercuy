import {postconfig} from "@/common/request.js"
import axios from "axios"
import store from "@/store/store"
import { HttpError } from "../common/custom-error"

class Serie{

    get_estadisticas = async function(params){
        const httpresp = axios.post("/SerieManager/SerieController/get_estadisticas",
            params,
            postconfig()
        )

        return httpresp
    }

    actualizar_serie = async function(data){        
        let httpresp = await axios.post("/SerieManager/SerieManagerLoader/actualizar_serie",{
            cod_symbol: data.cod_symbol
        }, postconfig())        

        if (httpresp.data.success == false){
            throw new HttpError(httpresp.data.message, httpresp)
        }
        //store.dispatch("incluir_httpresp_si_apperror", httpresp)
        return httpresp.data                
    }

    reparar = async function(data){
        let httpresp = await axios.post("/SerieManager/ReparadorSeriesController/reparar",{
            cod_symbol: data.cod_symbol
        }, postconfig())        
        return httpresp
    }

    get_lista_fechas_maximas_x_symbol = async function(){
        try{
            let httpresp = await axios.post("/SerieManager/SerieController/get_lista_fechas_maximas_x_symbol",{                
            },postconfig())
            store.dispatch("incluir_httpresp_si_apperror", httpresp)
            return httpresp.data.data
        }catch(err){
            console.log(err)
        }
    }    
}

export default Serie