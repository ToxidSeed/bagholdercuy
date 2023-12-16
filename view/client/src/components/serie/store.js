import Serie from "@/api/serie"
import { HttpError } from "../../common/custom-error"
import store from "@/store/store"

let table_resumen_serie = {
    state:{
        row:{},
        data:[]
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
        console.log("get_resumen_serie")
        this.state.data = await new Serie().get_lista_fechas_maximas_x_symbol()
    }
}

export default {
    table_resumen_serie: table_resumen_serie
}