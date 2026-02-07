//import { HttpResponseHandler } from "../../common/http-response-handler"
//import store from "@/store/store"
//import { HttpError } from "../../common/custom-error"
//import _ from "lodash"
import {postconfig} from "@/common/request.js"
import axios from "axios"
import store from "@/store/store"

export default {
    state:{
        stock_split_data:[],
        panel_stock_split_loader:{
            symbol:{
                value:"",
                name:""
            }
        }
    },
    get_stock_split_data: function(){
        let params = {}
        axios.post(
            "/metrica/MetricaController/get_metricas_diarias_de_cierres_positivos", params, postconfig()
        ).then(httpresp => {
            console.log(httpresp)
        })
    },
    procesar: function(){
        let params = {
            cod_symbol:this.state.panel_stock_split_loader.symbol.value    
        }

        axios.post(
            "/stocksplit/FmpStockSplitController/load_stock_splits", params, postconfig()
        ).then(httpresp => {
            store.dispatch("incluir_httpresp", httpresp)                 
        }).catch(error => {
            console.log(error)
        })
    },
    sel_symbol_procesar:function(selected){    
        this.state.panel_stock_split_loader.symbol.value = selected.value
        this.state.panel_stock_split_loader.symbol.name = selected.label       
    }
}