import { postconfig } from "@/common/request.js"
import axios from "axios"

class ContratoOpcion {
    get_cadena_de_opciones = function (params) {
        return axios.post("/contrato_opcion/ContratoOpcionController/get_options_chain", params, postconfig())
    }
}

export default ContratoOpcion