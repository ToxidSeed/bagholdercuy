<template>
    <div>
        <TableHistorialOrdenes
            v-on:ins-orden="ins_orden"
        />
        <q-dialog v-model="panelTradeVisible">
            <PanelTrade
                v-on:cerrar="panelTradeVisible=false"
                v-on:btn_opciones_click="abrir_opciones"
                v-bind:ref_num_orden="ref_num_orden"  
                v-bind:insertar="insertar" 
                v-bind:symbol="symbol"
                v-bind:asset_type="asset_type"
                v-bind:order_type="order_type"
                v-bind:order_date="order_date"
            />
        </q-dialog>
        <q-dialog v-model="panelOptionsChain">            
            <q-card style="width: 700px; max-width: 80vw;">
                 <q-card-section class="bg-primary text-white">
                    <div class="text-h6">Seleccionar Contrato</div>        
                </q-card-section>
                <PanelOptionsChain/>
            </q-card>
        </q-dialog>        
    </div>
</template>
<script>
import TableHistorialOrdenes from '@/components/Ordenes/TableHistorialOrdenes.vue'
import PanelTrade from '@/components/PanelTrade.vue';
import PanelOptionsChain from '@/components/PanelOptionsChain.vue'

export default {
    name:"MainPanelHistorialOrdenes",
    components:{
        TableHistorialOrdenes,
        PanelTrade,
        PanelOptionsChain
    },
    data: () => {
        return {
            panelTradeVisible:false,
            panelOptionsChain:false,
            ref_num_orden:"",
            insertar:"",
            symbol:"",
            asset_type:"",
            order_type:"",
            order_date:""
        }
    },
    methods:{
        ins_orden:function(lugar,row){
            console.log(lugar)
            this.ref_num_orden = row.num_orden
            this.insertar = lugar
            this.symbol = row.symbol
            this.asset_type = row.asset_type
            this.order_date = row.order_date         
            this.panelTradeVisible = true
        },
        abrir_opciones:function(symbol){
            console.log(symbol)
            this.panelOptionsChain = true
        }

    }
}
</script>