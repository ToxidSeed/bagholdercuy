<template>
    <div>
        <TableHistorialOperaciones
            v-on:ins_row="ins_row_handler"
        />
        <q-dialog v-model="panelTradeVisible">
            <PanelTrade
                v-on:cerrar="panelTradeVisible=false"
                v-bind:prev_oper="num_operacion"
                v-bind:action="action"
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
            panelTradeVisible:false,
            num_operacion:"",
            action:""
        }
    },
    methods:{
        ins_row_handler:function(prev_row){            
            this.panelTradeVisible = true
            this.num_operacion = prev_row.num_operacion
            this.action = "insertar"
        },
        sin_accion:function(){
            this.num_operacion = ""
            this.action = ""
        }
    }
}
</script>