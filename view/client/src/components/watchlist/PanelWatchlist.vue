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
        <WinSeleccionInstrumento
            v-model="winSeleccionInstrumentoOpen"
            @select-instrumento="sel_instrumento"
        />
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
            guardando: false,
            WinGestorAlertaStore: WinGestorAlertaStore,
            TableAlertasSymbolStore: tableAlertasSymbolStore,
            store: store
        }
    },
    mounted: function () {
        //this.TableAlertasSymbolStore.get_data()
    },
    methods: {
        sel_instrumento: async function (item) {
            if (this.guardando) {
                return
            }
            this.guardando = true
            try {
                let params = {}
                // Si es un contrato de opción
                if (item.id_contrato_opcion) {
                    params = {
                        id_contrato_opcion: item.id_contrato_opcion,
                        id_symbol_type: 2,
                        conid: item.conid || null
                    }
                } else if (item.id_symbol_type === 2 || item.tipo_opcion) {
                    params = {
                        id_symbol_type: 2,
                        id_symbol_subyacente: item.id_symbol_subyacente || item.id_symbol || item.id,
                        id_symbol: item.id_symbol_subyacente || item.id_symbol || item.id,
                        conid: item.conid || null,
                        cod_symbol: item.cod_symbol,
                        tipo_opcion: item.tipo_opcion,
                        fch_vencimiento: item.fch_vencimiento,
                        imp_strike: item.imp_strike,
                        tam_contrato: item.tam_contrato || 100,
                        cod_moneda: item.cod_moneda || 'USD',
                        descripcion: item.descripcion || item.cod_symbol
                    }
                } else {
                    // Symbol estándar (Acción, ETF, Índice)
                    const idSymbol = item.id_symbol || item.id
                    if (!idSymbol) {
                        throw new Error(`No se pudo obtener el identificador del símbolo ${item.symbol || ''}`)
                    }
                    params = {
                        id_symbol: idSymbol,
                        id_symbol_type: item.id_symbol_type || 1,
                        conid: item.conid || null
                    }
                }

                await this.store.panel_watchlist.registrar(params)

                // Refrescamos el monitoreo activo
                await this.store.table_monitoreo.get_monitoreo_activo()

                const nombre = item.cod_symbol || item.symbol || 'el instrumento'
                this.$q.notify({
                    type: 'positive',
                    message: `Se añadió ${nombre} a la lista de monitoreo`,
                    position: 'top',
                    timeout: 2500
                })
            } catch (error) {
                console.error("Error al registrar instrumento en monitoreo:", error)
                const errorMsg = error.response && error.response.data && error.response.data.message
                    ? error.response.data.message
                    : (error.message || "No se pudo añadir el instrumento al monitoreo")
                this.$q.notify({
                    type: 'warning',
                    message: errorMsg,
                    position: 'top',
                    timeout: 3000
                })
            } finally {
                this.guardando = false
            }
        },
        sel_symbol: function (item) {
            return this.sel_instrumento(item)
        }
    }
}
</script>