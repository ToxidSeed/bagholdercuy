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
        <q-separator />
        <q-card flat>
            <q-bar class="bg-white">
                <q-btn stack-label flat icon="add_circle_outline" dense label="AÑADIR INSTRUMENTO" color="blue-10"
                    @click="winSeleccionInstrumentoOpen = true">
                </q-btn>
            </q-bar>
        </q-card>
        <q-separator />
        <div class="row q-col-xs">
            <TableMonitoreo class="col-4" />
            <q-separator vertical />
            <TableAlertasSymbol class="col" />
        </div>
        <WinGestionAlerta v-model="WinGestorAlertaStore.state.open" />
        <WinSeleccionInstrumento v-model="winSeleccionInstrumentoOpen" @select-symbol="sel_symbol" />
    </div>
</template>
<script>
import TableAlertasSymbol from "@/components/watchlist/TableAlertasSymbol.vue"
import TableMonitoreo from "./TableMonitoreo.vue"
import WinGestionAlerta from "@/components/watchlist/WinGestionAlerta"
import WinSeleccionInstrumento from "./WinSeleccionInstrumento.vue"
import WinGestorAlertaStore from "./win-gestor-alerta-store"
import tableAlertasSymbolStore from "./table-alertas-symbol-store"
//import SelectSymbol from "@/components/SelectSymbol"
import store from "./store"

export default {
    name: "PanelWatchlist",
    components: {
        TableAlertasSymbol,
        WinGestionAlerta,
        WinSeleccionInstrumento,
        TableMonitoreo,
        //      SelectSymbol
    },
    data() {
        return {
            winSeleccionInstrumentoOpen: false,
            WinGestorAlertaStore: WinGestorAlertaStore,
            TableAlertasSymbolStore: tableAlertasSymbolStore,
            store: store
        }
    },
    mounted: function () {
        //this.TableAlertasSymbolStore.get_data()
    },
    methods: {
        sel_symbol: async function (item) {
            await this.store.panel_watchlist.registrar({
                id_symbol: item.id || item.id_symbol
            })
            // refrescamos el monitoreo
            this.store.table_monitoreo.get_monitoreo_activo()
        }
    }
}
</script>