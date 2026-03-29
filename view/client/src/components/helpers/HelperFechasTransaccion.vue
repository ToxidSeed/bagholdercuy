<template>
    <div>
        <q-dialog v-model="visible">
            <q-card style="min-width:40vw;">
                <q-toolbar>
                    <q-toolbar-title class="text-blue-10" style="overflow:visible;">
                        Seleccionar Fecha
                    </q-toolbar-title>
                    <q-space />
                    <q-btn icon="close" color="red" dense @click="visible = false" />
                </q-toolbar>
                <q-card-section class="q-pa-none">
                    <q-table dense :columns="columns" :data="data" row-key="fch_orden" separator="vertical"
                        :filter="filter" :pagination="pagination" @row-dblclick="select">
                        <template v-slot:top-left>
                            <div class="text-subtitle1">Fechas con transacciones</div>
                        </template>
                        <template v-slot:top-right>
                            <q-input outlined dense debounce="300" v-model="filter" placeholder="Filtrar resultados">
                                <template v-slot:append>
                                    <q-icon name="search" />
                                </template>
                            </q-input>
                        </template>
                    </q-table>
                </q-card-section>
            </q-card>
        </q-dialog>
        <MessageBox ref="msgbox" />
    </div>
</template>
<script>
//import { CLIENT_DATE_FORMAT, ISO_DATE_FORMAT } from '@/common/constants.js'
import { get_postconfig } from '@/common/request.js'
//import date from 'date-and-time';
import MessageBox from '../dialogs/MessageBox.vue';
//import SelectAnyosOrden from '@/components/helpers/SelectAnyosOrden.vue'
//import SelectMesesOrden from '@/components/helpers/SelectMesesOrden.vue'
import { TRANSACCION } from '@/api/endpoints.js'
export default {
    name: "HelperFechasTransaccion",
    props: {
        anyo: {
            type: String,
            default: ""
        },
        mes: {
            type: String,
            default: ""
        },
        close_on_select: {
            type: Boolean,
            default: true
        },
        filtros: {
            type: Object,
            default: () => {
                return {
                    codSymbol: null,
                    fchDesde: null,
                    fchHasta: null
                }
            }
        },
        nomSymbol: {
            type: String,
            default: ""
        }
    },
    components: {
        MessageBox
    },
    data: () => {
        return {
            filter: '',
            visible: false,
            columns: [
                {
                    label: "Fch. Transaccion",
                    align: "left",
                    name: "fch_transaccion",
                    field: "fch_transaccion",
                    style: "width:100px;"
                }, {
                    label: "Num. Transacciones",
                    align: "right",
                    name: "num_transacciones",
                    field: "num_transacciones",
                    style: "width:50px;"
                }, {
                    label: "Año",
                    align: "right",
                    name: "anyo",
                    field: "anyo",
                    style: "width:50px;"
                }, {
                    label: "Mes",
                    align: "right",
                    name: "mes",
                    field: "mes",
                    style: "width:50px;"
                }, {
                    label: "",
                    align: "left",
                    name: "",
                    field: ""
                }
            ],
            data: [],
            pagination: {
                rowsPerPage: 31
            }
        }
    },
    mounted: function () {

        //cargar los años

        //cargar los meses
    },
    watch: {
        /*anyo:function(newval,oldval){                    
            console.log(newval)
            console.log(oldval)
            console.log(this.mes)
            if(newval!=""){
                this.get_meses(newval)
            }
            if(newval!="" && this.mes!=""){
                this.get_fechas(newval, this.mes)
            }            
        },
        mes:function(newval,oldval){                  
            console.log(newval)
            console.log(oldval)
            if(newval!="" && this.anyo!=""){
                this.get_fechas(this.anyo, newval)
            }
        }*/
    },
    methods: {
        open: function (filtros) {
            this.visible = true
            this.get_fechas(filtros.codSymbol, filtros.fchDesde, filtros.fchHasta)
        },
        get_fechas: function (cod_symbol, fch_ini, fch_fin) {
            let postconfig = get_postconfig()
            this.data = []
            this.$http.post(TRANSACCION.GET_FECHAS_CON_TRANSACCIONES, {
                id_cuenta: localStorage.getItem("id_cuenta"),
                cod_symbol: cod_symbol,
                fch_ini: fch_ini,
                fch_fin: fch_fin
            }, postconfig).then(httpresp => {
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
        msgbox: function (httpresp) {
            this.$refs.msgbox.httpresp(httpresp)
        },
        select: function (evt, row) {
            this.$emit('select', row)
            this.visible = this.close_on_select == true ? false : true;
        }
    }
}
</script>