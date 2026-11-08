import {postconfig} from "@/common/request.js"
import axios from "axios"
import store from "@/store/store"

class Cotizacion {
    get_cotizacion = async function (cod_symbol, provider = "ibkr") {
        try {
            const httpresp = await axios.get(
                "/api/v2/cotizaciones",
                {
                    ...postconfig(),
                    params: {
                        cod_symbol: cod_symbol,
                        provider: provider,
                    },
                }
            )
            store.dispatch("incluir_httpresp_si_apperror", httpresp)
            return httpresp.data.data
        } catch (err) {
            console.log(err)
        }
    }

    get_cotizaciones = async function (params = {}) {
        try {
            const queryParams = {
                provider: params.provider || "ibkr"
            }
            if (params.id_symbol) {
                queryParams.id_symbol = Array.isArray(params.id_symbol)
                    ? params.id_symbol.join(",")
                    : params.id_symbol
            }
            if (params.id_contrato_opcion && params.id_contrato_opcion.length !== 0) {
                queryParams.id_contrato_opcion = Array.isArray(params.id_contrato_opcion)
                    ? params.id_contrato_opcion.join(",")
                    : params.id_contrato_opcion
            }
            if (params.conid && (!Array.isArray(params.conid) || params.conid.length > 0)) {
                queryParams.conid = Array.isArray(params.conid)
                    ? params.conid.join(",")
                    : params.conid
            }
            if (params.cod_symbol && (!Array.isArray(params.cod_symbol) || params.cod_symbol.length > 0)) {
                queryParams.cod_symbol = Array.isArray(params.cod_symbol)
                    ? params.cod_symbol.join(",")
                    : params.cod_symbol
            }

            const httpresp = await axios.get(
                "/api/v2/cotizaciones",
                {
                    ...postconfig(),
                    params: queryParams,
                }
            )
            store.dispatch("incluir_httpresp_si_apperror", httpresp)
            return httpresp.data.data || []
        } catch (err) {
            console.log(err)
            return []
        }
    }
}

export default new Cotizacion()
