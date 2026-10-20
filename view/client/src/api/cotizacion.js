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
                queryParams.id_symbol = params.id_symbol
            }
            if (params.id_contrato_opcion) {
                queryParams.id_contrato_opcion = params.id_contrato_opcion
            }
            if (params.cod_symbol) {
                queryParams.cod_symbol = params.cod_symbol
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