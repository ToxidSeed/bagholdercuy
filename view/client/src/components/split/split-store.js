//import { HttpResponseHandler } from "../../common/http-response-handler"
//import store from "@/store/store"
//import { HttpError } from "../../common/custom-error"
//import _ from "lodash"
import {postconfig} from "@/common/request.js"
import axios from "axios"

let store = {
    state:{
        stock_split_data:[]
    },
    get_stock_split_data: function(){
        let params = {}
        axios.post(
            "/metrica/MetricaController/get_metricas_diarias_de_cierres_positivos", params, postconfig()
        ).then(httpresp => {
            console.log(httpresp)
        })
    }
}

export default store