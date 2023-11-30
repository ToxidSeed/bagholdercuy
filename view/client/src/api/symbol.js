import {postconfig} from "@/common/request.js"
import axios from "axios"
import store from "@/store/store"

class Symbol{        
    get_symbol = async function(id_symbol){        
        try{
            let httpresp = await axios.post("/SymbolManager/SymbolFinder/get",{
                id_symbol: id_symbol
            },postconfig())
            store.dispatch("incluir_httpresp_si_apperror", httpresp)
            return httpresp.data.data
        }catch(err){
            console.log(err)
        }
    }    
}

export default new Symbol()