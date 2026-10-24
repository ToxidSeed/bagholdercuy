<template>
    <div>
        <q-dialog v-model="open" persistent>
            <q-card style="width: 480px; max-width: 95vw;">
                <q-toolbar class="text-blue-10 q-px-md q-pt-sm">
                    <q-toolbar-title class="text-subtitle1 text-weight-bold">
                        {{ titulo_dialogo }}
                    </q-toolbar-title>
                    <q-btn icon="close" flat round dense v-close-popup :disable="loading" />
                </q-toolbar>
                <q-separator />

                <q-card-section class="q-pt-md q-gutter-y-sm">
                    <!-- Selector de Proveedor -->
                    <div>
                        <q-select 
                            color="blue-10" 
                            v-model="proveedor" 
                            dense 
                            :options="lista_proveedores"
                            label="Proveedor de Datos" 
                            outlined 
                            stack-label 
                            emit-value 
                            map-options
                        />
                    </div>

                    <!-- Indicador o Buscador de Símbolo -->
                    <div v-if="inCodSymbol" class="q-pa-sm bg-blue-1 rounded-borders row items-center justify-between">
                        <div class="row items-center no-wrap">
                            <q-icon name="show_chart" color="primary" size="sm" class="q-mr-xs" />
                            <div>
                                <span class="text-subtitle1 text-weight-bolder text-primary">{{ cod_symbol }}</span>
                                <span v-if="nom_symbol" class="text-caption text-grey-8 q-ml-xs">- {{ nom_symbol }}</span>
                            </div>
                        </div>
                        <q-badge color="primary" label="Fijo" />
                    </div>
                    <div v-else>
                        <SelectSymbol @select-symbol="select_symbol" @clear-symbol="clear_symbol" />
                        <div v-if="cod_symbol" class="q-mt-xs text-caption text-primary text-weight-bold">
                            <q-icon name="check_circle" size="14px" class="q-mr-xs" />
                            Seleccionado: {{ cod_symbol }} <span v-if="nom_symbol" class="text-grey-7 text-weight-regular">({{ nom_symbol }})</span>
                        </div>
                    </div>

                    <!-- Proveedor de Archivo CSV -->
                    <template v-if="is_file_provider">
                        <q-file
                            v-model="fichero"
                            label="Seleccionar archivo .csv"
                            accept=".csv"
                            outlined
                            dense
                            color="blue-10"
                            stack-label
                            clearable
                        >
                            <template v-slot:prepend>
                                <q-icon name="attach_file" />
                            </template>
                        </q-file>

                        <q-select 
                            color="blue-10" 
                            v-model="modo_carga" 
                            dense 
                            outlined
                            :options="['Append', 'Replace']" 
                            label="Modo de Carga" 
                            stack-label 
                        />
                    </template>

                    <!-- Proveedor de API -->
                    <template v-else>
                        <div class="row items-center justify-between no-wrap q-pt-xs">
                            <span class="text-caption text-grey-8 text-weight-medium">Rango de fechas:</span>
                            <q-btn icon="event" flat color="blue-10" :label="rango_seleccionado.nombre" no-caps dense size="sm">
                                <q-menu>
                                    <q-list dense style="min-width: 150px">
                                        <q-item clickable v-close-popup class="text-body2" v-for="item in rangos_fechas"
                                            :key="item.codigo" @click="sel_rango(item.codigo)">
                                            <q-item-section>
                                                {{ item.nombre }}
                                            </q-item-section>
                                        </q-item>
                                    </q-list>
                                </q-menu>
                            </q-btn>
                        </div>

                        <div class="row q-gutter-x-sm">
                            <q-input label="Fecha Desde" stack-label color="blue-10" dense outlined placeholder="dd/mm/yyyy"
                                mask="##/##/####" v-model="fch_desde" class="col" />
                            <q-input label="Fecha Hasta" stack-label color="blue-10" dense outlined placeholder="dd/mm/yyyy"
                                mask="##/##/####" v-model="fch_hasta" class="col" />
                        </div>

                        <q-select 
                            color="blue-10" 
                            v-model="modo_carga" 
                            dense 
                            outlined 
                            :options="lista_modos_carga"
                            label="Modo de Escritura" 
                            stack-label 
                        />
                    </template>
                </q-card-section>

                <q-inner-loading :showing="loading">
                    <q-spinner-gears size="50px" color="primary" />
                </q-inner-loading>

                <q-separator />

                <q-card-actions align="right" class="q-pa-md">
                    <q-btn flat v-close-popup no-caps label="Cancelar" color="grey-7" :disable="loading" />
                    <q-btn 
                        unelevated 
                        @click="procesar" 
                        no-caps 
                        color="primary" 
                        icon="sync" 
                        label="Sincronizar" 
                        :loading="loading" 
                    />
                </q-card-actions>
            </q-card>
        </q-dialog>
    </div>
