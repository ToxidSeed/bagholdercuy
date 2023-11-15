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
            <TableMonitoreo class="col-4" v-on:btn-alerta-click="abrir_gestor_alertas"/>
            <TableListaFuturaCompra class="col-8"/>
        </div>
        <WinGestionAlerta v-model="WinGestionAlerta.open"/>
    </div>
</template>
<script>
import TableListaFuturaCompra from "@/components/watchlist/TableListaFuturaCompra.vue"
import TableMonitoreo from "./TableMonitoreo.vue"
import WinGestionAlerta from "@/components/watchlist/WinGestionAlerta"

export default {
    name:"PanelWatchlist",
    components:{
        TableListaFuturaCompra,
        WinGestionAlerta,
        TableMonitoreo
    },
    data(){
        return {
            WinGestionAlerta:{
                open:false,
                id_monitoreo: ""
            }
        }
    },
    methods:{
        abrir_gestor_alertas:function(params){        
            console.log(params)                
            this.$store.dispatch("configuracion_alerta/editar_configuracion_alerta",params,{root:true})                          
        }
    }
}
</script>