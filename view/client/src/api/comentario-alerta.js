import {postconfig} from "@/common/request.js"
import axios from "axios"
import store from "@/store/store"

class ComentarioAlerta{
    registrar = async function(params){        
        try{
            const httpresp = await axios.post("/comentarioalerta/ComentarioAlertaController/registrar",
            params
            ,postconfig())

            store.dispatch("incluir_httpresp", httpresp)                 
        }catch(err){
            console.log(err)
        }
    }

    get_comentarios_x_alerta = async function(params){
        try{
            const httpresp = await axios.post("/comentarioalerta/ComentarioAlertaController/get_comentarios_x_alerta",
            params
            ,postconfig())

            store.dispatch("incluir_httpresp_si_apperror", httpresp)                 
            return httpresp.data.data
        }catch(err){
            console.log(err)
        }
    }

    eliminar = async function(id_comentario_alerta){
        if (id_comentario_alerta == undefined || id_comentario_alerta == ""){
            store.dispatch("incluir_msg","No se ha indicado id_comentario_alerta")
            return
        }

        let params = {
            id_comentario_alerta: id_comentario_alerta
        }

        try{
            const httpresp = await axios.post("/comentarioalerta/ComentarioAlertaController/eliminar",params
            ,postconfig()
            )
            store.dispatch("incluir_httpresp", httpresp)                 
        }catch(err){
            console.log(err)
        }
    }
}

export default new ComentarioAlerta()