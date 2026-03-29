import { postconfig } from "@/common/request.js"
import axios from "axios"
//import store from "@/store/store"
import { OPERACION } from "./endpoints"

class Operacion {
    cargar_operaciones_ibkr(archivo) {
        let url = OPERACION.IBKR_LOAD
        let config = postconfig()
        let data = new FormData()
        data.append("archivo", archivo)
        return axios.post(url, data, config)
    }

    get_ibkr_import_trades_detail(id_importacion) {
        let url = OPERACION.IBKR_LOAD_DETAIL
        let config = postconfig()
        return axios.post(url, { id_importacion }, config)
    }

    generar_transacciones(operaciones_importadas, id_importacion, id_cuenta) {
        let url = OPERACION.IBKR_GEN_TRANSACCIONES
        let config = postconfig()
        return axios.post(url, { operaciones_importadas, id_importacion, id_cuenta }, config)
    }
}

export default new Operacion()