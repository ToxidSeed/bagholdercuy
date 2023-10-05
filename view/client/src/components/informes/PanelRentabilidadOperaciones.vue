<template>
    <div>
        <q-toolbar class="text-blue-10">
            <q-btn flat round dense icon="menu" />
            <q-toolbar-title>
                Rentabilidad de Operaciones
            </q-toolbar-title>
            <q-btn flat round dense icon="more_vert" />                                        
        </q-toolbar>
        <PanelRentabilidadOperacionesFecha class="q-pb-sm"/>
        <!--<q-toolbar>
            <q-btn icon="filter_alt" label="Filtrar" class="text-capitalize" flat dense color="blue-10"/>
        </q-toolbar>-->
        <router-view></router-view>
    </div>
</template>
<script>
import PanelRentabilidadOperacionesFecha from "@/components/informes/PanelRentabilidadOperacionesFecha.vue"

export default {
    name:"PanelRentabilidadOperaciones",
    components:{
        PanelRentabilidadOperacionesFecha
    }
}
</script>