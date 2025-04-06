import Serie from "@/api/serie"
import { HttpError } from "../../common/custom-error"
import {postconfig} from "@/common/request.js"
import store from "@/store/store"
import axios from "axios"
import resumenSerieApi from "../../api/resumenSerieApi"

export default {
    //table_resumen_serie: table_resumen_serie
    state:{
        t_resumen:{
            data:[]
        },
        w_reprocesar:{
            cod_symbol:"",
            open:false,
            fichero:null        
        },
        w_nasdaq_loader:{
            open:false
        }
    },
    actualizar_serie: async function(row){
        try{            
            let data = {
                cod_symbol: row.cod_symbol
            }                
            let response = await new Serie().actualizar_serie(data)
            console.log(response)  
        }catch(err){
            if (err instanceof HttpError){
                store.dispatch("incluir_httpresp", err.httpresponse)
            }
        }                
        this.get_resumen_serie()
    },
    get_resumen_serie: function(){        
        //this.state.t_resumen.data = await new Serie().get_lista_fechas_maximas_x_symbol()
        let resp = resumenSerieApi.get_resumen_serie()
        resp.then(httpresp => {
            console.log(httpresp)
            this.state.t_resumen.data = httpresp.data.data
        })
    },
    abrir_w_reprocesar: function(cod_symbol){
        this.state.w_reprocesar.cod_symbol = cod_symbol
        this.state.w_reprocesar.open = true
    },
    reprocesar_serie: function(){
        let form_data = new FormData();
        
        form_data.append("fichero", this.state.w_reprocesar.fichero)
        form_data.append("cod_symbol", this.state.w_reprocesar.cod_symbol)
        //form_data.append("id_cuenta", localStorage.getItem("id_cuenta"))

        axios.post("/SerieManager/ReprocesoSerieController/reprocesar"
            ,form_data
            ,postconfig()
        ).then(httpresponse => {
            console.log(httpresponse)
        })
    },
    abrir_w_nasdaq_loader: function(){
        console.log(this.state.w_nasdaq_loader.open)
        this.state.w_nasdaq_loader.open = true        
    }
}