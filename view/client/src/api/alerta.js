import {postconfig} from "@/common/request.js"
import axios from "axios"
import store from "@/store/store"

class Alerta{        
    get_alertas_x_configuracion = async function(params){        
        try{
            let httpresp = await axios.post("/alerta/AlertaController/get_alertas_x_configuracion",{
                id_config_alerta: params.id_config_alerta
            },postconfig())
            store.dispatch("incluir_httpresp_si_apperror", httpresp)
            return httpresp.data.data
        }catch(err){
            console.log(err)
        }
    }    
}

export default new Alerta()