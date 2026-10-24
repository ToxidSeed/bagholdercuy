import { postconfig } from "@/common/request.js"
import axios from "axios"
import store from "@/store/store"

class Monitoreo {
    get_monitoreo_activo = async function(params = {}) {
        try {
            params.id_cuenta = localStorage.getItem("id_cuenta")

            const httpresp = await axios.get(
                "/api/v2/monitoreos",
                { ...postconfig(), params }
            )
            store.dispatch("incluir_httpresp_si_apperror", httpresp)
            return httpresp.data.data
        } catch (err) {
            console.error(err)
            return []
        }
    }

    registrar = async function(params = {}) {
        try {
            params.id_cuenta = localStorage.getItem("id_cuenta")

            const httpresp = await axios.post(
                "/api/v2/monitoreos",
                params,
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

    eliminar = async function(id_monitoreo) {
        try {
            const httpresp = await axios.delete(
                `/api/v2/monitoreos/${id_monitoreo}`,
                postconfig()
            )
            store.dispatch("incluir_httpresp", httpresp)
            return httpresp.data
        } catch (err) {
            console.error(err)
            if (err.response) {
                store.dispatch("incluir_httpresp", err.response)
            }
            throw err
        }
    }
}

export default Monitoreo