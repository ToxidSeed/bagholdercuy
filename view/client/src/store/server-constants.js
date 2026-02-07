import * as ServerConstantsApi from '../api/server-constants'

export default {
    namespaced: true,
    state: {
        tiposTransaccion:null,
        instrumentosFinancieros:null
    },
    mutations: {
        SET_TIPOS_TRANSACCION(state, records){
            state.tiposTransaccion = records
        },
        SET_INSTRUMENTOS_FINANCIEROS(state, records){
            state.instrumentosFinancieros = records
        }
    },
    actions: {
        async getList({commit}){
            const httpresp = await ServerConstantsApi.getList()
            const httpdata = httpresp.data
            const data = httpdata.data            
            commit('SET_TIPOS_TRANSACCION', data.tiposTransaccion)
            commit('SET_INSTRUMENTOS_FINANCIEROS', data.instrumentosFinancieros)            
        }
    }
}