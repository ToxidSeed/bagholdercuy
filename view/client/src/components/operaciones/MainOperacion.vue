<template>
    <div>
        <q-toolbar class="text-blue-10">
            <q-btn flat round dense icon="menu"></q-btn>
            <q-toolbar-title>
                Operaciones
            </q-toolbar-title>
        </q-toolbar>
        <q-toolbar class="q-pa-none">
            <q-btn class="text-capitalize" flat dense color="blue-10" icon="publish" @click="WinCargaMultiple.open=true">Carga operaciones compra/venta</q-btn>
            <q-btn class="text-capitalize" flat dense color="blue-10" icon="move_down" @click="WinFiltrarOperaciones.open=true">Carga de transferencias</q-btn>
        </q-toolbar>
        
        <TableListaOperaciones
            v-on:ins_row="ins_row_handler"
        />
        <q-dialog v-model="panelTradeVisible">
            <PanelTrade
                v-on:cerrar="panelTradeVisible=false"
                v-bind:prev_oper="num_operacion"
                v-bind:action="action"
            />
        </q-dialog>        
        <WinCargaMultiple v-model="WinCargaMultiple.open"/>
    </div>
</template>
<script>
import TableListaOperaciones from '@/components/operaciones/TableListaOperaciones.vue'
import WinCargaMultiple from '@/components/Holdings/WinCargaMultiple.vue';
import PanelTrade from '@/components/PanelTrade.vue';

export default {
    name:"MainOperacion",
    components:{
        TableListaOperaciones,
        WinCargaMultiple,
        PanelTrade
    },
    data: () => {
        return {
            panelTradeVisible:false,
            num_operacion:"",
            action:"",
            WinCargaMultiple:{
                open:false
            }
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