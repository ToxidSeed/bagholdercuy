import {postconfig} from "@/common/request.js"
import axios from "axios"
import store from "@/store/store"
import { HttpError } from "../common/custom-error"

class Serie{
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