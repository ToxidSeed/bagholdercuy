<template>
    <div class="table-monitoreo-container">
        <q-table
            :data="store.table_monitoreo.state.monitoreo_activo_data"            
            :columns="columns"
            row-key="id_monitoreo"            
            dense
            hide-header            
            :pagination="pagination"
            :filter="filter"
            :loading="loading"
            flat
            class="bg-white"
        >            
            <template v-slot:top shrink>
                <q-toolbar class="q-px-sm q-py-xs">
                    <q-toolbar-title class="text-subtitle1 text-weight-bold text-blue-10">
                        Monitoreo
                    </q-toolbar-title>
                    <q-btn 
                        icon="refresh" 
                        flat 
                        round 
                        dense 
                        color="primary" 
                        :loading="loading"
                        @click="btn_refresh_click"
                    >
                        <q-tooltip>Actualizar cotizaciones</q-tooltip>
                    </q-btn>
                </q-toolbar>
                <q-toolbar class="q-px-sm q-pb-sm">
                    <q-input 
                        v-model="filter"
                        placeholder="Buscar símbolo o nombre..."
                        dense
                        outlined
                        clearable
                        class="full-width"
                    >
                        <template v-slot:append>
                            <q-icon name="search" />
                        </template>
                    </q-input>
                </q-toolbar>                                
            </template>

            <template v-slot:no-data>
                <div class="full-width text-center text-grey-6 q-pa-lg">
                    <q-icon name="visibility_off" size="40px" class="q-mb-xs text-grey-4" />
                    <div class="text-caption text-weight-medium">No hay instrumentos en monitoreo</div>
                    <div class="text-caption text-grey-5">Añade instrumentos con el botón superior</div>
                </div>
            </template>

            <template v-slot:body="props">                
                <q-tr :props="props" class="monitoreo-tr">                    
                    <q-td colspan="100%" class="q-pa-none">
                        <div 
                            class="monitoreo-card q-pa-sm cursor-pointer"
                            :class="{'monitoreo-card-active': is_selected(props.row)}"
                            @click="get_alertas(props.row)"
                        >
                            <!-- Fila Superior: Ticker + Campana y Precio Actual -->
                            <div class="row items-center justify-between no-wrap">
                                <div class="row items-center no-wrap">
                                    <span class="text-weight-bolder text-subtitle1 text-primary q-mr-xs">
                                        {{ props.row.cod_symbol }}
                                    </span>
                                    <q-btn 
                                        icon="notifications" 
                                        flat 
                                        round 
                                        dense 
                                        size="sm"
                                        :color="props.row.id_config_alerta ? 'amber-9' : 'grey-4'" 
                                        @click.stop="btn_alerta_click(props.row)"
                                    >
                                        <q-tooltip>
                                            {{ props.row.id_config_alerta ? 'Alerta configurada (clic para editar)' : 'Sin alerta (clic para crear)' }}
                                        </q-tooltip>
                                    </q-btn>
                                </div>
                                
                                <div class="text-right">
                                    <div class="text-subtitle1 text-weight-bolder text-dark">
                                        {{ format_currency(props.row.imp_actual) }}
                                    </div>
                                </div>
                            </div>

                            <!-- Fila Inferior: Nombre y Rendimiento / Cierre anterior -->
                            <div class="row items-center justify-between no-wrap q-mt-xs">
                                <div class="text-caption text-grey-7 truncate-name" :title="props.row.nom_symbol">
                                    {{ props.row.nom_symbol || '—' }}
                                </div>

                                <div class="row items-center justify-end q-gutter-x-xs no-wrap">
                                    <q-badge 
                                        v-if="has_variacion(props.row)"
                                        :color="badge_color(props.row)"
                                        class="q-px-xs text-weight-bold variation-badge"
                                    >
                                        <q-icon :name="props.row.imp_variacion >= 0 ? 'arrow_drop_up' : 'arrow_drop_down'" size="14px" />
                                        {{ format_variacion(props.row) }}
                                    </q-badge>

                                    <span class="text-caption text-grey-6 prev-close-text">
                                        Ant: {{ format_currency(props.row.imp_cierre_anterior) }}
                                    </span>
                                </div>
                            </div>
                        </div>
                        <q-separator />
                    </q-td>
                </q-tr>                                                                    
            </template>
        </q-table>      
    </div>
