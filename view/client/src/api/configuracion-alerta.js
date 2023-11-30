import {postconfig} from "@/common/request.js"
import axios from "axios"
import store from "@/store/store"

class ConfiguracionAlerta {
    async get_alerta(id_config_alerta){
        try{
            const httpresp = await axios.post("/configuracionalerta/ConfiguracionAlertaController/get_configuracion_alerta",{
                id_config_alerta: id_config_alerta
            },postconfig())
            store.dispatch("incluir_httpresp_si_apperror", httpresp)                 
            return httpresp.data.data
        }catch(err){
            console.log(err)
        }
    }

    async registrar(configuracion_alerta){        
        let params = Object.assign({}, configuracion_alerta) 
        params.id_cuenta = localStorage.getItem("id_cuenta")        
        
        if (params.id_config_alerta != ""){
            store.dispatch("incluir_msg", "No se debe enviar el id de configuracion de la alerta")
            return
        }

        try{
            const httpresp = await axios.post(
                "/configuracionalerta/ConfiguracionAlertaController/registrar",
                params,
                postconfig()
            )
            store.dispatch("incluir_httpresp", httpresp)
        }catch(err){
            console.log(err)
        }
    }

    async incluir_en_monitoreo(configuracion_alerta){
        let params = Object.assign({}, configuracion_alerta) 
        params.id_cuenta = localStorage.getItem("id_cuenta")        
        
        if (params.id_config_alerta != ""){
            store.dispatch("incluir_msg", "No se debe enviar el id de configuracion de la alerta")
            return
        }

        if (params.id_monitoreo == ""){
            store.dispatch("incluir_msg", "No se ha enviado el identificador del monitoreo")
        }

        try{
            const httpresp = await axios.post(
                "/configuracionalerta/ConfiguracionAlertaController/asociar_a_monitoreo",
                params,
                postconfig()
            )
            store.dispatch("incluir_httpresp", httpresp)
        }catch(err){
            console.log(err)
        }
    }

    async actualizar(configuracion_alerta){
        let params = Object.assign({}, configuracion_alerta) 
        params.id_cuenta = localStorage.getItem("id_cuenta")

        if (params.id_config_alerta == ""){
            store.dispatch("incluir_msg","No se ha enviado el id_config_alerta")
        }

        try{
            const httpresp = await axios.post(
                "/configuracionalerta/ConfiguracionAlertaController/actualizar",
                params,
                postconfig()
            )
            store.dispatch("incluir_httpresp", httpresp)
        }catch(err){
            console.log(err)
        }
    }
}

export default new ConfiguracionAlerta()