import { postconfig } from "@/common/request.js"
import axios from "axios"

class Ibkr {
    sync_all_conids = function (params) {
        return axios.post(`/api/v2/ibkr/trsrv/load-all-conids`, params, postconfig())
    }
}

export default Ibkr;
