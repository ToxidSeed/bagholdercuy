<template>
    <div>        
        <q-toolbar>                    
            <q-btn class="q-ml-xs" color="blue-10" dense icon="menu" flat>
                <q-menu>
                    <q-list dense>
                        <q-item clickable v-close-popup :to="{name:'iexcloud-loader'}">
                            <q-item-section class="text-subtitle1">
                                <div>Carga de series desde <span class="text-blue-10 text-bold">iexcloud</span></div>
                            </q-item-section>                            
                        </q-item>
                        <q-item clickable v-close-popup @click="store.abrir_w_nasdaq_loader()">
                            <q-item-section class="text-subtitle1">
                                <div>Carga de series desde <span class="text-blue-10 text-bold">Csv Nasdaq</span></div>
                            </q-item-section>                            
                        </q-item>
                    </q-list>
                </q-menu>
            </q-btn>
            <q-toolbar-title class="text-blue-10">Series</q-toolbar-title>
        </q-toolbar>      
        <q-card >
            <!--
            <div class="q-pl-xs row">
                <div class="col-3">
                    <router-view></router-view>                
                </div>
            </div>                       
            <q-separator/>         
            -->
            <div class="col">
                <div class="row">
                    <div class="col">
                        <TableResumenSerie/>
                    </div>                    
                </div>                
            </div>    
        </q-card>      
        <WinNasdaqCsvLoader v-model="store.state.w_nasdaq_loader.open"/>
    </div>
</template>
<script>
import store from './store'
import TableResumenSerie from '@/components/serie/TableResumenSerie.vue'
import WinNasdaqCsvLoader from './WinNasdaqCsvLoader.vue'
//import PanelSerieLoader from '@/components/serie/PanelSerieLoader.vue'
export default {
    name:"MainMantSerie",
    components:{
        TableResumenSerie,
        WinNasdaqCsvLoader

  //      PanelSerieLoader
    },
    data: () => {
        return {
            visible:0,
            store: store
        }
    }
}
</script>