import axios from "axios"
import { postconfig } from "@/common/request.js"

const BASE_PATH = "/api/v2/simulacion-estrategias"

export default {
  listar() {
    return axios.get(BASE_PATH, postconfig())
  },

  guardar(payload) {
    return axios.post(BASE_PATH, payload, postconfig())
  },

  eliminar(idSimulacionEstrategia) {
    return axios.delete(`${BASE_PATH}/${idSimulacionEstrategia}`, postconfig())
  }
}
