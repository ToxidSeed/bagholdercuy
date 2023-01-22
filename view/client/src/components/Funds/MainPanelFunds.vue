<template>
    <div>                
        <div  class="row"  >
            <q-toolbar class="text-blue-10">
                <q-btn flat round dense icon="menu">
                    <q-menu>
                        <q-list style="min-width: 100px" dense>
                            <q-item clickable v-close-popup :to="{name:'funds-deposito'}">
                                <q-item-section>Deposito</q-item-section>
                            </q-item>                         
                            <q-item clickable v-close-popup :to="{name:'funds-retiro'}">
                                <q-item-section>Retiro</q-item-section>
                            </q-item>                 
                            <q-item clickable v-close-popup :to="{name:'funds-conversion'}">
                                <q-item-section>Conversion</q-item-section>
                            </q-item>                     
                            <q-item clickable v-close-popup :to="{name:'funds-recalcular'}">
                                <q-item-section>Recalcular</q-item-section>
                            </q-item>                     
                            <q-item clickable v-close-popup :to="{name:'funds-reorganizar'}">
                                <q-item-section>Reorganizar</q-item-section>
                            </q-item>                         
                        </q-list>
                    </q-menu>
                </q-btn>
                <q-toolbar-title>
                    Fondos
                </q-toolbar-title>
                <q-btn flat round dense icon="more_vert" />
            </q-toolbar>
            <q-card v-for="item in balance" :key="item.moneda" class="q-ml-sm q-mt-sm q-mb-sm">
                <q-card-section class="col-1 q-pa-sm" bordered>  
                    <span>Cash {{item.moneda}}</span>                                  
                    <div class="text-h5 text-blue-10 text-center q-ma-sm">{{item.importe}}</div>
                </q-card-section>            
            </q-card>
            <!--
            <q-card class="q-ml-sm q-mt-sm q-mb-sm">
                <q-card-section class="col-1 q-pa-sm" bordered>  
                    <span>Cash USD</span>                                  
                    <div class="text-h5 text-blue-10 text-center q-ma-sm" >$6000.00</div>
                </q-card-section>            
            </q-card>
            <q-card class="q-ml-sm q-mt-sm q-mb-sm">
                <q-card-section class="col-1 q-pa-sm">                  
                    <span>Cash EUR</span>                                   
                        <div class="text-h5 text-blue-10 text-center q-ma-sm" >€3000.00</div>
                </q-card-section>
            </q-card>
            -->
        </div>        
        <PanelFunds 
        v-bind:visible="mantvisible"
        v-on:procesar-fin="procesar_fin_handler"
        />
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import PanelFunds from '@/components/Funds/PanelFunds.vue';
import MessageBox from '@/components/MessageBox.vue'
import {postconfig} from '@/common/request.js';
//import TableFundsHistory from '@/components/Funds/TableFundsHistory.vue';

export default {
    name:"MainPanelFunds",
    components:{
        PanelFunds,
        MessageBox
    },
    data: () => {
        return {
            mantvisible:0,
            tab:"Gestion",
            balance:[]
        }
    },
    mounted:function(){
        this.reset()    
        this.get_funds()
    },
    watch:{
        $route:function(){
            this.reset()    
        }
    },
    methods:{
        reset:function(){
            if(this.$route.name!="funds"){
                this.mantvisible = 30
            }else{
                this.mantvisible = 0
            }            
        },
        procesar_fin_handler:function(){
            this.get_funds()
        },
        get_funds:function(){
            this.balance = []

            this.$http.post('FundsManager/FundsManager/get_funds',{
                symbol:""
            },postconfig()).then(httpresp => {
                this.$refs.msgbox.http_resp_on_error(httpresp)
                let appresp = httpresp.data
                if(appresp.success){                     
                    appresp.data.forEach(element => {
                        element.importe = element.importe.toFixed(2)
                        this.balance.push(element)
                    });                    
                }
            })
        }
    }
}
</script>
<style>
.bblue {  
  border: 1px solid rgb(48, 6, 238);
}
</style>