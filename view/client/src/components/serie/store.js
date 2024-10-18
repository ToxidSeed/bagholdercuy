import Serie from "@/api/serie"
import { HttpError } from "../../common/custom-error"
import {postconfig} from "@/common/request.js"
import store from "@/store/store"
import axios from "axios"

export default {
    //table_resumen_serie: table_resumen_serie
    state:{
        t_resumen:{
            data:[]
        },
        w_reparar:{
            cod_symbol:"",
            open:false,
            fichero:null        
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
    get_resumen_serie: async function(){        
        this.state.t_resumen.data = await new Serie().get_lista_fechas_maximas_x_symbol()
    },
    abrir_w_reparar: function(cod_symbol){
        this.state.w_reparar.cod_symbol = cod_symbol
        this.state.w_reparar.open = true
    },
    reparar_serie: function(){
        let form_data = new FormData();
        
        form_data.append("fichero", this.state.w_reparar.fichero)
        form_data.append("cod_symbol", this.state.w_reparar.cod_symbol)
        form_data.append("id_cuenta", localStorage.getItem("id_cuenta"))

        axios.post("/SerieManager/ReparadorSeriesController/reparar"
            ,form_data
            ,postconfig()
        ).then(httpresponse => {
            console.log(httpresponse)
        })
    }
}