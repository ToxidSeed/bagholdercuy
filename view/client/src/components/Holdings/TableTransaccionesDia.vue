<template>
    <div>
        <q-table title="Ordenes por día" :columns="columns" :data="data" row-key="num_orden" selection="single"
            :selected.sync="selected" :pagination="pagination" separator="vertical" dense flat>
            <template v-slot:top>
                <div class="text-subtitle2 text-primary">Transacciones Encontradas</div><q-chip>{{ textNumTransacciones
                    }}</q-chip>
                <q-toolbar class="q-pl-none">
                    <div class="q-gutter-xs">
                        <q-btn outline color="primary" dense icon="keyboard_arrow_down" disabled @click="mover_abajo" />
                        <q-btn outline color="primary" dense icon="keyboard_arrow_up" @click="mover_arriba" disabled />
                        <span class="q-pl-xs">Selecciona una fila</span>
                    </div>
                </q-toolbar>
            </template>
            <template v-slot:body-cell-cod_symbol="props">
                <q-td :props="props">
                    {{ props.value }}
                    <q-popup-proxy context-menu>
                        <q-list dense bordered class="bg-white text-black">
                            <q-item v-for="(formato, index) in mostrar_formatos_alternativos(props.row)" :key="index"
                                v-show="formato" class="q-pl-none" clickable v-ripple v-close-popup
                                @click="copiar_portapapeles(formato)">
                                <q-item-section>{{ formato }}</q-item-section>
                            </q-item>
                        </q-list>
                    </q-popup-proxy>
                </q-td>
            </template>
        </q-table>
        <MessageBox ref="msgbox" />
        <!--
        <HelperFechasOrden ref="helperfechas" v-on:select="select_fch_orden" />
        -->
    </div>
</template>
<script>
import MessageBox from '../dialogs/MessageBox.vue'
//import HelperFechasOrden from '@/components/helpers/HelperFechasOrden.vue'

import date from 'date-and-time'
import { CLIENT_DATE_FORMAT, ISO_DATE_FORMAT } from '@/common/constants.js'
import { get_postconfig } from '@/common/request.js'
import { ContratoOpcion } from '@/common/contrato-opcion.js'
import { copyToClipboard } from 'quasar'

