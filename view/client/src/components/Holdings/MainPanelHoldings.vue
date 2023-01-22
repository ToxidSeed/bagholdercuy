<template>
    <div>
        <q-toolbar class="text-blue-10">
            <q-btn flat round dense icon="menu"></q-btn>
            <q-toolbar-title>
                Holdings
            </q-toolbar-title>
        </q-toolbar>
        <q-splitter
            v-model="first_panel_size"
            :limits="[0,100]"
            style="height:100hr"
            >
            <template v-slot:before>
                <router-view
                v-on:open="open_handler">                    
                </router-view>
            </template>
            <template v-slot:after >
                <TableHoldings/>
            </template>
        </q-splitter>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import TableHoldings from '@/components/Holdings/TableHoldings.vue';
import MessageBox from '@/components/MessageBox.vue';
export default {
    name:"PanelHoldings",
    components:{
        //PanelTrade,
        //-->PanelResumen,
        //PanelOptionsChain,
        TableHoldings,
        MessageBox        
    },
    data:() =>{
        return {
            first_panel_size:0,
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
        },
        open_handler:function(size){
            this.first_panel_size = size
        }
    }
}
</script>