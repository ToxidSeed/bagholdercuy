<template>
    <div class="row">
        <q-toolbar class="bg-white">
            <q-btn label="filtrar" icon="filter_alt" color="blue-10" dense flat class="text-capitalize"/>                
        </q-toolbar>
        <div class="col-2">
            <TableRentabilidadOperacionesDiaria/>
        </div>
        <div class="col-10 q-pl-xs">
            <ChartRentabilidadOperacionesDiaria/>
        </div>
    </div>
</template>
<script>
import TableRentabilidadOperacionesDiaria from "@/components/informes/TableRentabilidadOperacionesDiaria.vue"
import ChartRentabilidadOperacionesDiaria from "@/components/informes/ChartRentabilidadOperacionesDiaria.vue"

export default {
    name:"PanelRentabilidadOperacionesDiaria",
    components:{
        TableRentabilidadOperacionesDiaria,
        ChartRentabilidadOperacionesDiaria
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