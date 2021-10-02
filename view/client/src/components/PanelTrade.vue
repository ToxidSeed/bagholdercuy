<template>
    <div>        
        <div>
            <q-card>
                <q-card-section>
                    <div class="text-h6">Order Entry</div>
                </q-card-section>
                <q-separator />
                <q-card-section>
                    <div class="row">
                        <q-btn-group push  unelevated>
                        <q-btn push label="Buy" icon="fas fa-angle-double-left" 
                        :color="order.order_type=='B'?'primary':'white'" 
                        :text-color="order.order_type=='B'?'white':'black'"
                        @click="order.order_type='B'"
                        />
                        <q-btn push label="Sell" icon-right="fas fa-angle-double-right" 
                        :color="order.order_type=='S'?'red':'white'"
                        :text-color="order.order_type=='S'?'white':'black'"
                        @click="order.order_type='S'"
                        />                 
                        </q-btn-group>    
                    </div>                              
                    <div class="row">
                        <div class="col-8">
                        <q-input v-model="symbol_search" label="symbol" ref="symbol" @input="search" debounce="1000">    
                            <template v-slot:after>
                            <q-icon name="search" @click="search" class="cursor-pointer"/>
                            </template>                 
                            <q-popup-proxy v-model="states.symbol_popup" @show="onShowProxy">
                                <div :style="style.symbol_width">
                                <q-list bordered separator>
                                <q-item v-for="item in symbol_list" :key="item.id" clickable v-ripple @click="sel_symbol(item)">
                                    <q-item-section>{{item.symbol}}-{{item.name}}</q-item-section>
                                </q-item>                       
                                </q-list>
                                </div>
                            </q-popup-proxy>
                        </q-input>
                        </div>
                        <div class="col-4 q-pl-xs">
                            <q-select v-model="order.asset_type" :options="asset_type_list" label="asset type" />                 
                        </div>
                    </div>
                    <div class="q-pt-xs">{{order.symbol_name}}</div>
                    <div class="row">
                        <div class="col-6">
                            <q-input v-model="order.quantity" label="quantity" type="number" input-class="text-right"/>
                        </div>
                        <div class="col-6 q-pl-xs">
                            <q-input v-model="order.price" label="price" type="number" input-class="text-right"/>
                        </div>
                    </div>
                    <div class="row">
                        <q-input class="col-6"
                        v-model="order.order_date"                  
                        stack-label label="order date" 
                        mask="##/##/####" 
                        fill-mask="#"                              
                        >
                            <!--<q-popup-proxy ref="qDateProxy" transition-show="scale" transition-hide="scale">
                            <q-date v-model="order.order_date" mask="YYYY-MM-DD" v-close-popup >                    
                            </q-date>
                            </q-popup-proxy>-->
                        </q-input> 
                    </div>
                </q-card-section>
                <q-separator />
                <q-card-actions >
                    <q-btn  color="green" @click="save">Guardar</q-btn>
                    <q-btn flat>Cerrar</q-btn>
                </q-card-actions>
                <MessageBox ref="msgbox"/>
            </q-card>
        </div>
        <!--
        <PanelOptionsChain class="col-9" v-bind:asset_type="order.asset_type"
            v-on:option-select="option_selected"
        />
        -->
        
    </div>
</template>
<script>

import MessageBox from './MessageBox.vue';
import date from 'date-and-time';
//import PanelOptionsChain from './PanelOptionsChain.vue';
//import { ref } from 'vue'

