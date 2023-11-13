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
                Watchlist
            </q-toolbar-title>            
            <q-btn flat round dense icon="more_vert" />                                        
        </q-toolbar>   
        <q-separator/>
        <q-toolbar>
            <!--<q-toolbar-title class="text-blue-10">Alertas</q-toolbar-title>            -->
            <q-btn stack-label flat icon="add" label="Nueva alerta" class="text-capitalize" color="blue-10" @click="WinGestionAlerta.open=true">                
            </q-btn>
        </q-toolbar>
        <q-separator/>
        <div class="row q-col-gutter-xs">            
            <ListaSymbolsAlertas class="col-4"/>
            <TableListaFuturaCompra class="col-8"/>
        </div>
        <WinGestionAlerta v-model="WinGestionAlerta.open"/>
    </div>
</template>
<script>
import ListaSymbolsAlertas from "@/components/watchlist/ListaSymbolsAlertas.vue"
import TableListaFuturaCompra from "@/components/watchlist/TableListaFuturaCompra.vue"
import WinGestionAlerta from "@/components/watchlist/WinGestionAlerta"

export default {
    name:"PanelWatchlist",
    components:{
        TableListaFuturaCompra,
        ListaSymbolsAlertas,
        WinGestionAlerta
    },
    data(){
        return {
            WinGestionAlerta:{
                open:false
            }
        }
    }
}
</script>