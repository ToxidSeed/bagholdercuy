<template>
    <div class="row">
        <q-toolbar class="bg-white">
            <q-toolbar-title class="text-blue-10">Rentabilidad Anual</q-toolbar-title>
            <q-btn label="filtrar" icon="filter_alt" color="blue-10" dense flat class="text-capitalize"/>                
        </q-toolbar>
        <div class="col-2">
            <TableRentabilidadOperacionesAnual/>
        </div>
        <div class="col-10 q-pl-xs">
            <ChartRentabilidadOperacionesAnual/>
        </div>
    </div>
</template>
<script>
import TableRentabilidadOperacionesAnual from "@/components/operaciones/rentabilidadanual/TableRentabilidadOperacionesAnual.vue"
import ChartRentabilidadOperacionesAnual from "@/components/operaciones/rentabilidadanual/ChartRentabilidadOperacionesAnual.vue"

export default {
    name:"MainRentabilidadOperacionesAnual",
    components:{
        TableRentabilidadOperacionesAnual,
        ChartRentabilidadOperacionesAnual
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