export default {
    name:"PanelTrade",
    components:{
        MessageBox,
        //PanelOptionsChain
    },
    props:{
        symbol:{
            default:""            
        },
        asset_type:{
            default:""
        },
        order_type:{
            default:""
        },
        update:{
            default:""
        }
    },    
    data:()=>{
        return {
            order:{
                id:"",
                symbol:"",
                symbol_name:"",
                quantity:"",
                price:"",
                order_date:"",
                order_type:"",
                asset_type:"stock"                
            },
            states:{
                symbol_popup:false
            },
            style:{
                symbol_width:""
            },
            symbol_list:[],
            asset_type_list:["stock","options"],
            symbol_search:""            
        }
    },
    watch:{
        update:function(old, value){        
            if (old != value){
                this.order.symbol = this.symbol
                this.order.asset_type = this.asset_type
                this.order.order_type = this.order_type
                this.symbol_search = this.symbol            
            }
        }
    },
    computed:{
        order_date_iso:function(){
            var current_date = date.parse(this.order.order_date, 'DD/MM/YYYY')
            return date.format(current_date, 'YYYY-MM-DD')
        }
    },
    mounted:function(){
        //var var_order_date = new Date().toISOString().substring(0,10)
        var var_order_date = date.format(new Date(), 'DD/MM/YYYY');
                             
        this.order.order_date = var_order_date
        var symbol_witdh = this.$refs.symbol.$el.control.clientWidth
        this.style.symbol_width = "width:"+symbol_witdh+"px";

        //initial values
        this.order.symbol = this.symbol
        this.order.asset_type = this.asset_type
        this.order.order_type = this.order_type
        this.symbol_search = this.symbol
    },
    methods:{
        sel_symbol:function(item){
            this.states.symbol_popup=false
            this.order.symbol = item.symbol
            this.order.symbol_name = item.name
            this.symbol_search = item.symbol
        },
        onShowProxy:function(){
            this.$refs.symbol.focus()
        },
        search:function(){
            if (this.symbol_search == ""){
                return
            }

            this.$http.post(
            this.$backend_url+'DataManager/Symbol/search',{
                symbol:this.symbol_search,
                asset_type:this.order.asset_type
            }).then(httpresponse => {
                var appresponse = httpresponse.data
                this.symbol_list = appresponse.data

                this.states.symbol_popup = true
            });
        },
        save:function(){            
            //order_type
            if (!(this.order.order_type == "B" || this.order.order_type == "S")){
                this.$refs.msgbox.new({
                    title:"Error al guardar",
                    message:"Debe seleccionar un tipo de participación",
                    action:"save"
                })
                return;
            }
            //symbol
            if (this.order.symbol == ""){
                this.$refs.msgbox.new({
                    title:"Error al guardar",
                    message:"Debe seleccionar un símbolo",
                    action:"save"
                })
                return;
            }
            //quantity
            if (parseInt(this.order.quantity) <= 0){
                this.$refs.msgbox.new({
                    title:"Error al guardar",
                    message:"la cantidad de participaciones debe ser mayor a 0",
                    action:"save"
                })
                return;
            }

            //price
            if (parseInt(this.order.quantity) <= 0){
                this.$refs.msgbox.new({
                    title:"Error al guardar",
                    message:"la cantidad de participaciones debe ser mayor a 0",
                    action:"save"
                })
                return;
            }
            //order_date
            if (this.order.order_date == ""){
                this.$refs.msgbox.new({
                    title:"Error al guardar",
                    message:"Debe seleccionar una fecha de transacción",
                    action:"save"
                })
                return;
            }

            //determine if it is buy or sell
            this.do_order();
        },
        option_selected:function(option){
            console.log(option)
            this.order.symbol = option.symbol
            this.symbol_search = option.symbol
            this.order.order_type = option.order_type
        },
        do_order:function(){
            this.$http.post(
            this.$backend_url+'TradeManager/TradeManager/order',{
                symbol:this.order.symbol,
                order_type:this.order.order_type,
                shares_quantity:this.order.quantity,
                price_per_share:this.order.price,
                order_date:this.order_date_iso,
                asset_type:this.order.asset_type             
            }).then(httpresponse => {
                var appresponse = httpresponse.data
                    if (appresponse.success == true){
                        this.$refs.msgbox.new({
                            title:"Información",
                            message:"La orden de compra fue completada con éxito",
                            action:"save-success"
                        })
                    }else{
                        this.$refs.msgbox.new({
                            title:"Error",
                            message:"Error al guardar la orden de compra",
                            action:"save-error"
                        })
                    }
            });
        }
    }
}
</script>