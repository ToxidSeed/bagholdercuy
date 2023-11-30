import {SET_MODEL} from "./mutation-types"
import axios from 'axios'
import {postconfig} from "@/common/request.js"

export default {
    namespaced:true,
    state:{
        model:{

        }
    },
    actions:{
        async get(context, payload){
            if (payload.id_symbol == "" || payload.id_symbol == undefined){
                const httpresp = await axios.post("/SymbolManager/SymbolFinder/get",{
                    id_symbol: payload.id_symbol
                },postconfig())               

                context.commit("message",{"httpresp":httpresp, "mostrar_si_error":true},{root:true})            
                let data = httpresp.data.data
                context.commit("SET_MODEL", data)                
            }
        }
    },
    mutations:{
        [SET_MODEL](state, payload){
            state.model.id = payload.id
        }
    }
}