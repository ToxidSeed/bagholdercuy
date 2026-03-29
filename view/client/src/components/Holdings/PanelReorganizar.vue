<template>
    <div>
        <q-toolbar>
            <q-toolbar-title>
                Reorganizar Transacciones
            </q-toolbar-title>
        </q-toolbar>
        <q-card flat>
            <q-toolbar>
                <div class="q-gutter-xs">
                    <q-btn label="Reorganizar" color="primary" dense no-caps icon="flip_to_front" />
                </div>
            </q-toolbar>
            <q-separator />
            <q-bar class="bg-white">
                <q-btn label="BUSCAR TRANSACCIONES" flat icon="search" color="blue-10" class="text-capitalize"
                    @click="btnBuscarTransaccionesClick" />
            </q-bar>
            <q-separator />
            <q-tabs v-model="tab" class="text-grey shadow-2" align="left" dense no-caps inline-label
                active-color="primary">
                <q-tab name="otros_activos" label="OTROS ACTIVOS" />
                <q-tab name="opciones" label="OPCIONES" />
            </q-tabs>
            <q-tab-panels v-model="tab">
                <q-tab-panel name="otros_activos">
                    <div class="row q-col-gutter-xs">
                        <SelectSymbol class="col-4" label="Symbol" v-on:select-symbol="sel_symbol"
                            v-if="tab == 'otros_activos'" />
                        <HelperPeriodo class="col-4" />
                    </div>
                </q-tab-panel>
                <q-tab-panel name="opciones">
                    <div class="row q-col-gutter-xs">
                        <q-input label="Código de opción" v-model="cod_symbol_contrato" outlined color="blue-10" dense
                            class="col-2">
                            <template v-slot:after>
                                <q-btn round dense flat icon="search" @click="win_opciones.visible = true" />
                            </template>
                        </q-input>

                        <div class="col-4">
                            <div class="q-field__label">Subyacente</div>
                            <span class="text-primary text-bold">{{ symbol_subyacente.value }}</span> - {{
                                symbol_subyacente.label }}
                        </div>
                        <q-input borderless class="col-2" label="Fch. Expiracion" readonly v-model="fch_expiracion"
                            color="blue-10" dense />
                        <q-input borderless readonly class="col-2" label="Strike" v-model="imp_strike" color="blue-10"
                            dense />
                    </div>

                    <!--
                        <SelectSymbol class="col-4" label="Subyacente" v-on:select-symbol="sel_subyacente" />
                        <q-input label="Fch. Expiracion" outlined color="blue-10" dense>
                        </q-input>
                        <q-input label="Strike" outlined color="blue-10" dense class="col-1">
                        </q-input>
                        -->
                </q-tab-panel>
            </q-tab-panels>
        </q-card>
        <q-separator />
        <q-card-section class="text-subtitle1 text-bold  q-pb-none text-primary" v-show="false">
            Transacciones Encontradas
        </q-card-section>
        <TableTransaccionesDia :data="data" />
        <winBuscadorOpciones v-model="win_opciones.visible" v-on:option-select="selContratoOpcion" />
    </div>
</template>
<script>
import { get_postconfig } from '@/common/request.js'
import TableTransaccionesDia from '@/components/Holdings/TableTransaccionesDia.vue'

import SelectSymbol from '@/components/SelectSymbol.vue';
import HelperPeriodo from '@/components/common/HelperPeriodo.vue'
import { TRANSACCION } from '@/api/endpoints.js'
import winBuscadorOpciones from '@/components/common/winBuscadorOpciones/winBuscadorOpciones.vue'
export default {
    name: "PanelReorganizar",
    components: {
        TableTransaccionesDia,
        SelectSymbol,
        HelperPeriodo,
        winBuscadorOpciones
    },
    data: () => {
        return {
            flg_opcion: false,
            cod_symbol: "",
            nom_symbol: "",
            symbol_subyacente: {},
            cod_symbol_contrato: "",
            fch_expiracion: null,
            imp_strike: null,
            fch_desde: null,
            fch_hasta: null,
            data: [],
            tab: "otros_activos",
            win_opciones: {
                visible: false
            }
        }
    },
    methods: {
        sel_symbol: function (item) {
            this.cod_symbol = item.value
            this.nom_symbol = item.label
        },
        sel_subyacente: function (item) {
            this.symbol_subyacente = item
        },
        btnBuscarTransaccionesClick: function () {
            let cod_symbol = ""
            cod_symbol = this.tab == 'opciones' ? this.cod_symbol_contrato : this.cod_symbol
            this.get_transacciones_x_symbol({ cod_symbol: cod_symbol })
        },
        get_transacciones_x_symbol: function (params) {
            let postconfig = get_postconfig()
            const cod_symbol = params.cod_symbol

            this.$http.post(TRANSACCION.GET_TRANSACCIONES_X_SYMBOL, {
                id_cuenta: localStorage.getItem("id_cuenta"),
                cod_symbol: cod_symbol
            }, postconfig).then(httpresp => {
                this.data = []
                let appresp = httpresp.data
                if (appresp.success == false) {
                    this.$refs.msgbox.httpresp(httpresp)
                } else {
                    appresp.data.forEach(element => {
                        this.data.push(element)
                    })
                }
            })
        },
        selContratoOpcion: function (item) {
            console.log(item)
            this.cod_symbol_contrato = item.cod_symbol
            this.symbol_subyacente = item.subyacente
            this.fch_expiracion = item.fch_vencimiento
            this.imp_strike = item.imp_strike
        }
    }
}
</script>