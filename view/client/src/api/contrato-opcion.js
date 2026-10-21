import { postconfig } from "@/common/request.js"
import axios from "axios"
import store from "@/store/store"

class ContratoOpcion {
    get_cadena_de_opciones = async function (params) {
        return axios.post("/api/v2/contratos-opcion/chain", params, postconfig())
    }

    get_contratos = async function (params = {}) {
        try {
            const httpresp = await axios.get(
                "/api/v2/contratos-opcion",
                { ...postconfig(), params }
            )
            store.dispatch("incluir_httpresp_si_apperror", httpresp)
            return httpresp.data.data
        } catch (err) {
            console.error(err)
            return []
        }
    }

    get_contrato = async function (id_contrato_opcion) {
        try {
            const httpresp = await axios.get(
                `/api/v2/contratos-opcion/${id_contrato_opcion}`,
                postconfig()
            )
            store.dispatch("incluir_httpresp_si_apperror", httpresp)
            return httpresp.data.data
        } catch (err) {
            console.error(err)
            throw err
        }
    }

    guardar = async function (data = {}) {
        try {
            const httpresp = await axios.post(
                "/api/v2/contratos-opcion",
                data,
                postconfig()
            )
            store.dispatch("incluir_httpresp", httpresp)
            return httpresp.data.data
        } catch (err) {
            console.error(err)
            if (err.response) {
                store.dispatch("incluir_httpresp", err.response)
            }
            throw err
        }
    }

    get_resumen_subyacentes = async function () {
        try {
            const httpresp = await axios.get(
                "/api/v2/contratos-opcion/resumen-subyacentes",
                postconfig()
            )
            store.dispatch("incluir_httpresp_si_apperror", httpresp)
            return httpresp.data.data
        } catch (err) {
            console.error(err)
            return []
        }
    }
}

export default ContratoOpcion