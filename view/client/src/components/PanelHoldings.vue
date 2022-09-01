<template>
    <div>
        <!--<div class="q-ma-md text-h6">Posiciones</div>-->        
        <div class="row">
            <div class="col-9">
             <q-tabs
                v-model="tabmodel"
                align="left"
                dense
                class="text-grey"
                active-color="primary"                
            >                         
                <q-tab name="holdings" icon="fas fa-cubes" label="Holdings" />                    
                <q-tab name="options_chain" icon="fas fa-link" label="Options Chain" />                    
            </q-tabs>            
            <q-separator />
            <q-tab-panels v-model="tabmodel">                
                <q-tab-panel name="holdings" class="q-pl-none q-pr-none q-pt-none">                    
                    <TableHoldings/>       
                 </q-tab-panel>
                 <q-tab-panel name="options_chain">
                     <PanelOptionsChain
                     v-bind:asset_type="order.asset_type"
                     />
                 </q-tab-panel>
            </q-tab-panels>
            </div>
            <div class="col-3">
                <PanelResumen/>
            </div>                                                 
            <q-dialog v-model="panel_trade.visible">
                <PanelTrade style="max-width:450px;"
                v-on:cerrar="panel_trade.visible=false"
                />  
            </q-dialog>
        </div>
        <MessageBox ref="msgbox"/>
    </div>    
</template>
<script>
import PanelTrade from './PanelTrade.vue';
import PanelResumen from '@/components/Holdings/PanelResumen.vue';
import PanelOptionsChain from './PanelOptionsChain.vue';
import TableHoldings from '@/components/Holdings/TableHoldings.vue';
import MessageBox from '@/components/MessageBox.vue';
//import PanelOverview from './PanelOverview.vue';

export default {
    name:"PanelHoldings",
    components:{
        PanelTrade,
        PanelResumen,
        PanelOptionsChain,
        TableHoldings,
        MessageBox        
    },
    data:() =>{
        return {
            tabmodel:"holdings",
            order:{
                symbol:"",
                asset_type:"",
                order_type:"",
                update:""
            },
            panel_trade:{
                visible:false
            },            
            open_panel_order:false
        }
    },
    computed:{
        resumen_visible:function(){
            return true
        },     
        holdings_table_col: function () {
        // `this` apunta a la instancia vm
            if (this.open_panel_order == true){
                return "col-9"
            }else{
                return "col-12"
            }
        },
        panel_order_col:function(){
            if (this.open_panel_order == true){
                return "col-3"
            }else{
                return "col-0"
            }
        }
    },
    mounted:function(){
        
    },
    methods:{        
        buy:function(row){     
            this.order.symbol = ""            
            this.open_panel_order = true
            this.order.order_type = "B"
            
            this.order.update = new Date()            
            if (row != undefined){
                this.order.symbol = row.symbol
                this.order.asset_type = row.asset_type
            }else{
                this.order.asset_type = "stock"
            }
        },
        sell:function(row){           
            this.order.symbol = "" 
            this.open_panel_order = true
            this.order.order_type = "S"
            
            this.order.update = new Date()
            if (row != undefined){
                this.order.symbol = row.symbol
                this.order.asset_type = row.asset_type
            }else{
                this.order.asset_type = "stock"
            }
        },
        close:function(){
            this.open_panel_order = false
        }
    }
}
</script>