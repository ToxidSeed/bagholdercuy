import {postconfig} from "@/common/request.js"
import axios from "axios"
import store from "@/store/store"

class Monitoreo{
    get_monitoreo_activo = async function(params){
        try{
            params.id_cuenta = localStorage.getItem("id_cuenta")
            
            const httpresp = await axios.post(
                "/monitoreo/MonitoreoController/get_monitoreo_activo",
                params,
                postconfig()
            )
            store.dispatch("incluir_httpresp_si_apperror", httpresp)
            return httpresp.data.data
        }catch(err){
            console.log(err)
        }
    }

    registrar = async function(params){
        try{
            params.id_cuenta = localStorage.getItem("id_cuenta")
            
            const httpresp = await axios.post(
                "/monitoreo/MonitoreoController/registrar",
                params,
                postconfig()
            )
            store.dispatch("incluir_httpresp", httpresp)
            return httpresp.data.data
        }catch(err){
            console.log(err)
        }
    }
}

export default Monitoreo