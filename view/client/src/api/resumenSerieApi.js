import {postconfig} from "@/common/request.js"
import axios from "axios"

export default {
    get_resumen_serie() {
        return axios.post("/resumenserie/ResumenSerie/get_resumen_serie",{}, postconfig())
    }
}