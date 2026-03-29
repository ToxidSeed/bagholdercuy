<template>
    <div>
        <q-card>
            <q-card-section class="q-pt-xs q-pb-none row">

                <div class="text-h6 text-blue-10">Registro de Orden</div>
                <q-space />
                <q-btn color="primary" @click="btn_opciones_click" :disable="btn_opciones_disable">Opciones</q-btn>
                <q-btn flat color="red" icon="close" @click="btn_close_click_handler" />

                <!--<div v-show="ref_num_orden_visible">Insertar {{insertar}} de la Orden: <span class="text-primary">{{ref_num_orden}}</span></div>-->
            </q-card-section>
            <q-card-actions align="left">
                <q-btn color="green-8" @click="save" icon="done" flat no-caps>Confirmar</q-btn>
            </q-card-actions>
            <q-separator />
            <q-card-section>
                <div class="row">
                    <q-btn-group push unelevated>
                        <q-btn push label="Buy" icon="fas fa-angle-double-left"
                            :color="order.id_tipo_transaccion == tiposTransaccion.C.value ? 'blue-10' : 'white'"
                            :text-color="order.id_tipo_transaccion == tiposTransaccion.C.value ? 'white' : 'black'"
                            @click="order.id_tipo_transaccion = tiposTransaccion.C.value" />
                        <q-btn push label="Sell" icon-right="fas fa-angle-double-right"
                            :color="order.id_tipo_transaccion == tiposTransaccion.V.value ? 'red-10' : 'white'"
                            :text-color="order.id_tipo_transaccion == tiposTransaccion.V.value ? 'white' : 'black'"
                            @click="order.id_tipo_transaccion = tiposTransaccion.V.value" />
                    </q-btn-group>
                </div>
                <div class="row">
                    <div class="col-3 q-pl-xs">
                        <q-input class="col-3" v-model="order.fch_transaccion" stack-label label="Fch. Transacción"
                            mask="##/##/####" fill-mask="">
                            <!--<q-popup-proxy ref="qDateProxy" transition-show="scale" transition-hide="scale">
                            <q-date v-model="order.order_date" mask="YYYY-MM-DD" v-close-popup >                    
                            </q-date>
                            </q-popup-proxy>-->
                        </q-input>
                    </div>
                    <div class="col-9 q-pl-xs">
                        <q-input v-model="symbol_search" label="symbol" ref="symbol" @input="search" debounce="1000">
                            <template v-slot:after>
                                <q-icon name="search" @click="search" class="cursor-pointer" />
                            </template>
                            <q-popup-proxy v-model="states.symbol_popup" @show="onShowProxy">
                                <!--<div :style="style.symbol_width">-->
                                <q-list bordered separator>
                                    <q-item v-for="item in symbol_list" :key="item.id" clickable v-ripple
                                        @click="sel_symbol(item)">
                                        <q-item-section>{{ item.symbol }}-{{ item.name }}</q-item-section>
                                    </q-item>
                                </q-list>
                                <!--</div>-->
                            </q-popup-proxy>
                        </q-input>
                    </div>
                </div>

                <div v-if="order.asset_type == TIPO_ACTIVO_OPT">
                    <span class="text-h6 text-bold">Subyacente:</span><span
                        class="q-pt-xs q-pl-xs text-h6  text-deep-purple">{{
                        order.subyacente }}</span>
                    <div class="q-pt-xs">{{ symbol_info }}</div>
                </div>
                <div v-if="order.asset_type != TIPO_ACTIVO_OPT">
                    <div class="q-pt-xs text-h6 text-bold text-deep-purple">{{ order.symbol }}</div>
                    <div class="q-pt-xs">{{ symbol_info }}</div>
                </div>

                <div class="row">
                    <div class="col-5">
                        <q-input stack-label v-model="order.cantidad" label="Cantidad" type="number"
                            input-class="text-right" />
                    </div>
                    <div class="col-5 q-pl-xs">
                        <q-input stack-label v-model="order.importe" label="Precio" type="number"
                            input-class="text-right" />
                    </div>
                    <div class="col-2 q-pl-xs">
                        <q-input stack-label label="Moneda" readonly v-model="order.moneda_id" />
                    </div>
                </div>
            </q-card-section>
            <q-separator />

        </q-card>
        <q-dialog v-model="win_opciones.visible">
            <PanelOptionsChain style="max-width:750px" v-bind:symbol_val="order.symbol"
                v-bind:symbol_name="order.symbol_name" v-on:option-select="option_selected"
                v-on:close="win_opciones.visible = false" v-on:sel-contract="option_selected" />
        </q-dialog>

    </div>
