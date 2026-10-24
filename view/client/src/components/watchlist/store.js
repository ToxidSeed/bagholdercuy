import Monitoreo from "@/api/monitoreo"
import Cotizacion from "@/api/cotizacion"
import Vue from 'vue'

let table_monitoreo = {
    state:{
        params:{},
        monitoreo_activo_data:[]
    },
    get_monitoreo_activo: async function(params){                  
        if (params == undefined){
            this.state.params = {}
        }else{
            this.state.params = params
        }
        
        this.state.monitoreo_activo_data = await new Monitoreo().get_monitoreo_activo(
            this.state.params 
        )       
        this.aplicar_cotizacion()                 
    },
    refresh: async function(){
        this.state.monitoreo_activo_data = await new Monitoreo().get_monitoreo_activo(
            this.state.params 
        )       
        this.aplicar_cotizacion()                 
    },
    eliminar: async function(id_monitoreo){
        await new Monitoreo().eliminar(id_monitoreo)
        this.state.monitoreo_activo_data = this.state.monitoreo_activo_data.filter(
            item => item.id_monitoreo !== id_monitoreo
        )
    },
    aplicar_cotizacion: async function () {
        if (!Array.isArray(this.state.monitoreo_activo_data) || this.state.monitoreo_activo_data.length === 0) {
            return
        }

        const symbolIds = []
        const optionIds = []
        const fallbackSymbols = []

        this.state.monitoreo_activo_data.forEach(element => {
            if (element.id_symbol) {
                symbolIds.push(element.id_symbol)
            } else if (element.id_contrato_opcion) {
                optionIds.push(element.id_contrato_opcion)
            } else if (element.cod_symbol) {
                fallbackSymbols.push(element.cod_symbol)
            }
        })

        if (symbolIds.length === 0 && optionIds.length === 0 && fallbackSymbols.length === 0) {
            return
        }

        const cotizaciones = await Cotizacion.get_cotizaciones({
            id_symbol: symbolIds.length > 0 ? symbolIds.join(",") : undefined,
            id_contrato_opcion: optionIds.length > 0 ? optionIds.join(",") : undefined,
            cod_symbol: fallbackSymbols.length > 0 ? fallbackSymbols.join(",") : undefined,
        })

        if (!Array.isArray(cotizaciones)) {
            return
        }

        const quoteMapSymbol = new Map()
        const quoteMapOption = new Map()
        const quoteMapCode = new Map()

        cotizaciones.forEach(quote => {
            if (quote.id_symbol) {
                quoteMapSymbol.set(Number(quote.id_symbol), quote)
            }
            if (quote.id_contrato_opcion) {
                quoteMapOption.set(Number(quote.id_contrato_opcion), quote)
            }
            if (quote.cod_symbol) {
                quoteMapCode.set(String(quote.cod_symbol).toUpperCase(), quote)
            }
        })

        this.state.monitoreo_activo_data.forEach(element => {
            let cotizacion = null
            if (element.id_symbol && quoteMapSymbol.has(Number(element.id_symbol))) {
                cotizacion = quoteMapSymbol.get(Number(element.id_symbol))
            } else if (element.id_contrato_opcion && quoteMapOption.has(Number(element.id_contrato_opcion))) {
                cotizacion = quoteMapOption.get(Number(element.id_contrato_opcion))
            } else if (element.cod_symbol && quoteMapCode.has(String(element.cod_symbol).toUpperCase())) {
                cotizacion = quoteMapCode.get(String(element.cod_symbol).toUpperCase())
            }

            if (cotizacion) {
                Vue.set(element, 'imp_actual', cotizacion.imp_cierre)
                Vue.set(element, 'imp_cierre_anterior', cotizacion.imp_cierre_anterior)
                if (cotizacion.imp_variacion !== undefined) {
                    Vue.set(element, 'imp_variacion', cotizacion.imp_variacion)
                }
                if (cotizacion.pct_variacion !== undefined) {
                    Vue.set(element, 'pct_variacion', cotizacion.pct_variacion)
                }
            }
        })
    }
}

let panel_watchlist = {
    state:{},
    registrar: async function(params){
        return await new Monitoreo().registrar(params)
    }
}

export default {
    table_monitoreo: table_monitoreo,
    panel_watchlist: panel_watchlist
}