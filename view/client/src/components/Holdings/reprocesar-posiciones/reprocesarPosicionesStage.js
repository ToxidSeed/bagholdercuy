import Vue from 'vue'
import Transaccion from "@/api/transaccion"

export const state = Vue.observable({
    tablePosiciones: []
})

export const mutations = {}

export const actions = {
    async obtenerDatosTablePosiciones(params) {
        try {
            const transaccionApi = new Transaccion()
            const resp = await transaccionApi.get_max_fechas_agroupadas_x_symbol(params)
            const appData = resp.data
            state.tablePosiciones = appData.data
        } catch (err) {
            console.error(err)
        }
    }
}