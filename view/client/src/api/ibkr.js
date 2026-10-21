import { postconfig } from "@/common/request.js"
import axios from "axios"

class Ibkr {
    sync_all_conids = function (params) {
        return axios.post(`/api/v2/ibkr/contracts`, params, postconfig())
    }

    get_contracts = function (params) {
        return axios.get(`/api/v2/ibkr/contracts`, { params: params, ...postconfig() })
    }
}

export default Ibkr;
