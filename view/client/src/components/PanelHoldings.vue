<template>
    <div>
        <!--<div class="q-ma-md text-h6">Posiciones</div>-->        
        <div class="row">
            <div :class="holdings_table_col">
             <q-tabs
                v-model="tabmodel"
                align="left"
                dense
                class="text-grey"
                active-color="primary"                
            >         
                <q-tab name="overview" icon="fas fa-chart-pie" label="Overview" />   
                <q-tab name="holdings" icon="fas fa-cubes" label="Holdings" />                    
                <q-tab name="options_chain" icon="fas fa-link" label="Options Chain" />    <div class="text-primary">Cash: 10300.75 USD</div>                
            </q-tabs>            
            <q-separator />
            <q-tab-panels v-model="tabmodel">
                <q-tab-panel name="overview">
                    <PanelOverview />
                </q-tab-panel>
                <q-tab-panel name="holdings">                    
                    <q-table
                    title="Posiciones"
                    :data="data"
                    :columns="columns"
                    row-key="name"
                    dense            
                    >
                        <template v-slot:top>
                            <q-btn color="primary" label="Buy" @click="buy()" />                
                            <q-btn color="red" label="Sell" @click="sell()" class="q-ml-xs" />                
                            <q-btn color="green" label="Options Chain" to="/order" class="q-ml-xs" />                
                        </template>
                        <template v-slot:body-cell-symbol="props">
                            <q-menu
                            touch-position
                            context-menu
                            >
                            <q-list dense style="min-width: 100px" >
                                <q-item style="padding: 0px 0px" clickable v-close-popup @click="buy(props.row)">
                                    <q-item-section class="bg-primary text-white"><div class="q-pl-sm">Buy</div></q-item-section>                                    
                                </q-item>
                                <q-item style="padding: 0px 0px" clickable v-close-popup @click="sell(props.row)">
                                    <q-item-section class="bg-red text-white"><div class="q-pl-sm">Sell</div></q-item-section>                                    
                                </q-item>
                            </q-list>
                            </q-menu>
                            <q-td :props="props">                    
                                {{props.value}}
                            </q-td>
                        </template>
                        <template v-slot:body-cell-total_change="props">
                            <q-td :props="props">                    
                                <div v-bind:class="{'text-red':props.row.total_change < 0,'text-green':props.row.total_change >= 0}">
                                    {{props.value}}%
                                </div>
                            </q-td>                
                        </template>
                        <template v-slot:body-cell-total_pl="props">
                            <q-td :props="props">
                                <div v-bind:class="{'text-red':props.row.total_change < 0,'text-green':props.row.total_change >= 0}">
                                    {{props.value}}
                                </div>
                            </q-td>                
                        </template>            
                    </q-table>                        
                 </q-tab-panel>
                 <q-tab-panel name="options_chain">
                     <PanelOptionsChain
                     v-bind:asset_type="order.asset_type"
                     />
                 </q-tab-panel>
            </q-tab-panels>
            </div>         
            <div :class="panel_order_col">  
            <PanelTrade                 
                v-if="open_panel_order"
                v-bind:symbol="order.symbol"
                v-bind:asset_type="order.asset_type"
                v-bind:order_type="order.order_type"
                v-bind:update="order.update"
                v-on:cerrar="open_panel_order=false"                
            />   
            </div>                     
        </div>
    </div>    
</template>
<script>
import PanelTrade from './PanelTrade.vue';
import PanelOptionsChain from './PanelOptionsChain.vue';
import PanelOverview from './PanelOverview.vue';

export default {
    name:"PanelHoldings",
    components:{
        PanelTrade,
        PanelOptionsChain,
        PanelOverview
    },
    data:() =>{
        return {
            tabmodel:"overview",
            order:{
                symbol:"",
                asset_type:"",
                order_type:"",
                update:""
            },
            open_panel_order:false,
            columns:[
                {
                    label:"symbol",
                    align: 'left',
                    field:"symbol",
                    name:"symbol"                              
                },{
                    label:"holding since",
                    align:"left",
                    field:"holding_since",
                    name:"holding_since"
                },
                {
                    label:"P/L",
                    align:"right",
                    field:"total_change",
                    name:"total_change"                    
                },{
                    label:"P/L IMP",
                    align:"right",
                    field:"total_pl",
                    name:"total_pl"                    
                },{
                    label:"shares",
                    align:"left",
                    field:"sum_shares_balance",
                    name:"sum_shares_balance"
                },{
                    label:"avg. price per order",
                    align:"right",
                    field:"avg_buy_price",
                    name:"avg_buy_price"    
                },{
                    label:"last price",
                    align:"right",
                    field:"last_price",
                    name:"last_price"                    
                },{
                    label:"market value",
                    align:"right",
                    field:"market_value",
                    name:"market_value"
                }
            ],            
            data:[]
        }
    },
    computed:{
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
        this.get_list();
    },
    methods:{
        get_list:function(){
            this.$http.post(
            'HoldingsManager/HoldingsManager/get_list',{
            }).then(httpresp =>{
                console.log(httpresp);
                var appresp = httpresp.data
                this.data = appresp.data 
            })
        },
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