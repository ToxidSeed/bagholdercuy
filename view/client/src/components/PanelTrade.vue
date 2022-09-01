<template>
    <div>
        <q-card>
            <q-card-section>
                <div class="row">
                    <div class="text-h6 text-primary">Order Entry</div>
                    <q-space/>
                    <q-btn color="primary" @click="btn_opciones_click" :disable="btn_opciones_disable">Opciones</q-btn>         
                </div>            
                <!--<div v-show="ref_num_orden_visible">Insertar {{insertar}} de la Orden: <span class="text-primary">{{ref_num_orden}}</span></div>-->
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
                    <div class="col-3 q-pl-xs">
                        <q-input class="col-3"
                        v-model="order.order_date"                  
                        stack-label label="Order date" 
                        mask="##/##/####" 
                        fill-mask=""                              
                        >
                            <!--<q-popup-proxy ref="qDateProxy" transition-show="scale" transition-hide="scale">
                            <q-date v-model="order.order_date" mask="YYYY-MM-DD" v-close-popup >                    
                            </q-date>
                            </q-popup-proxy>-->
                        </q-input>                    
                    </div>
                    <div class="col-9 q-pl-xs">
                        <q-input v-model="symbol_search" label="symbol" ref="symbol" 
                        @input="search" debounce="1000">    
                            <template v-slot:after>
                            <q-icon name="search" @click="search" class="cursor-pointer"/>
                            </template>
                            <q-popup-proxy v-model="states.symbol_popup" @show="onShowProxy">
                                <!--<div :style="style.symbol_width">-->
                                    <q-list bordered separator>
                                    <q-item v-for="item in symbol_list" :key="item.id" clickable v-ripple @click="sel_symbol(item)">
                                        <q-item-section>{{item.symbol}}-{{item.name}}</q-item-section>
                                    </q-item>
                                    </q-list>
                                <!--</div>-->
                            </q-popup-proxy>
                        </q-input>
                    </div>                
                </div>
                <div class="q-pt-xs text-h6 text-bold text-deep-purple">{{symbol_info}}</div>
                <div class="q-pt-xs">{{symbol_info_desc}}</div>
                <div class="row">
                    <div class="col-5">
                        <q-input stack-label  v-model="order.quantity" label="Cantidad" type="number" input-class="text-right"/>
                    </div>                
                    <div class="col-5 q-pl-xs">
                        <q-input stack-label  v-model="order.price" label="Precio" type="number" input-class="text-right"/>
                    </div>
                    <div class="col-2 q-pl-xs">
                        <q-input stack-label label="Moneda" readonly v-model="order.moneda_id"/>
                    </div>
                </div>            
            </q-card-section>
            <q-separator />
            <q-card-actions align="right">
                <q-btn  color="green" @click="save">Guardar</q-btn>
                <q-btn flat @click="cerrar">Cerrar</q-btn>
            </q-card-actions>
            <MessageBox ref="msgbox"/>
        </q-card> 
        <q-dialog v-model="win_opciones.visible">
            <PanelOptionsChain
                v-bind:symbol_val="order.symbol"
                v-bind:symbol_name="order.symbol_name"
                v-on:option-select="option_selected"
                v-on:close="win_opciones.visible=false"
                v-on:sel-contract="option_selected"
            />
        </q-dialog>        
    </div>
</template>
<script>

import MessageBox from './MessageBox.vue';
import date from 'date-and-time'
import PanelOptionsChain from './PanelOptionsChain.vue';
import {CLIENT_DATE_FORMAT} from '@/common/constants.js'

