<template>
    <div>
        <q-card>
            <q-card-section class="q-pb-none row">
                <div class="text-h6 text-blue-10">{{ title }}</div>
                <q-space />
                <q-btn flat dense icon="close" @click="close" />
                <!--<div class="text-subtitle2">{{subtitle}}</div>-->
            </q-card-section>
            <q-card-section>
                <div class="q-gutter-xs">
                    <SelectSymbol v-on:select-symbol="select_symbol" label="Subyacente" :in_symbol="symbol" />
                    <div>
                        <div class="row q-col-gutter-xs">
                            <q-input class="col-4" stack-label label="Contrato" v-model="cod_symbol_contrato"
                                color="blue-10" @input="get_options_chain" debounce="1000" outlined dense>
                            </q-input>
                            <q-input class="col-4" v-model="fch_expiracion" stack-label label="Fch. Expiracion"
                                color="blue-10" mask="##/##/####" placeholder="dd/mm/yyyy" debounce="2000"
                                :rules="[validateExpirationDate]" @input="input_expiration_date" outlined dense>
                                <template v-slot:after>
                                    <q-icon name="arrow_drop_down" class="cursor-pointer">
                                        <q-popup-proxy :offset="[100, 0]" v-model="show_sel_exp">
                                            <q-list bodered separator dense>
                                                <q-item v-for="elem in exp_dates" :key="elem" clickable v-ripple:purple
                                                    @click="sel_exp_date(elem)">
                                                    <q-item-section>{{ elem }}</q-item-section>
                                                </q-item>
                                            </q-list>
                                        </q-popup-proxy>
                                    </q-icon>
                                </template>
                            </q-input>
                            <q-input class="col-4" label="Strike" v-model="filter.strike" color="blue-10" stack-label
                                dense mask="#####" input-class="text-right" debounce="500" @input="get_options_chain"
                                outlined>
                                <template v-slot:after>
                                    <q-icon name="arrow_drop_down" class="cursor-pointer">
                                        <q-popup-proxy v-model="show_sel_strikes" :offset="[200, 0]">
                                            <q-list bordered separator dense>
                                                <q-item v-for="elem in strikes" :key="elem" clickable
                                                    style="width:150px;" @click="sel_strike(elem)">
                                                    <q-item-section>{{ elem }}</q-item-section>
                                                </q-item>
                                            </q-list>
                                        </q-popup-proxy>
                                    </q-icon>
                                </template>
                            </q-input>
                        </div>
                    </div>
                    <q-checkbox v-model="flg_opciones_vencidas" label="Opciones Vencidas" color="blue-10" />

                </div>
            </q-card-section>
            <div class="row">

                <div class="col-6">
                    <q-table dense title="CALLS" color="primary" :data="calls" :columns="call_columns" row-key="name"
                        :pagination="pagination" separator="vertical" flat
                        :visible-columns="['symbol', 'strike', 'expiration']">
                        <template v-slot:body="props">
                            <q-tr :props="props" @dblclick="sel_contract(props.row)" class="cursor-pointer"
                                style=":hover:'">
                                <q-menu touch-position context-menu>
                                    <q-list dense style="min-width: 100px">
                                        <q-item style="padding: 0px 0px" clickable v-close-popup
                                            @click="buy(props.row)">
                                            <q-item-section class="bg-primary text-white">
                                                <div class="q-pl-sm">Buy</div>
                                            </q-item-section>
                                        </q-item>
                                        <q-item style="padding: 0px 0px" clickable v-close-popup
                                            @click="sell(props.row)">
                                            <q-item-section class="bg-red text-white">
                                                <div class="q-pl-sm">Sell</div>
                                            </q-item-section>
                                        </q-item>
                                    </q-list>
                                </q-menu>
                                <q-td key="symbol" :props="props" style="width:30px">
                                    {{ props.row.cod_symbol }}
                                </q-td>
                                <q-td style="width:30px">
                                    {{ props.row.imp_strike }}
                                </q-td>
                                <q-td style="width:30px">
                                    {{ props.row.fch_vencimiento }}
                                </q-td>
                                <q-td>
                                </q-td>
                            </q-tr>
                        </template>
                    </q-table>
                </div>
                <div class="col-6 q-pl-sm">
                    <q-table dense title="PUTS" :data="puts" :columns="put_columns" row-key="name"
                        :pagination="pagination" separator="vertical" flat
                        :visible-columns="['symbol', 'strike', 'expiration']">
                        <template v-slot:body="props">
                            <q-tr :props="props" @dblclick="sel_contract(props.row)" class="cursor-pointer">
                                <q-menu touch-position context-menu>
                                    <q-list dense style="min-width: 100px">
                                        <q-item clickable v-close-popup @click="buy(props.row)">
                                            <q-item-section>Buy</q-item-section>
                                        </q-item>
                                        <q-item clickable v-close-popup @click="sell(props.row)">
                                            <q-item-section>Sell</q-item-section>
                                        </q-item>
                                    </q-list>
                                </q-menu>
                                <q-td key="symbol" :props="props" style="width:30px">
                                    {{ props.row.cod_symbol }}
                                </q-td>
                                <q-td style="width:30px">
                                    {{ props.row.imp_strike }}
                                </q-td>
                                <q-td style="width:30px">
                                    {{ props.row.fch_vencimiento }}
                                </q-td>
                                <q-td>
                                </q-td>
                            </q-tr>
                        </template>
                    </q-table>
                </div>
                <q-inner-loading :showing="dataLoading">
                    <q-spinner-gears size="50px" color="primary" />
                </q-inner-loading>
            </div>
        </q-card>
    </div>
