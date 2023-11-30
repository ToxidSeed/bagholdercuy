import {postconfig} from "@/common/request.js"
import axios from "axios"
import store from "@/store/store"

class Cotizacion{        
    get_cotizacion = async function(cod_symbol){            
        try{
            const httpresp = await axios.post(
                "/cotizacion/CotizacionManager/get_cotizacion",{
                    cod_symbol: cod_symbol
                },
                postconfig()
            )            
            store.dispatch("incluir_httpresp_si_apperror", httpresp)
            return httpresp.data.data
        }catch(err){
            console.log(err)
        }
    }    
}

export default new Cotizacion()