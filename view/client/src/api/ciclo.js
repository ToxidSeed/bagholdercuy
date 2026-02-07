import {postconfig} from "@/common/request.js"
import axios from "axios"

export const CicloService = {
    get_ciclos_diarios: (params) => axios.post("/ciclo/CicloController/get_ciclos_diarios", params, postconfig()),
    get_variacion_ciclos_diarios: (params) => axios.post("/ciclo/CicloVariacionController/get_ciclos_diarios", params, postconfig())
}