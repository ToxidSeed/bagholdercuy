import { postconfig } from "@/common/request.js"
import axios from "axios"

const CONTROLLER_PATH = "/transaccion/TransaccionController"

class Transaccion {
    get_fechas_con_transacciones = function (params) {
        return axios.post(`${CONTROLLER_PATH}/get_fechas_con_transacciones`, params, postconfig())
    }

    get_transacciones_x_fecha = function (params) {
        return axios.post(`${CONTROLLER_PATH}/get_transacciones_x_fecha`, params, postconfig())
    }

    get_transacciones_x_symbol = function (params) {
        return axios.post(`${CONTROLLER_PATH}/get_transacciones_x_symbol`, params, postconfig())
    }

    get_max_fechas_agroupadas_x_symbol = function (params) {
        return axios.post(`/api/v2/transaccion/transaccion-agrupada-search`, params, postconfig())
    }
}

export default Transaccion;
