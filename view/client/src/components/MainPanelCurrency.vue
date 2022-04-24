<template>
    <div class="row">
        <div class="col-3">
            <q-card>
                <!--<q-card-section style="border:1px solid black;">-->
                <q-card-section class="q-pa-none">
                    <q-tabs
                        v-model="tab"
                        class="text-primary"
                        align="left"
                        dense                        
                    >
                        <q-tab name="currency"  label="Moneda" />
                        <q-tab name="pairs" label="Pares" />
                    </q-tabs>
                    <q-tab-panels v-model="tab" animated>
                        <q-tab-panel name="currency" class="q-pa-none">
                            <PanelCurrency 
                            ref="PanelCurrency" 
                            v-on:panel-close="pnl_currecy_close_handler"
                            v-on:symbol-changed="pnl_currency_symbol_changed_handler"  
                            v-bind:in_data="pnl_currency_data"                
                            />
                        </q-tab-panel>
                        <q-tab-panel name="pairs">
                            <PanelAddPair 
                            v-bind:in_currency_base_symbol=currency_symbol
                            v-on:add-pair-btn-click="add_pair_btn_click_handle"
                            />
                            <TablePairs ref="TablePairs" class="q-pt-xs"      
                            v-bind:in_data="tbl_pairs_data"
                            v-bind:in_currency_base_symbol="currency_symbol"
                            v-on:panel-close="tbl_pairs_close_handler"
                            />
                        </q-tab-panel>
                    </q-tab-panels>
                </q-card-section>
                <q-card-actions align="right">
                    <q-btn color="primary" @click="btn_save_click_handler">Guardar</q-btn>
                    <q-btn color="orange">Cancelar</q-btn>                
                </q-card-actions>
            </q-card>
        </div>
        <div class="col-9">
            <TableCurrency/>
        </div>        
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>

import PanelCurrency from './PanelCurrency.vue'
import TablePairs from './TablePairs.vue'
import TableCurrency from './TableCurrency.vue'
import PanelAddPair from './PanelAddPair.vue'
import MessageBox from './MessageBox.vue'

export default {
    name:"MainPanelCurrency",
    components:{
        PanelCurrency,
        TablePairs,
        TableCurrency,
        PanelAddPair,
        MessageBox
    },
    data:() => {
        return {
            tab:"currency",            
            currency_symbol:"",
            pnl_currency_data:{},
            tbl_pairs_data:{}
        }
    },
    methods:{        
        pnl_currency_symbol_changed_handler:function(data){    
            console.log("trigger")                    
            this.currency_symbol = data.new
            this.tbl_pairs_data = {}
        },
        btn_save_click_handler:function(){                        
            var pairs = this.get_pairs_data()
            var currency_data = this.get_currency_data()      
            
            this.$http.post('CurrencyManager/CurrencyManager/save',{
                currency_id: currency_data.currency_id,
                currency_symbol: currency_data.symbol,
                currency_name: currency_data.currency_name,
                currency_desc: "",
                //pairs_to_add:pairs.pairs_to_add,
                pairs_to_remove:pairs.pairs_to_delete
            }).then(httpresponse => {                
                //guardar resultado
                console.log(JSON.parse(httpresponse.config.data))
                var appresp = httpresponse.data
                console.log(appresp.message)
                console.log(appresp.errors)
                console.log(appresp)
                this.$refs.msgbox.new(appresp)
                
            })
        },
        tbl_pairs_close_handler:function(data){
            this.tbl_pairs_data = data.data
        },
        pnl_currecy_close_handler:function(data){
            this.pnl_currency_data = data           
            this.currency_symbol = data.symbol  
        },
        add_pair_btn_click_handle:function(data){
            this.$refs.TablePairs.add_pair(data)
        },
        get_currency_data(){
            var currency_data = this.pnl_currency_data
            //check if exist PanelCurrency
            if (this.$refs.PanelCurrency != undefined){
                currency_data = this.$refs.PanelCurrency.get_currency_data()
            }
            return currency_data
        },
        get_pairs_data:function(){
            var pairs = {
                pairs_to_add:[],
                pairs_to_delete:[]
            }

            console.log(this.tbl_pairs_data)
            if (Object.keys(this.tbl_pairs_data) == true){                
                pairs.pairs_to_add = this.tbl_pairs_data.data
                pairs.pairs_to_delete = this.tbl_pairs_data.deleted_records
            }

            if(this.$refs.TablePairs != undefined){
                var currpairs = this.$refs.TablePairs.get_pairs_data()                
                pairs.pairs_to_add = currpairs.data
                pairs.pairs_to_delete = currpairs.deleted_records
            }
            console.log(pairs)
            return pairs
        }
    }
}
</script>