export default {
    name: "TableTransaccionesDia",
    components: {
        MessageBox,
        //      HelperFechasOrden
    },
    props: {
        data: {
            type: Array,
            default: () => []
        }
    },
    computed: {
        textNumTransacciones: function () {
            return `${this.data.length} registro${this.data.length == 1 ? '' : 's'}`
        }
    },
    data: () => {
        return {
            fch_orden: "",
            filter: {
                fch_orden: ""
            },
            flg_opcion: false,
            columns: [
                {
                    label: "Id. Transaccion",
                    align: "left",
                    field: "id_transaccion",
                    name: "id_transaccion",
                    style: 'width:60px;'
                }, {
                    label: "Fecha/hora Transaccion",
                    align: "left",
                    field: "fch_hr_transaccion",
                    name: "fch_hr_transaccion",
                    style: 'width:60px;'
                }, {
                    label: "FIFO Seq",
                    align: "left",
                    field: "orden_fifo",
                    name: "orden_fifo",
                    style: 'width:60px;'
                }, {
                    label: "Symbol",
                    align: "left",
                    field: "cod_symbol",
                    name: "cod_symbol",
                    classes: "bg-yellow",
                    style: 'width:60px;'
                }, {
                    label: "A/C",
                    align: "left",
                    field: row => row.indicador_apcierre ? row.indicador_apcierre.cod_indicador : '',
                    name: "cod_indicador",
                    style: 'width:60px;'
                }, {
                    label: "Inst. Fin.",
                    align: "left",
                    field: row => row.instrumento_financiero ? row.instrumento_financiero.cod_instrumento_financiero : '',
                    name: "cod_instrumento_financiero",
                    style: 'width:60px;'
                }, {
                    label: "Tipo",
                    align: "left",
                    field: row => row.tipo_transaccion ? row.tipo_transaccion.cod_tipo_transaccion : '',
                    name: "cod_tipo_transaccion",
                    style: 'width:60px;'
                }, {
                    label: "Ev. Orig.",
                    align: "left",
                    field: row => row.evento_origen ? row.evento_origen.cod_evento : '',
                    name: "cod_evento",
                    style: 'width:60px;'
                }, {
                    label: "Cantidad",
                    align: "right",
                    field: "cantidad",
                    name: "cantidad",
                    style: 'width: 60px'
                }, {
                    label: "Imp. Unitario",
                    align: "right",
                    field: "imp_unitario",
                    name: "imp_unitario",
                    style: 'width:60px;'
                }, {
                    label: "Imp. Transaccion",
                    align: "right   ",
                    field: "imp_transaccion",
                    name: "imp_transaccion",
                    style: 'width:60px;'
                }, {
                    label: "",
                    align: "left",
                    field: "",
                    name: ""
                }
            ],
            selected: [],
            pagination: {
                rowsPerPage: 15
            }
        }
    },
    mounted: function () {
        //this.init()
    },
    watch: {
        /*fch_orden:function(newval){
            this.get_ordenes_x_fecha(newval)
        }*/
    },
    methods: {
        init: async function () {
            let postconfig = get_postconfig()
            let httpresp = await this.$http.post('/OrdenManager/Buscador/get_max_fch_orden', {}, postconfig)
            let appdata = httpresp.data
            if (appdata.success == false) {
                this.$refs.msgbox.httpresp(httpresp)
            } else {
                let data = appdata.data
                this.filter.fch_orden = date.transform(data.fch_orden, ISO_DATE_FORMAT, CLIENT_DATE_FORMAT)
                this.fch_orden = this.filter.fch_orden
            }
            //
            this.get_ordenes_x_fecha(this.filter.fch_orden)
        },
        get_ordenes_x_fecha: function (fch_orden) {
            let postconfig = get_postconfig()

            this.selected = []
            this.$http.post('/OrdenManager/Buscador/get_ordenes_x_fecha', {
                fch_orden: fch_orden
            }, postconfig).then(httpresp => {
                let appresp = httpresp.data
                if (appresp.success == false) {
                    this.$refs.msgbox.httpresp(httpresp)
                } else {
                    this.data = appresp.data
                }
            })
        },
        open_fechas_helper: function () {
            this.$refs.helperfechas.open()
        },
        select_fch_orden: function (row) {
            this.fch_orden = row.order_date
            this.filter.fch_orden = row.order_date
            this.get_ordenes_x_fecha(this.filter.fch_orden)
        },
        mover_arriba: function () {
            let selected = this.selected.shift()
            let num_orden = selected.num_orden
            let prev_num_orden = num_orden - 1
            const prevrow = this.data.find(element => {
                return element.num_orden == prev_num_orden
            })
            prevrow.num_orden = num_orden
            selected.num_orden = prev_num_orden
            this.selected.push(selected)
            //ordenar
            this.ordenar()
        },
        mover_abajo: function () {
            let selected = this.selected.shift()
            let num_orden = selected.num_orden
            let sig_num_orden = num_orden + 1
            const sigrow = this.data.find(element => {
                return element.num_orden == sig_num_orden
            })
            sigrow.num_orden = num_orden
            selected.num_orden = sig_num_orden
            this.selected.push(selected)
            this.ordenar()
        },
        ordenar: function () {
            this.data.sort((a, b) => {
                if (a.num_orden > b.num_orden) {
                    return 1;
                }
                if (a.num_orden < b.num_orden) {
                    return -1;
                }
                if (a.num_orden == b.num_orden) {
                    return 0
                }
            })
        },
        mostrar_formatos_alternativos: function (row) {
            try {
                let contrato_opcion = new ContratoOpcion(row.cod_symbol)
                let human_readable = contrato_opcion.toHumanReadable()
                //let occ_extendido = contrato_opcion.toOCCExtendido()
                return [human_readable]
            } catch (error) {
                // Return empty if symbol is valid stock but not a valid option contract
                return []
            }
        },
        copiar_portapapeles: function (texto) {
            copyToClipboard(texto)
        }
    }
}
</script>

<style scoped>
::v-deep .q-table th {
    background-color: #eeeeee !important;
    color: #4a5568 !important;
    font-weight: bold !important;
    text-transform: uppercase !important;
    font-size: 12px !important;
}
</style>