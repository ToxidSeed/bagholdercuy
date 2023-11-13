<template>
    <div>
        <q-toolbar class="text-blue-10">
            <q-btn flat round dense icon="menu">
                <q-menu>
                    <q-list dense>
                        <q-item clickable v-close-popup :to="{name:'rentabilidad-diario-opciones'}">
                            <q-item-section class="text-subtitle1">
                                <div>Rentabilidad <span class="text-blue-10 text-bold">Diaria</span> de opciones</div>
                            </q-item-section>                            
                        </q-item>
                        <q-item clickable v-close-popup :to="{name:'rentabilidad-mensual-opciones'}">
                            <q-item-section class="text-subtitle1">
                                <div>Rentabilidad <span class="text-blue-10 text-bold">Semanal</span> de opciones</div>
                            </q-item-section>                            
                        </q-item>
                        <q-item clickable v-close-popup :to="{name:'rentabilidad-semanal-opciones'}">
                            <q-item-section class="text-subtitle1">
                                <div>Rentabilidad <span class="text-blue-10 text-bold">Mensual</span> de opciones</div>
                            </q-item-section>                            
                        </q-item>                                                     
                    </q-list>
                </q-menu>
            </q-btn>
            <q-toolbar-title>
                Simulacion de rentabilidad
            </q-toolbar-title>
            <q-btn flat round dense icon="more_vert" />                                        
        </q-toolbar>   
        <router-view></router-view>
    </div>
</template>
<script>
export default {
    name:"PanelSimulacionRentabilidad",
    components:{
        
    }
}
</script>