<template>
    <div class="row">
        <q-toolbar class="bg-white">
            <q-toolbar-title class="text-blue-10">Rentabilidad Mensual</q-toolbar-title>
            <q-btn label="filtrar" icon="filter_alt" color="blue-10" dense flat class="text-capitalize"/>                
        </q-toolbar>
        <div class="col-2">
            <TableRentabilidadOperacionesSemanal/>
        </div>
        <div class="col-10 q-pl-xs">
            <ChartRentabilidadOperacionesSemanal/>
        </div>
    </div>
</template>
<script>
import TableRentabilidadOperacionesSemanal from "@/components/operaciones/rentabilidadsemanal/TableRentabilidadOperacionesSemanal.vue"
import ChartRentabilidadOperacionesSemanal from "@/components/operaciones/rentabilidadsemanal/ChartRentabilidadOperacionesSemanal.vue"

export default {
    name:"MainRentabilidadOperacionesSemanal",
    components:{
        TableRentabilidadOperacionesSemanal,
        ChartRentabilidadOperacionesSemanal
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