export default {
    name:"PanelTrade",
    components:{
        MessageBox,
        PanelOptionsChain
    },
    props:{
        ref_num_orden:{
            default:""
        },
        insertar:{
            default:""
        },
        symbol:{
            default:""            
        },
        asset_type:{
            default:""
        },
        order_type:{
            default:"B"
        },
        order_date:{
            type:String,
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
                contrato:"",
                contrato_desc:"",
                symbol_name:"",
                quantity:"",
                price:"",
                order_date:"",
                order_type:"",
                asset_type:""                
            },
            states:{
                symbol_popup:false
            },
            style:{
                symbol_width:""
            },
            symbol_list:[],
            asset_type_list:["stock","options"],
            symbol_search:"",
            btn_opciones:{
                disable:true
            },
            win_opciones:{
                visible:false
            }            
        }
    },
    watch:{
        /*update:function(old, value){        
            if (old != value){
                this.order.symbol = this.symbol
                this.order.asset_type = this.asset_type
                this.order.order_type = this.order_type
                this.symbol_search = this.symbol            
            }
        }*/
        symbol:function(newval){                        
            this.order.symbol = newval
            this.symbol_search = newval
            this.get_datos_symbol()
        }
    },
    computed:{      
        /*order_date_iso:function(){            
            return date.format_to_iso(this.order.order_date,"DD/MM/YYYY")
            
        },*/
        ref_num_orden_visible:function(){
            return this.ref_num_orden.length==0?false:true;            
        },
        btn_opciones_disable:function(){            
            return this.order.symbol==""?true:false;
        },
        symbol_info:function(){
            return this.order.contrato==""?this.order.symbol:this.order.contrato;
        },
        symbol_info_desc:function(){
            return this.order.contrato_desc==""?this.order.symbol_name:this.order.contrato_desc;
        }
    },
    mounted:function(){
        console.log('mounted')
        //var var_order_date = new Date().toISOString().substring(0,10)
        //var var_order_date = date.format(new Date(), 'DD/MM/YYYY');                
        if (this.order_date != ""){
            this.order.order_date = this.order_date
        }else{
            this.order.order_date = date.format(new Date(), CLIENT_DATE_FORMAT);
        }
        
        var symbol_witdh = this.$refs.symbol.$el.control.clientWidth
        this.style.symbol_width = "width:"+symbol_witdh+"px";

        //initial values
        this.order.symbol = this.symbol
        this.order.asset_type = this.asset_type
        this.order.order_type = this.order_type
        this.symbol_search = this.symbol
        //
        //this.get_datos_symbol()

    },
    methods:{        
        onShowProxy:function(){
            this.$refs.symbol.focus()
        }/*,
        get_datos_symbol:function(){
            this.$http.post(
                'SymbolManager/SymbolFinder/get_datos_symbol',{
                    symbol:this.order.symbol
                }
            ).then(httpresp => {
                let appresp = httpresp.data
                if(appresp.success == false){
                    this.$refs.msgbox.httpresp(httpresp)                    
                    return
                }
                console.log(appresp)
                //
                let data = appresp.data                
                if(data.stock != undefined){
                    this.order.symbol_name = data.stock.symbol
                    this.order.moneda_id = data.stock.moneda_id   
                }
                if(data.contrato != undefined){
                    this.order.symbol_name = data.stock.symbol
                    this.order.moneda_id = data.stock.moneda_id
                }
            })
        }*/,
        search:function(){
            console.log(new Date())
            if (this.symbol_search == ""){
                return
            }
            this.$http.post(    
            'SymbolManager/SymbolFinder/buscar_por_texto',{
                texto:this.symbol_search
            }).then(httpresponse => {
                console.log(httpresponse)
                var appresponse = httpresponse.data
                this.symbol_list = appresponse.data
                this.states.symbol_popup = true
            });
        },
        save:function(){            
            console.log('save')
            //order_type
            if (!(this.order.order_type == "B" || this.order.order_type == "S")){
                this.$refs.msgbox.new({
                    title:"Error al guardar",
                    message:"Debe seleccionar un tipo de operacion",
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
            console.log('befoew-sav')
            this.do_order();
        },
        cerrar:function(){
            this.$emit("cerrar")
        },
        sel_symbol:function(item){            
            this.states.symbol_popup=false
            this.order.symbol = item.symbol
            this.order.symbol_name = item.name
            this.order.moneda_id = item.moneda_id
            this.symbol_search = item.symbol
        },
        option_selected:function(option, order_type){
            
            this.win_opciones.visible = false
            //this.order.symbol = 
            this.order.contrato = option.symbol
            this.order.contrato_desc = option.description
            //this.symbol_search = option.symbol
            //this.order.symbol_name = option.description
            if(this.order.order_type == ""){
                this.order.order_type = order_type=="buy"?"B":"S";    
            }                        
        },
        do_order:function(){      
            let symbol = this.order.contrato==""?this.order.symbol:this.order.contrato;
            
            this.$http.post(
            'OrdenManager/ProcesadorEntryPoint/procesar',{
                ref_num_orden:this.ref_num_orden,
                insertar:this.insertar,
                symbol:symbol,
                order_type:this.order.order_type,
                shares_quantity:this.order.quantity,
                price_per_share:this.order.price,
                order_date:this.order.order_date
            }).then(httpresp => {
                this.$refs.msgbox.httpresp(httpresp)                   
            });
        },
        btn_opciones_click:function(){
            let symbol = this.symbol
            let text = this.symbol_search

            if(symbol == text){
                text = ""
            }
            if (symbol != text && text != ""){
                symbol = ""
            }
            this.win_opciones.visible=true

            /*this.$emit(
                'btn_opciones_click',symbol, text
            )*/
        }
    }
}
</script>