import {SET_DATA} from "./mutation-types"

export default {
    namespaced:true,
    state:{
        
        data:[]
    },
    actions:{
        async get_data({commit}){
            const data = await this.$http.post("/")
            commit("SET_DATA", data)
        }
    },
    mutations:{
        [SET_DATA](state, data){
            state.data = data
        }
    }
}