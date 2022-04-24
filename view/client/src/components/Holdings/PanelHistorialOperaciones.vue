<template>
    <div>
        <TableHistorialOperaciones
            v-on:ins_row="ins_row_handler"
        />
        <q-dialog v-model="panelTradeVisible">
            <PanelTrade
                v-on:cerrar="panelTradeVisible=false"
            />
        </q-dialog>        
    </div>
</template>
<script>
import TableHistorialOperaciones from '@/components/Holdings/TableHistorialOperaciones.vue'
import PanelTrade from '@/components/PanelTrade.vue';

export default {
    name:"PanelHistorialOperaciones",
    components:{
        TableHistorialOperaciones,
        PanelTrade
    },
    data: () => {
        return {
            panelTradeVisible:false
        }
    },
    methods:{
        ins_row_handler:function(prev_row){
            console.log(prev_row)
            this.panelTradeVisible = true
        }
    }
}
</script>