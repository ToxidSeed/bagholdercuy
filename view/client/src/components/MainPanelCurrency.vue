<template>
    <div class="row">
        <div class="col-6" v-show="data_panel_show">
            <q-card>
                <!--<q-card-section style="border:1px solid black;">-->
                <q-card-section class="q-pa-none">
                    <div class="row">                    
                        <div class="col-6">
                            <PanelCurrency 
                            ref="PanelCurrency"                             
                            v-on:symbol-changed="pnl_currency_symbol_changed_handler"                              
                            v-bind:in_moneda_id="moneda_id"              
                            />
                        </div>
                        <div class="col-6 q-pa-md">
                            <div class="text-bold text-primary">PARES</div>
                            <PanelAddPair 
                            v-bind:moneda_id=moneda_id
                            v-on:add-par-end="add_par_end_handler"
                            />
                            <TablePairs ref="TablePairs" class="q-pt-xs"      
                            v-bind:in_data="tbl_pairs_data"
                            v-bind:moneda_id="moneda_id"                            
                            />
                        </div>
                    </div>                    
                </q-card-section>
                <q-card-actions align="right">
                    <q-btn color="primary" @click="btn_save_click_handler">Guardar</q-btn>
                    <q-btn color="orange" label="Cancelar" to="/currency"/>
                </q-card-actions>
            </q-card>
        </div>
        <div class="col-6 q-pl-xs">
            <TableCurrency ref="TableCurrency"
            v-on:row-dblclick="tbl_moneda_row_dblclick"
            />
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
    props:{
        action:{
            type:String,
            default:""
        },
        moneda_id:{
            type:String,
            default:""
        }
    },
    data:() => {
        return {
            tab:"currency", 
            //moneda_id:"",           
            currency_symbol:"",
            tbl_pairs_data:{}
        }
    },
    computed:{
        edit_disable:function(){
            if (this.moneda_id == ""){
                return false
            }else{
                return true
            }
        },
        data_panel_show:function(){
            console.log(this.action)
            if (this.action == ""){
                return false
            }else{
                return true
            }
        }
    },
    methods:{        
        pnl_currency_symbol_changed_handler:function(data){    
            console.log("trigger")                    
            this.currency_symbol = data.new
            this.tbl_pairs_data = {}
        },
        btn_save_click_handler:function(){      
            console.log(this.$refs.PanelCurrency)                       
            let moneda_id = this.$refs.PanelCurrency.moneda_id
            let codigo_iso = this.$refs.PanelCurrency.codigo_iso
            let nombre = this.$refs.PanelCurrency.nombre
            let simbolo = this.$refs.PanelCurrency.simbolo
            let descripcion = this.$refs.PanelCurrency.descripcion
            
            this.$http.post('CurrencyManager/CurrencyManager/save',{
                moneda_id: moneda_id,
                codigo_iso: codigo_iso,
                nombre: nombre,
                simbolo: simbolo,
                descripcion: descripcion
            }).then(httpresponse => {                        
                this.$emit('save-finish')
                this.$refs.msgbox.httpresp(httpresponse)
                let appdata = httpresponse.data                
                let extradata = appdata.extradata
                if (extradata != null){
                    this.moneda_id = extradata.moneda_id
                    this.$router.push("/currency/edit="+extradata.moneda_id)
                }                
            })
        },
        add_pair_btn_click_handle:function(data){
            this.$refs.TablePairs.add_pair(data)
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
        },
        tbl_moneda_row_dblclick:function(row){
            this.moneda_id = row.moneda_id            
        },
        add_par_end_handler:function(){
            this.$refs.TablePairs.actualizar_lista()
        }
    },
    beforeRouteEnter(to, from, next){        
        let actions = ["new","edit","view"]
        if (to.params.action != undefined){
            const action = actions.find(element => element == to.params.action)
            console.log(action)
            if (action == undefined){
                console.log("action")
                console.log(from)
                next(false)
            }else{
                next()  
            }
        }else{
            next()
        }                
    },
    beforeRouteUpdate(to, from, next){
        console.log(to)
        console.log(from)
        console.log(next)
        next()
    }
}
</script>