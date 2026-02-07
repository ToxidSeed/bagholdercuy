import {postconfig} from "@/common/request.js"
import axios from "axios"

class OpcionesContrato{
    get_cadena_de_opciones = function(params){
        return axios.post("/OpcionesContrato/OpcionesContratoManager/get_options_chain", params, postconfig())
    }
}

export default OpcionesContrato