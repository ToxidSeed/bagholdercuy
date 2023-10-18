<template>
    <div class="row">
        <q-toolbar class="bg-white">
            <q-toolbar-title class="text-blue-10">Rentabilidad Mensual</q-toolbar-title>
            <q-btn label="filtrar" icon="filter_alt" color="blue-10" dense flat class="text-capitalize"/>                
        </q-toolbar>
        <div class="col-2">
            <TableRentabilidadOperacionesMensual/>
        </div>
        <div class="col-10 q-pl-xs">
            <ChartRentabilidadOperacionesMensual/>
        </div>
    </div>
</template>
<script>
import TableRentabilidadOperacionesMensual from "@/components/operaciones/rentabilidadoperaciones/TableRentabilidadOperacionesMensual.vue"
import ChartRentabilidadOperacionesMensual from "@/components/operaciones/rentabilidadoperaciones/ChartRentabilidadOperacionesMensual.vue"

export default {
    name:"PanelRentabilidadOperacionesDiaria",
    components:{
        TableRentabilidadOperacionesMensual,
        ChartRentabilidadOperacionesMensual
    },
    data(){
        return {

        }
    },
    methods:{
        get_rentabilidad_diaria:function(){
            
        }
    }
}
</script>