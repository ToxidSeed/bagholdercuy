<template>
    <q-card>
        <q-toolbar class="text-blue-10">
            <q-btn flat round dense icon="call_to_action" />
            <q-toolbar-title>
                Evolución Semanal
            </q-toolbar-title>            
        </q-toolbar>
        <div class="row">
            <ChartEvolucionSemanal v-bind:infiltros="filtros" class="col-6"/>
            <TableEvolucionSemanal v-bind:infiltros="filtros" class="col-6"/>            
        </div>        
    </q-card>
</template>
<script>
import ChartEvolucionSemanal from '@/components/informes/ChartEvolucionSemanal.vue';
import TableEvolucionSemanal from '@/components/informes/TableEvolucionSemanal.vue';

export default {
    name:"PanelEvolucionSemanal",
    components:{
        ChartEvolucionSemanal,
        TableEvolucionSemanal
    },
    props:{
        infiltros:{
            type:Object,
            default: () => {}
        }
    },
    watch:{
        infiltros:function(newval){                        
            this.filtros = newval                        
        }
    },
    data(){
        return {
            filtros:{}
        }
    },
    mounted:function(){
        this.filtros = this.infiltros
    }
}
</script>