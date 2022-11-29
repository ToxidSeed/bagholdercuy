<template>
    <div>                
        <q-splitter
            v-model="firstPanelSize"
            :limits="[0,100]"
            style="height:100hr"
            >            
            <template v-slot:before>
                <router-view 
                    v-on:open="open_handler"
                    v-on:close="close_handler" 
                    v-on:procesar-fin="procesar_fin_handler"         
                    >                      
                </router-view>
            </template>
            <template v-slot:after >            
                <TableCurrencyExchanges v-bind:in_filter="filter"/>       
            </template>
        </q-splitter>
        <!--<div class="col-12">     
            <div class="q-ma-sm">
                <q-btn label="Nuevo" color = "primary" @click="win_currexchange_open=true"/>
                <q-btn class="q-ml-sm" label="Loader" color="green" @click="win_loader_open=true"/>
            </div>
            
        </div>-->
        <!--<q-dialog v-model="win_currexchange_open">
            <PanelCurrencyExchangeRate
                v-on:conversion-moneda-cancel="win_currexchange_open=false"
            />
        </q-dialog>    
        <q-dialog v-model="win_loader_open">
            <PanelCurrencyExchangeRateHistLoader
                v-on:btn_cancelar_click="win_loader_open=false"
            />
        </q-dialog>-->                
    </div>
</template>
<script>
//import PanelCurrencyExchangeRate from './PanelCurrencyExchangeRate.vue'
//import { number } from '@amcharts/amcharts4/core';
import TableCurrencyExchanges from './TableCurrencyExchangeRates.vue'
//import PanelCurrencyExchangeRateLoader from './PanelCurrencyExchangeRateLoader.vue'

export default {
    name:"MainPanelCurrencyExchange",
    components:{
        //PanelCurrencyExchangeRate,
        TableCurrencyExchanges/*,
        PanelCurrencyExchangeRateHistLoader*/
    },
    props:{
        inFirstPanelSize:{
            type:Number,
            default:0
        }
    },
    data: () => {
        return {
            firstPanelSize:0,
            /*maintabs:"pnl_currency_exchange_rate",
            win_currexchange_open:false,
            win_loader_open:false,*/
            filter:{
                updtime:""
            }
        }
    },
    mounted:function(){
        this.init()        
    },
    watch:{
        inFirstPanelSize:function(newval){                   
            this.firstPanelSize = newval
        }
    },
    methods:{
        init:function(){            
            /*console.log(this.child)
            if (this.child.mounted){
                this.firstPanelSize = this.child.size
            }else{
                this.firstPanelSize = this.inFirstPanelSize
            }    */        
        },        
        open_handler:function(size){            
            this.firstPanelSize = size
        },
        close_handler:function(){
            this.firstPanelSize = 0
        },
        procesar_fin_handler:function(){
            this.filter.updtime = Date.now()
        }
    }
}
</script>