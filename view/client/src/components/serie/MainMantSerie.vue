<template>
    <div>
        <q-splitter
            v-model="visible"
            :limits="[0,100]"
            style="height:100hr"
        >
            <template v-slot:before>
                <PanelSerieLoader class="q-pl-xs q-pb-xs"/>
            </template>
            <template v-slot:after>
                <q-toolbar>                    
                    <q-btn class="q-ml-xs" color="blue-10" dense icon="menu" flat>
                        <q-menu>
                            <q-list dense>
                                <q-item clickable v-close-popup @click="visible=30">
                                    <q-item-section class="text-subtitle1">
                                        <div>Carga de series desde <span class="text-blue-10 text-bold">iexcloud</span></div>
                                    </q-item-section>                            
                                </q-item>
                            </q-list>
                        </q-menu>
                    </q-btn>
                    <q-toolbar-title class="text-blue-10">Series</q-toolbar-title>
                </q-toolbar>
                <TableResumenSerie  class="q-pl-xs q-pb-xs"/>
            </template>
        </q-splitter>        
    </div>
</template>
<script>
import TableResumenSerie from '@/components/serie/TableResumenSerie.vue'
import PanelSerieLoader from '@/components/serie/PanelSerieLoader.vue'
export default {
    name:"MainMantSerie",
    components:{
        TableResumenSerie,
        PanelSerieLoader
    },
    data: () => {
        return {
            visible:0
        }
    }
}
</script>