<template>
    <div>
        <q-card flat>
            <TableVariacionDiaria :indata="data" :symbol_value="symbol_value" :symbol_nombre="symbol_text">
            </TableVariacionDiaria>
            <q-inner-loading :showing="loading">
                <q-spinner-gears size="50px" color="blue-10" />
            </q-inner-loading>
        </q-card>
    </div>
</template>
<script>
import TableVariacionDiaria from '@/components/informes/TableVariacionDiaria.vue'
import { postconfig } from '@/common/request.js';
//import date from 'date-and-time'

export default {
    name: "PanelVariacionDiariaSeries",
    components: {
        TableVariacionDiaria
    },
    props: {
        symbolName: {
            type: String,
            default: ""
        },
        symbolValue: {
            type: String,
            default: ""
        },
        fchDesde: {
            type: String,
            default: ""
        },
        fchHasta: {
            type: String,
            default: ""
        }
    },
    mounted: function () {
        console.log("mounted")
        this.init()
    },
    watch: {
        $route: function (newval) {
            if (Object.keys(newval.query).length > 0) {
                console.log("query", newval.query)
                this.symbol_value = newval.query.cod_symbol
                this.symbol_text = this.symbolName
                this.fch_desde = newval.query.fch_desde
                this.fch_hasta = newval.query.fch_hasta
                let params = {
                    symbol_value: this.symbol_value,
                    fch_desde: this.fch_desde,
                    fch_hasta: this.fch_hasta
                }
                this.get_variacion_diaria(params)
            }
        }
    },
    data() {
        return {
            symbol_value: "",
            symbol_text: "",
            data: [],
            loading: false,
            fch_desde: "",
            fch_hasta: ""
        }
    },
    methods: {
        init: function () {
            if (Object.keys(this.$route.query).length > 0) {
                this.symbol_value = this.$route.query.cod_symbol
                this.symbol_text = this.symbolNameSOXL
                this.fch_desde = this.$route.query.fch_desde
                this.fch_hasta = this.$route.query.fch_hasta
                let params = {
                    symbol_value: this.symbol_value,
                    fch_desde: this.fch_desde,
                    fch_hasta: this.fch_hasta
                }
                this.get_variacion_diaria(params)
            }
        },
        get_variacion_diaria: function (params) {

            this.loading = true
            this.$http.post(
                '/reportes/VariacionDiariaBuilder/build', {
                symbol: params.symbol_value,
                fch_desde: params.fch_desde,
                fch_hasta: params.fch_hasta
            },
                postconfig()
            ).then(httpresp => {
                this.msgbox = {
                    httpresp: httpresp,
                    onerror: true
                }

                let appresp = httpresp.data
                this.data = []

                if (appresp.extradata && appresp.extradata.meta) {
                    this.symbol_text = appresp.extradata.meta.symbol_text
                    this.symbol_value = appresp.extradata.meta.symbol_value
                }

                appresp.data.forEach(element => {
                    element.imp_cierre_ant = element.imp_cierre_ant.toFixed(2)
                    element.num_dia_semana = new Date(element.fch_serie).getDay() + 1
                    element.imp_apertura = element.imp_apertura.toFixed(2)
                    element.imp_maximo = element.imp_maximo.toFixed(2)
                    element.imp_minimo = element.imp_minimo.toFixed(2)
                    element.imp_cierre = element.imp_cierre.toFixed(2)
                    element.imp_variacion_apertura = element.imp_variacion_apertura.toFixed(2)
                    element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(2)
                    element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(2)
                    element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(2)
                    element.pct_variacion_apertura = element.pct_variacion_apertura.toFixed(2)
                    element.pct_variacion_cierre = element.pct_variacion_cierre.toFixed(2)
                    element.pct_variacion_maximo = element.pct_variacion_maximo.toFixed(2)
                    element.pct_variacion_minimo = element.pct_variacion_minimo.toFixed(2)
                    this.data.push(element)
                })
            }).finally(() => {
                this.loading = false
            })

        }
    }
}
</script>