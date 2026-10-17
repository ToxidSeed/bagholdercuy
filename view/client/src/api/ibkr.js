import { postconfig } from "@/common/request.js"
import axios from "axios"

class Ibkr {
    static sync_all_conids(params) {
        return axios.post(`/api/v2/ibkr/trsrv/load-all-conids`, params, postconfig())
    }
    static get_contracts(params) {
        return axios.get(`/api/v2/ibkr/trsrv/contracts`, { ...postconfig(), params })
    }
    static get_expiration_dates(params) {
        return axios.get(`/api/v2/ibkr/expiration-dates`, { ...postconfig(), params })
    }
    static get_strikes(params) {
        return axios.get(`/api/v2/ibkr/strikes`, { ...postconfig(), params })
    }
    static get_options_chain(params) {
        return axios.get(`/api/v2/ibkr/options-chain`, { ...postconfig(), params })
    }
}

export default Ibkr;