</template>
<script>
import WinGestorAlertaStore from "./win-gestor-alerta-store"
import tableAlertasSymbolStore from "./table-alertas-symbol-store"
import winComentariosAlertaStore from "./win-comentarios-alerta-store"
import store from "./store"

export default {
    name: "TableMonitoreo",
    data() {
        return {
            filter: "",
            loading: false,
            columns: [
                {
                    name: "cod_symbol",
                    label: "Cod. Symbol",
                    align: "left",
                    field: "cod_symbol"
                },
                {
                    name: "nom_symbol",
                    label: "Nom. Symbol",
                    align: "left",
                    field: "nom_symbol"
                }
            ],
            pagination: {
                rowsPerPage: 15
            },
            WinManagerFuturaOperacion: {
                open: false
            },
            WinGestorAlertaStore: WinGestorAlertaStore,
            tableAlertasSymbolStore: tableAlertasSymbolStore,
            winComentariosAlertaStore: winComentariosAlertaStore,
            store: store
        }
    },
    mounted: function() {
        this.init()
    },
    methods: {
        init: async function() {            
            this.loading = true
            try {
                await store.table_monitoreo.get_monitoreo_activo()
            } finally {
                this.loading = false
            }
        },        
        btn_refresh_click: async function() {
            this.loading = true
            try {
                await store.table_monitoreo.refresh()
            } finally {
                this.loading = false
            }
        },
        is_selected: function(row) {
            return this.tableAlertasSymbolStore.state.id_symbol === row.id_symbol
        },
        format_currency: function(val) {
            if (val === null || val === undefined || isNaN(val)) {
                return '—'
            }
            return Number(val).toLocaleString('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            })
        },
        has_variacion: function(row) {
            return row.pct_variacion !== null && row.pct_variacion !== undefined && !isNaN(row.pct_variacion)
        },
        badge_color: function(row) {
            if (row.imp_variacion > 0) return 'positive'
            if (row.imp_variacion < 0) return 'negative'
            return 'grey-6'
        },
        format_variacion: function(row) {
            if (!this.has_variacion(row)) return ''
            const sign = row.pct_variacion > 0 ? '+' : ''
            return `${sign}${(row.pct_variacion * 100).toFixed(2)}%`
        },
        get_alertas: function(row) {                        
            winComentariosAlertaStore.cerrar()

            this.tableAlertasSymbolStore.set_symbol({
                id_symbol: row.id_symbol,
                cod_symbol: row.cod_symbol,
                nom_symbol: row.nom_symbol
            })

            this.tableAlertasSymbolStore.fetch_data({                 
                id_config_alerta: row.id_config_alerta
            })
        },  
        btn_alerta_click: function(row) {
            if (row.id_config_alerta !== undefined && row.id_config_alerta !== "" && row.id_config_alerta != null) {
                this.WinGestorAlertaStore.editar(row.id_config_alerta)
                return
            }

            if (row.id_monitoreo !== undefined && row.id_monitoreo !== "") {
                this.WinGestorAlertaStore.incluir_alerta(row.id_monitoreo, row.id_symbol)
            }            
        }
    }
}
</script>

<style scoped>
.table-monitoreo-container {
    border-right: 1px solid #e0e0e0;
}

.monitoreo-tr {
    background: transparent;
}

.monitoreo-card {
    transition: background-color 0.18s ease, border-left 0.18s ease;
    border-left: 4px solid transparent;
}

.monitoreo-card:hover {
    background-color: #f7f9fc;
}

.monitoreo-card-active {
    background-color: #e8f0fe !important;
    border-left: 4px solid #1976d2 !important;
}

.truncate-name {
    max-width: 140px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.variation-badge {
    font-size: 11px;
    padding: 2px 5px;
    border-radius: 4px;
}

.prev-close-text {
    font-size: 11px;
}
</style>