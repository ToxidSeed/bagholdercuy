<template>
    <div>
        <q-toolbar class="text-blue-10">
            <q-btn flat round dense icon="menu">
                <q-menu>
                    <q-list dense>
                        <q-item clickable v-close-popup :to="{name:'rentabilidad-operaciones-diaria'}">
                            <q-item-section class="text-subtitle1">
                                <div>Rentabilidad de operaciones <span class="text-blue-10 text-bold">Diaria</span></div>
                            </q-item-section>                            
                        </q-item>
                        <q-item clickable v-close-popup :to="{name:'rentabilidad-operaciones-semanal'}">
                            <q-item-section class="text-subtitle1">
                                <div>Rentabilidad de operaciones <span class="text-blue-10 text-bold">Semanal</span></div>
                            </q-item-section>                            
                        </q-item>
                        <q-item clickable v-close-popup :to="{name:'rentabilidad-operaciones-mensual'}">
                            <q-item-section class="text-subtitle1">
                                <div>Rentabilidad de operaciones <span class="text-blue-10 text-bold">Mensual</span></div>
                            </q-item-section>                            
                        </q-item>                             
                        <q-item clickable v-close-popup :to="{name:'rentabilidad-operaciones-anual'}">
                            <q-item-section class="text-subtitle1">
                                <div>Rentabilidad de operaciones <span class="text-blue-10 text-bold">Anual</span></div>
                            </q-item-section>                            
                        </q-item>                             
                    </q-list>
                </q-menu>
            </q-btn>
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