</template>
<script>
import SelectSymbol from "@/components/SelectSymbol.vue"
import date from 'date-and-time'
import Serie from "@/api/serie.js"
import store from "@/store/store.js"
import serieStore from "./store.js"
import axios from "axios"
import { postconfig, get_postconfig } from "@/common/request.js"

export default {
    name: "WinSincronizarSeries",
    props: {
        value: {
            required: true
        },
        inCodSymbol: {
            type: String,
            default: ""
        }
    },
    components: {
        SelectSymbol
    },
    computed: {
        is_file_provider() {
            return this.proveedor === "CSV_NASDAQ" || this.proveedor === "CSV_INVESTING"
        },
        titulo_dialogo() {
            if (this.inCodSymbol) {
                return `Sincronizar Serie: ${this.inCodSymbol}`
            }
            return "Sincronizar Símbolo"
        }
    },
    watch: {
        open: function (newval) {
            this.$emit('input', newval)
            if (newval) {
                this.cod_symbol = this.inCodSymbol || ""
                this.nom_symbol = ""
                this.fichero = null
                if (!this.fch_desde || !this.fch_hasta) {
                    this.sel_rango(this.rango_seleccionado.codigo)
                }
            }
        },
        value: function (newval) {
            this.open = newval
        },
        inCodSymbol: function (newval) {
            this.cod_symbol = newval || ""
            this.nom_symbol = ""
        }
    },
    data() {
        return {
            open: this.value,
            cod_symbol: this.inCodSymbol || "",
            nom_symbol: "",
            proveedor: "IBKR",
            lista_proveedores: [
                { label: "Interactive Brokers (IBKR)", value: "IBKR" },
                { label: "MarketData", value: "MARKETDATA" },
                { label: "AlphaVantage", value: "ALPHAVANTAGE" },
                { label: "Massive", value: "MASSIVE" },
                { label: "CSV NASDAQ (Archivo local)", value: "CSV_NASDAQ" },
                { label: "CSV Investing (Archivo local)", value: "CSV_INVESTING" }
            ],
            fichero: null,
            modo_carga: "Append",
            fch_desde: "",
            fch_hasta: "",
            loading: false,
            lista_modos_carga: ["Append", "Overwrite", "Replace"],
            rangos_fechas: [
                { "codigo": "RANGOS_FECHAS", "nombre": "Rangos de Fechas" },
                { "codigo": "ULTIMOS_7_DIAS", "nombre": "Últimos 7 días" },
                { "codigo": "ULTIMOS_30_DIAS", "nombre": "Últimos 30 días" },
                { "codigo": "ULTIMOS_100_DIAS", "nombre": "Últimos 100 días" },
                { "codigo": "ANYO_EN_CURSO", "nombre": "Año en curso" },
                { "codigo": "MAX", "nombre": "Máximo posible" }
            ],
            rango_seleccionado: { "codigo": "ULTIMOS_7_DIAS", "nombre": "Últimos 7 días" }
        }
    },
    mounted: function () {
        this.sel_rango(this.rango_seleccionado.codigo)
    },
    methods: {
        sel_rango: function (rango_codigo) {
            for (const elem of this.rangos_fechas) {
                if (elem.codigo == rango_codigo) {
                    this.rango_seleccionado = elem
                }
            }

            let fch_desde = null, fch_hasta = null

            switch (rango_codigo) {
                case 'ULTIMOS_7_DIAS':
                    [fch_desde, fch_hasta] = this.calc_ultimos_n_dias(7)
                    break;
                case 'ULTIMOS_30_DIAS':
                    [fch_desde, fch_hasta] = this.calc_ultimos_n_dias(30)
                    break;
                case 'ULTIMOS_100_DIAS':
                    [fch_desde, fch_hasta] = this.calc_ultimos_n_dias(100)
                    break;
                case 'ANYO_EN_CURSO':
                    [fch_desde, fch_hasta] = this.calc_anyo_en_curso()
                    break;
                case 'MAX':
                    [fch_desde, fch_hasta] = this.calc_max()
                    break;
                default:
                    break;
            }
            this.fch_desde = fch_desde
            this.fch_hasta = fch_hasta
        },
        calc_ultimos_n_dias: function (n_dias) {
            const now = new Date()
            const fch_desde = date.format(date.addDays(now, n_dias * -1), "DD/MM/YYYY")
            const fch_hasta = date.format(now, "DD/MM/YYYY")
            return [fch_desde, fch_hasta]
        },
        calc_anyo_en_curso: function () {
            const now = new Date()
            const fch_desde = date.format(new Date(now.getFullYear(), 0, 1), "DD/MM/YYYY")
            const fch_hasta = date.format(now, "DD/MM/YYYY")
            return [fch_desde, fch_hasta]
        },
        calc_max: function () {
            const now = new Date()
            const fch_hasta = date.format(now, "DD/MM/YYYY")
            const fch_desde = "01/01/1000"
            return [fch_desde, fch_hasta]
        },
        select_symbol: function (symbol) {
            if (!symbol) return
            this.cod_symbol = symbol.value || ""
            this.nom_symbol = symbol.label || ""
        },
        clear_symbol: function () {
            this.cod_symbol = ""
            this.nom_symbol = ""
        },
        procesar: async function () {
            if (!this.cod_symbol) {
                store.dispatch("incluir_msg", "Debe seleccionar o indicar un símbolo")
                return
            }

            const providerVal = typeof this.proveedor === 'object' && this.proveedor !== null
                ? this.proveedor.value || this.proveedor.label
                : this.proveedor

            const providerKey = (providerVal || "").toUpperCase()
            const api_serie = new Serie()

            this.loading = true

            try {
                // Caso 1: Archivo CSV NASDAQ
                if (providerKey === "CSV_NASDAQ") {
                    if (!this.fichero) {
                        store.dispatch("incluir_msg", "Debe seleccionar un archivo CSV de NASDAQ")
                        this.loading = false
                        return
                    }
                    const formData = new FormData()
                    formData.append("fichero", this.fichero)
                    formData.append("cod_symbol", this.cod_symbol)
                    formData.append("modo_carga", this.modo_carga || "Append")

                    const postConfig = get_postconfig()
                    postConfig.headers['Content-Type'] = "multipart/form-data"

                    const resp = await axios.post('/serie_controller/NasdaqCsvLoader/load', formData, postConfig)
                    store.dispatch("incluir_httpresp", resp)
                }
                // Caso 2: Archivo CSV Investing
                else if (providerKey === "CSV_INVESTING") {
                    if (!this.fichero) {
                        store.dispatch("incluir_msg", "Debe seleccionar un archivo CSV de Investing")
                        this.loading = false
                        return
                    }
                    const formData = new FormData()
                    formData.append("fichero", this.fichero)
                    formData.append("cod_symbol", this.cod_symbol)
                    formData.append("modo_carga", this.modo_carga || "Append")

                    const postConfig = postconfig()
                    postConfig.headers['Content-Type'] = "multipart/form-data"

                    const resp = await axios.post('/serie_controller/InvestingLoader/load', formData, postConfig)
                    store.dispatch("incluir_httpresp", resp)
                }
                // Caso 3: Proveedores por API
                else {
                    if (!this.fch_desde || !this.fch_hasta) {
                        store.dispatch("incluir_msg", "Debe ingresar las fechas de inicio y fin")
                        this.loading = false
                        return
                    }

                    const fchDesdeFormatted = date.transform(this.fch_desde, "DD/MM/YYYY", "YYYY-MM-DD")
                    const fchHastaFormatted = date.transform(this.fch_hasta, "DD/MM/YYYY", "YYYY-MM-DD")

                    if (providerKey === "ALPHAVANTAGE") {
                        const resp = await api_serie.load_alphavantage_series({
                            cod_symbol: this.cod_symbol,
                            fch_desde: fchDesdeFormatted,
                            fch_hasta: fchHastaFormatted,
                            modo_carga: this.modo_carga || "Append"
                        })
                        store.dispatch("incluir_httpresp", resp)
                    } else if (providerKey === "MASSIVE") {
                        const resp = await api_serie.load_massive_series({
                            cod_symbol: this.cod_symbol,
                            fch_desde: fchDesdeFormatted,
                            fch_hasta: fchHastaFormatted,
                            modo_carga: this.modo_carga || "Append"
                        })
                        store.dispatch("incluir_httpresp", resp)
                    } else if (providerKey === "MARKETDATA") {
                        const resp = await api_serie.load_marketdata_series({
                            cod_symbol: this.cod_symbol,
                            fch_desde: fchDesdeFormatted,
                            fch_hasta: fchHastaFormatted,
                            modo_carga: this.modo_carga || "Append"
                        })
                        store.dispatch("incluir_httpresp", resp)
                    } else {
                        // INTERACTIVE BROKERS / IBKR (por defecto)
                        const resp = await api_serie.synchronize({
                            market_data_provider: "IBKR",
                            cod_symbol: this.cod_symbol,
                            fch_desde: fchDesdeFormatted,
                            fch_hasta: fchHastaFormatted,
                            modo_carga: (this.modo_carga || "APPEND").toUpperCase()
                        })
                        store.dispatch("incluir_httpresp", resp)
                    }
                }

                // Notificación de éxito
                this.$q.notify({
                    type: "positive",
                    message: `Serie ${this.cod_symbol} sincronizada correctamente`,
                    position: "top",
                    timeout: 2500
                })

                this.open = false
                this.$emit("sincronizado", { cod_symbol: this.cod_symbol })
                serieStore.get_resumen_serie()

            } catch (err) {
                console.error(err)
                if (err.response) {
                    store.dispatch("incluir_httpresp", err.response)
                } else {
                    store.dispatch("incluir_msg", err.message || "Error al sincronizar")
                }
            } finally {
                this.loading = false
            }
        }
    }
}
</script>