</template>
<script>

import date from 'date-and-time'
import PanelOptionsChain from '@/components/common/PanelOptionsChain.vue';
import { postconfig } from '@/common/request.js';
import { CLIENT_DATE_FORMAT, TIPO_ACTIVO_OPT, ISO_DATE_FORMAT } from '@/common/constants.js'
import store from '../../store/store';
import { mapState } from 'vuex'

export default {
    name: "PanelTrade",
    components: {
        PanelOptionsChain
    },
    props: {
        ref_num_orden: {
            default: ""
        },
        insertar: {
            default: ""
        },
        symbol: {
            default: ""
        },
        asset_type: {
            default: ""
        },
        order_type: {
            default: "B"
        },
        order_date: {
            type: String,
            default: ""
        },
        update: {
            default: ""
        }
    },
    data: () => {
        return {
            order: {
                id: "",
                symbol: "",
                contrato: "",
                contrato_desc: "",
                symbol_name: "",
                cantidad: "",
                importe: "",
                fch_transaccion: "",
                order_type: "",
                asset_type: "",
                subyacente: "",
                id_instrumento_financiero: null,
                id_tipo_transaccion: null,
                id_contrato_opcion: null
            },
            states: {
                symbol_popup: false
            },
            style: {
                symbol_width: ""
            },
            symbol_list: [],
            asset_type_list: ["stock", "options"],
            symbol_search: "",
            btn_opciones: {
                disable: true
            },
            win_opciones: {
                visible: false
            },
            TIPO_ACTIVO_OPT: TIPO_ACTIVO_OPT,
            symbol_info: ""
        }
    },
    watch: {
        /*update:function(old, value){        
            if (old != value){
                this.order.symbol = this.symbol
                this.order.asset_type = this.asset_type
                this.order.order_type = this.order_type
                this.symbol_search = this.symbol            
            }
        }*/
        symbol: function (newval) {
            this.order.symbol = newval
            this.symbol_search = newval
            this.get_datos_symbol()
        },
        order_type: function (newval) {
            this.order.order_type = newval
        }
    },
    computed: {
        ...mapState('serverConstants', ['instrumentosFinancieros', 'tiposTransaccion']),
        ref_num_orden_visible: function () {
            return this.ref_num_orden.length == 0 ? false : true;
        },
        btn_opciones_disable: function () {
            return this.order.symbol == "" ? true : false;
        },
        symbol_info_desc: function () {
            return this.order.contrato_desc == "" ? this.order.symbol_name : this.order.contrato_desc;
        }
    },
    mounted: function () {
        this.order.fch_transaccion = date.format(new Date(), CLIENT_DATE_FORMAT);

        var symbol_witdh = this.$refs.symbol.$el.control.clientWidth
        this.style.symbol_width = "width:" + symbol_witdh + "px";

        //initial values
        this.order.symbol = this.symbol
        //this.order.asset_type = this.asset_type
        //this.order.order_type = this.order_type
        this.order.id_tipo_transaccion = this.tiposTransaccion.C.value
        this.symbol_search = this.symbol
        //
        //this.get_datos_symbol()
        this.$emit('open', 30)
    },
    methods: {
        onShowProxy: function () {
            this.$refs.symbol.focus()
        },
        search: function () {
            console.log(this.instrumentosFinancieros)
            console.log('xxxxx')
            if (this.symbol_search == "") {
                return
            }
            this.$http.post(
                'SymbolManager/SymbolFinder/buscar_por_texto', {
                texto: this.symbol_search
            },
                postconfig()
            ).then(httpresponse => {
                store.dispatch("incluir_httpresp_si_apperror", httpresponse)
                let appresponse = httpresponse.data
                if (appresponse.success == true) {
                    this.symbol_list = appresponse.data
                    console.log(this.symbol_list)
                    this.states.symbol_popup = true
                }
            });
        },
        save: function () {
            //order_type           

            /*
            .doc-gdpr {
                max-width: 360px;
            }
             */
            //symbol
            if (this.order.symbol == "") {
                this.$q.notify({
                    message: 'No se ha informado el symbol',
                    color: "white",
                    textColor: 'red',
                    position: 'bottom-right',
                    multiLine: true,
                    actions: [
                        { label: 'Aceptar', color: 'primary', handler: () => { /* ... */ } }
                    ],
                    classes: "doc-gdpr"
                })
                return;
            }
            //quantity
            if (parseInt(this.order.quantity) <= 0) {
                this.$q.notify({
                    message: 'La cantidad de participaciones debe ser mayor a 0',
                    color: "white",
                    textColor: 'red',
                    position: 'bottom-right',
                    multiLine: true,
                    actions: [
                        { label: 'Aceptar', color: 'primary', handler: () => { /* ... */ } }
                    ],
                    classes: "doc-gdpr"
                })
                return;
            }

            //price
            if (parseInt(this.order.quantity) <= 0) {
                this.$q.notify({
                    message: 'El precio por participación debe ser mayor a 0',
                    color: "white",
                    textColor: 'red',
                    position: 'bottom-right',
                    multiLine: true,
                    actions: [
                        { label: 'Aceptar', color: 'primary', handler: () => { /* ... */ } }
                    ],
                    classes: "doc-gdpr"
                })
                return;
            }
            //order_date
            if (this.order.order_date == "") {
                this.$q.notify({
                    message: 'Debe seleccionar una fecha de transacción',
                    color: "white",
                    textColor: 'red',
                    position: 'bottom-right',
                    multiLine: true,
                    actions: [
                        { label: 'Aceptar', color: 'primary', handler: () => { /* ... */ } }
                    ],
                    classes: "doc-gdpr"
                })
                return;
            }

            if (this.order.id_instrumento_financiero == null) {
                this.$q.notify({
                    message: `El symbol ${this.order.symbol} no tiene id_instrumento_financiero informado`,
                    color: "white",
                    textColor: 'red',
                    position: 'bottom-right',
                    multiLine: true,
                    actions: [
                        { label: 'Aceptar', color: 'primary', handler: () => { /* ... */ } }
                    ],
                    classes: "doc-gdpr"
                })
                return;
            }

            //determine if it is buy or sell            
            this.do_order();
        },
        cerrar: function () {
            this.$emit("cerrar")
        },
        sel_symbol: function (item) {
            console.log(item)
            this.states.symbol_popup = false
            this.order.symbol = item.symbol
            this.order.symbol_name = item.name
            this.order.moneda_id = item.moneda_id
            this.order.id_instrumento_financiero = item.id_instrumento_financiero
            this.symbol_search = item.symbol
            //this.order.asset_type = item.asset_type
            this.symbol_info = item.name
        },
        option_selected: function (option, order_type) {
            console.log(option)
            this.win_opciones.visible = false
            //this.order.symbol = 
            this.order.symbol = option.cod_symbol
            this.order.contrato = option.cod_symbol
            this.symbol_info = option.descripcion
            this.order.subyacente = option.cod_symbol_subyacente
            this.order.id_instrumento_financiero = this.instrumentosFinancieros.OPTION.value
            this.order.id_contrato_opcion = option.id_contrato_opcion
            this.symbol_search = option.cod_symbol
            this.order.symbol_name = option.descripcion
            if (this.order.order_type == "") {
                this.order.order_type = order_type == "buy" ? "B" : "S";
            }
            console.log(this.order)
        },
        do_order: function () {
            console.log(this.order)
            this.$http.post(
                'orden/OrdenController/ejecutar', {
                cod_symbol: this.order.symbol,
                id_instrumento_financiero: this.order.id_instrumento_financiero,
                id_tipo_transaccion: this.order.id_tipo_transaccion,
                id_contrato_opcion: this.order.id_contrato_opcion,
                cantidad: this.order.cantidad,
                imp_accion: this.order.importe,
                fch_transaccion: date.transform(this.order.fch_transaccion, CLIENT_DATE_FORMAT, ISO_DATE_FORMAT)
            },
                postconfig()).then(httpresp => {
                    //this.$refs.msgbox.httpresp(httpresp)                                   
                    store.dispatch("incluir_httpresp", httpresp)
                });
        },
        btn_opciones_click: function () {
            let symbol = this.symbol
            let text = this.symbol_search

            if (symbol == text) {
                text = ""
            }
            if (symbol != text && text != "") {
                symbol = ""
            }
            this.win_opciones.visible = true

            /*this.$emit(
                'btn_opciones_click',symbol, text
            )*/
        },
        btn_close_click_handler: function () {
            this.$emit('btn-close-click')
        }
    }
}
</script>
<style lang="scss">
.doc-gdpr {
    max-width: 400px;
    min-width: 350px;
    background-color: "white";
    color: red;
}
</style>