</template>
<script>
import SelectSymbol from '@/components/SelectSymbol.vue'
import ContratoOpcion from "@/api/contrato-opcion.js"
import { HttpResponseHandler } from "@/common/http-response-handler.js"
import date from "date-and-time"

export default {
    name: "PanelOptionsChain",
    props: {
        asset_type: {
            type: String,
            default: ""
        },
        symbol: {
            type: Object,
            default: () => ({})
        },
        contract: {
            type: String,
            default: ""
        },
        title: {
            type: String,
            default: "Opciones"
        },
        sel_symbol_readonly: {
            type: Boolean,
            default: true
        },
        close_btn: {
            type: Boolean,
            default: false
        }
    },
    components: {
        SelectSymbol
    },
    data: () => {
        return {
            dataLoading: false,
            subyacente: "",
            fch_expiracion: "",
            imp_ejercicio: null,
            cod_symbol_contrato: "",
            flg_opciones_vencidas: false,
            filter: {
                cod_subyacente: "",
                fch_expiracion: null,
                imp_ejercicio: null,
                cod_symbol_contrato: "",
                flg_opciones_vencidas: false
            },
            calls: [],
            puts: [],
            exp_dates: [],
            strikes: [],
            call_columns: [
                {
                    align: "left",
                    name: "id_contrato_opcion",
                    label: "id_contrato_opcion",
                    field: "id_contrato_opcion"
                },
                {
                    align: "left",
                    name: "symbol",
                    label: "symbol",
                    field: "cod_symbol"
                }, {
                    align: "left",
                    name: "strike",
                    label: "strike",
                    field: "imp_strike"
                }, {
                    align: "left",
                    name: "expiration",
                    label: "expiration date",
                    field: "fch_vencimiento"
                }],
            put_columns: [
                {
                    align: "left",
                    name: "id_contrato_opcion",
                    label: "id_contrato_opcion",
                    field: "id_contrato_opcion"
                }, {
                    align: "left",
                    name: "symbol",
                    label: "symbol",
                    field: "cod_symbol"
                }, {
                    align: "left",
                    name: "strike",
                    label: "strike",
                    field: "imp_strike"
                }, {
                    align: "left",
                    name: "expiration",
                    label: "expiration date",
                    field: "fch_vencimiento"
                }],
            pagination: {
                rowsPerPage: 15
            },
            show_sel_exp: false,
            show_sel_strikes: false
        }
    },
    computed: {

    },
    watch: {
        symbol: function (newVal, oldVal) {
            console.log("newVal", newVal)
            console.log("oldVal", oldVal)
        }
    },
    mounted: function () {
        if (this.symbol?.value) {
            console.log("mounted", this.symbol.value)
            this.filter.cod_subyacente = this.symbol.value
            this.get_options_chain({ ...this.filter });
        }

        /*let search = false
        if (this.symbol_val != ""){            
            this.filter.symbol.value = this.symbol_val            
            search = true            
            console.log(this.filter)
            this.get_datos_symbol(this.symbol_val)
        }*/
        /*if (this.contract != ""){
            this.filter.contract = this.contract
            search = true
        }*/
        /*if (search == true){
            this.get_options_chain()
        }*/
    },
    methods: {
        select_symbol: function (selected) {
            this.subyacente = selected
            this.filter.cod_subyacente = this.subyacente.value
            this.get_options_chain({ ...this.filter });
        },
        sel_exp_date: function (selected) {
            this.show_sel_exp = false
            this.fch_expiracion = selected
            this.filter.fch_expiracion = date.transform(this.fch_expiracion, 'DD/MM/YYYY', 'YYYY-MM-DD');
            this.get_options_chain({ ...this.filter });
        },
        sel_strike: function (selected) {
            this.show_sel_strikes = false
            this.filter.imp_ejercicio = selected
            this.get_options_chain({ ...this.filter });
        },
        sel_contract: function (row) {
            let contrato = { ...row }
            contrato.subyacente = this.subyacente
            this.$emit('sel-contract', contrato, "")
        },
        input_expiration_date: function () {
            if (this.filter.cod_subyacente == {}) {
                return
            }

            if (this.validateExpirationDate(this.fch_expiracion) !== true) {
                return
            } else {

                this.filter.fch_expiracion = date.format(date.parse(this.fch_expiracion, 'DD/MM/YYYY'), 'YYYY-MM-DD');
            }
            this.get_options_chain({ ...this.filter });
        },
        input_strike: function () {
            if (this.filter.cod_subyacente == "") {
                return
            }
            this.get_options_chain({ ...this.filter });
        },
        get_options_chain: function (params) {
            this.dataLoading = true
            /*console.log('get_options_chain') */
            console.log(params)
            if (params.cod_symbol_contrato == "" && params.cod_subyacente == "") {
                console.log(params)
                return;
            }

            let contrato_opcion_api = new ContratoOpcion()

            let response = contrato_opcion_api.get_cadena_de_opciones({
                contract: params.cod_symbol_contrato,
                cod_symbol: params.cod_subyacente,
                fch_expiracion: params.fch_expiracion,
                imp_ejercicio: params.imp_ejercicio,
                flg_opciones_vencidas: params.flg_opciones_vencidas
            })

            response.then(httpresponse => {
                HttpResponseHandler.showMessageIfError(httpresponse)

                var appresponse = httpresponse.data
                var appdata = appresponse.data
                console.log(appdata)

                appdata["calls"].forEach(c => {
                    c.fch_vencimiento = date.format(date.parse(c.fch_vencimiento, 'YYYY-MM-DD'), 'DD/MM/YYYY')
                })
                appdata["puts"].forEach(p => {
                    p.fch_vencimiento = date.format(date.parse(p.fch_vencimiento, 'YYYY-MM-DD'), 'DD/MM/YYYY')
                })

                this.calls = appdata["calls"]
                this.puts = appdata["puts"]
                //this.exp_dates = appdata["exp_dates"]
                this.exp_dates = appdata["exp_dates"].map(d => date.transform(d, 'YYYY-MM-DD', 'DD/MM/YYYY'))
                this.strikes = appdata["strikes"]

            }).finally(() => {
                this.dataLoading = false
            })
        },
        get_datos_symbol: function (symbol) {
            this.$http.post('SymbolManager/SymbolFinder/get_datos_symbol', {
                symbol: symbol
            }).then(httpresp => {
                let appresp = httpresp.data
                let appdata = appresp.data
                console.log(appdata)
                this.filter.symbol.value = appdata.symbol
                this.filter.symbol.name = appdata.name
            })
        },
        buy: function (data) {
            //data["trade_type"] = "B"
            this.$emit("option-select", data, "buy")
        },
        sell: function (data) {
            console.log(data)
            data["trade_type"] = "S"
            this.$emit("option-select", data)
        },
        close: function () {
            this.$emit("close")
        },
        validateExpirationDate(val) {
            if (val == "") {
                return true
            }
            return date.isValid(val, 'DD/MM/YYYY') || 'El formato debe ser dd/mm/yyyy'
        }
    }
}
</script>
<style scoped lang="sass">
@import '~quasar/src/css/variables'

tr:hover 
  background-color: $primary;
  color: #ffffff;

</style>