<template>
    <div>
        <q-toolbar class="text-blue-10">
            <q-btn flat round dense icon="menu">
                <q-menu>
     
                </q-menu>
            </q-btn>
            <q-toolbar-title>
                Watchlist
            </q-toolbar-title>            
            <q-btn flat round dense icon="more_vert" />                                        
        </q-toolbar>   
        <q-separator/>
        <q-card flat>
            <q-toolbar>
            <!--<q-toolbar-title class="text-blue-10">Alertas</q-toolbar-title>            -->
                <q-btn stack-label flat icon="add" dense label="Nueva alerta" class="text-capitalize" color="blue-10" @click="WinGestorAlertaStore.nuevo()">                
                </q-btn >
                <div class="q-pb-xs q-pl-md"  >
                    <SelectSymbol label="Incluir en monitoreo" v-on:select-symbol="sel_symbol"/>
                </div>
            </q-toolbar>
        </q-card>        
        <q-separator/>        
        <div class="row q-col-gutter-xs">            
            <TableMonitoreo class="col-4"/>
            <TableAlertasSymbol class="col-8"/>            
        </div>
        <WinGestionAlerta v-model="WinGestorAlertaStore.state.open"/>
    </div>
</template>
<script>
import TableAlertasSymbol from "@/components/watchlist/TableAlertasSymbol.vue"
import TableMonitoreo from "./TableMonitoreo.vue"
import WinGestionAlerta from "@/components/watchlist/WinGestionAlerta"
import WinGestorAlertaStore from "./win-gestor-alerta-store"
import tableAlertasSymbolStore from "./table-alertas-symbol-store"
import SelectSymbol from "@/components/SelectSymbol"
import store from "./store"

export default {
    name:"PanelWatchlist",
    components:{
        TableAlertasSymbol,
        WinGestionAlerta,
        TableMonitoreo,
        SelectSymbol
    },
    data(){
        return {
            WinGestorAlertaStore: WinGestorAlertaStore,
            TableAlertasSymbolStore: tableAlertasSymbolStore,
            store: store
        }
    },
    mounted:function(){
        //this.TableAlertasSymbolStore.get_data()
    },
    methods:{
        sel_symbol: async function(item){            
            await this.store.panel_watchlist.registrar({
                id_symbol: item.id_symbol
            })
            // refrescamos el monitoreo
            this.store.table_monitoreo.get_monitoreo_activo()
        }
    }
}
</script>