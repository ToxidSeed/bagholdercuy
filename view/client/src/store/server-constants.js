import * as ServerConstantsApi from '../api/server-constants'

export default {
    namespaced: true,
    state: {
        tiposTransaccion:null,
        symbolTypes:null
    },
    mutations: {
        SET_TIPOS_TRANSACCION(state, records){
            state.tiposTransaccion = records
        },
        SET_SYMBOL_TYPES(state, records){
            state.symbolTypes = records
        }
    },
    actions: {
        async getList({commit}){
            const httpresp = await ServerConstantsApi.getList()
            const httpdata = httpresp.data
            const data = httpdata.data            
            commit('SET_TIPOS_TRANSACCION', data.tiposTransaccion)
            commit('SET_SYMBOL_TYPES', data.symbolTypes)            
        }
    }
}