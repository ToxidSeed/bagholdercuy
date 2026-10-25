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
                                
                                <div class="row items-center justify-end no-wrap">
                                    <div class="text-subtitle1 text-weight-bolder text-dark q-mr-xs">
                                        {{ format_currency(props.row.imp_actual) }}
                                    </div>
                                    <q-btn 
                                        icon="delete_outline" 
                                        flat 
                                        round 
                                        dense 
                                        size="sm"
                                        class="btn-eliminar-monitoreo"
                                        @click.stop="abrir_dialogo_eliminar(props.row)"
                                    >
                                        <q-tooltip>Eliminar de monitoreo</q-tooltip>
                                    </q-btn>
                                </div>
                            </div>

                            <!-- Fila Expiración (solo para contratos de opción o con vencimiento) -->
                            <div v-if="has_expiracion(props.row)" class="row items-center justify-between no-wrap q-mt-xs">
                                <div class="row items-center q-gutter-x-xs no-wrap">
                                    <q-badge 
                                        :color="badge_expiracion_color(props.row)"
                                        class="q-px-xs text-weight-bold dte-badge"
                                    >
                                        <q-icon name="timer" size="12px" class="q-mr-xs" />
                                        {{ format_dias_expiracion(props.row) }}
                                        <q-tooltip>
                                            Vencimiento: {{ format_fecha_vencimiento(props.row) }}
                                        </q-tooltip>
                                    </q-badge>
                                    <span class="text-caption text-grey-7 expiration-date-label">
                                        Vence: {{ format_fecha_vencimiento(props.row) }}
                                    </span>
                                </div>

                                <div v-if="props.row.tipo_opcion" class="row items-center q-gutter-x-xs no-wrap text-caption">
                                    <q-badge 
                                        :color="props.row.tipo_opcion.toUpperCase() === 'CALL' ? 'teal-8' : 'deep-orange-8'"
                                        outline
                                        class="text-weight-bold q-px-xs option-type-badge"
                                    >
                                        {{ props.row.tipo_opcion.toUpperCase() }}
                                    </q-badge>
                                    <span v-if="props.row.imp_strike !== null && props.row.imp_strike !== undefined" class="text-weight-bold text-grey-8 strike-label">
                                        ${{ Number(props.row.imp_strike).toFixed(2) }}
                                    </span>
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

        <!-- Diálogo de Confirmación de Eliminación Lógica -->
        <q-dialog v-model="confirmDeleteDialog.open" persistent>
            <q-card style="min-width: 360px; max-width: 440px;" class="q-pa-sm">
                <q-card-section class="row items-center no-wrap">
                    <q-avatar icon="delete_sweep" color="red-1" text-color="negative" />
                    <div class="q-ml-md">
                        <div class="text-subtitle1 text-weight-bold">
                            Eliminar de monitoreo
                        </div>
                        <div class="text-caption text-grey-7 q-mt-xs">
                            ¿Estás seguro de que deseas quitar 
                            <span class="text-weight-bold text-dark">{{ confirmDeleteDialog.row ? confirmDeleteDialog.row.cod_symbol : '' }}</span> 
                            de la lista de monitoreo activo?
                        </div>
                        <div v-if="confirmDeleteDialog.row && confirmDeleteDialog.row.id_config_alerta" class="text-caption text-amber-9 q-mt-sm">
                            <q-icon name="info" size="xs" class="q-mr-xs" />
                            Las alertas y comentarios configurados se mantendrán archivados.
                        </div>
                    </div>
                </q-card-section>

                <q-card-actions align="right" class="q-pt-none">
                    <q-btn flat label="Cancelar" color="grey-7" v-close-popup :disable="confirmDeleteDialog.loading" />
                    <q-btn 
                        flat 
                        label="Eliminar" 
                        color="negative" 
                        :loading="confirmDeleteDialog.loading"
                        @click="ejecutar_eliminar"
                    />
                </q-card-actions>
            </q-card>
        </q-dialog>
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
            confirmDeleteDialog: {
                open: false,
                loading: false,
                row: null
            },
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
                },
                {
                    name: "tipo_opcion",
                    field: "tipo_opcion"
                },
                {
                    name: "fch_vencimiento",
                    field: "fch_vencimiento"
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
            const state = this.tableAlertasSymbolStore.state
            if (row.id_monitoreo && state.id_monitoreo) {
                return state.id_monitoreo === row.id_monitoreo
            }
            if (row.id_symbol && state.id_symbol) {
                return state.id_symbol === row.id_symbol
            }
            if (row.cod_symbol && state.cod_symbol) {
                return state.cod_symbol === row.cod_symbol
            }
            return false
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
            return `${sign}${Number(row.pct_variacion).toFixed(2)}%`
        },
        get_dias_expiracion: function(row) {
            if (row.dias_expiracion !== undefined && row.dias_expiracion !== null) {
                return Number(row.dias_expiracion)
            }
            const fch = row.fch_vencimiento || this.parse_osi_date(row.cod_symbol)
            if (fch) {
                const parts = String(fch).split(/[-T ]/)[0].split('-')
                if (parts.length === 3) {
                    const year = parseInt(parts[0], 10)
                    const month = parseInt(parts[1], 10) - 1
                    const day = parseInt(parts[2], 10)
                    const expDate = new Date(year, month, day)
                    const now = new Date()
                    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
                    const diffTime = expDate.getTime() - today.getTime()
                    return Math.round(diffTime / (1000 * 60 * 60 * 24))
                }
            }
            return null
        },
        parse_osi_date: function(symbol) {
            if (!symbol || typeof symbol !== 'string') return null
            const match = symbol.match(/(\d{2})(\d{2})(\d{2})[CPcp]\d{8}$/)
            if (match) {
                const year = `20${match[1]}`
                const month = match[2]
                const day = match[3]
                return `${year}-${month}-${day}`
            }
            return null
        },
        has_expiracion: function(row) {
            return this.get_dias_expiracion(row) !== null || (row.id_symbol_type === 2 && Boolean(row.fch_vencimiento))
        },
        format_dias_expiracion: function(row) {
            const dias = this.get_dias_expiracion(row)
            if (dias === null) return ''
            if (dias === 0) return 'Expira hoy'
            if (dias === 1) return '1 día'
            if (dias > 1) return `${dias} días`
            if (dias === -1) return 'Expiró ayer'
            return `Expiró hace ${Math.abs(dias)} días`
        },
        badge_expiracion_color: function(row) {
            const dias = this.get_dias_expiracion(row)
            if (dias === null) return 'grey-6'
            if (dias < 0) return 'grey-7'
            if (dias <= 2) return 'negative'
            if (dias <= 7) return 'amber-9'
            if (dias <= 30) return 'primary'
            return 'teal-8'
        },
        format_fecha_vencimiento: function(row) {
            const raw = row.fch_vencimiento || this.parse_osi_date(row.cod_symbol)
            if (!raw) return ''
            const clean = String(raw).split(/[-T ]/)[0]
            const parts = clean.split('-')
            if (parts.length === 3) {
                return `${parts[2]}/${parts[1]}/${parts[0]}`
            }
            return clean
        },
        get_alertas: function(row) {                        
            winComentariosAlertaStore.cerrar()

            this.tableAlertasSymbolStore.set_symbol({
                id_monitoreo: row.id_monitoreo,
                id_symbol: row.id_symbol,
                id_contrato_opcion: row.id_contrato_opcion,
                cod_symbol: row.cod_symbol,
                nom_symbol: row.nom_symbol,
                fch_vencimiento: row.fch_vencimiento || this.parse_osi_date(row.cod_symbol),
                dias_expiracion: this.get_dias_expiracion(row),
                tipo_opcion: row.tipo_opcion,
                imp_strike: row.imp_strike
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
        },
        abrir_dialogo_eliminar: function(row) {
            this.confirmDeleteDialog.row = row
            this.confirmDeleteDialog.open = true
        },
        ejecutar_eliminar: async function() {
            const row = this.confirmDeleteDialog.row
            if (!row || !row.id_monitoreo) {
                this.confirmDeleteDialog.open = false
                return
            }

            this.confirmDeleteDialog.loading = true
            try {
                await this.store.table_monitoreo.eliminar(row.id_monitoreo)

                if (this.is_selected(row)) {
                    this.tableAlertasSymbolStore.limpiar()
                    this.winComentariosAlertaStore.cerrar()
                }

                this.$q.notify({
                    type: 'positive',
                    message: `Se quitó ${row.cod_symbol} de la lista de monitoreo`,
                    position: 'top',
                    timeout: 2500
                })
                this.confirmDeleteDialog.open = false
            } catch (error) {
                console.error("Error al eliminar monitoreo:", error)
                const errorMsg = error.response && error.response.data && error.response.data.message
                    ? error.response.data.message
                    : (error.message || "No se pudo eliminar el instrumento del monitoreo")
                this.$q.notify({
                    type: 'warning',
                    message: errorMsg,
                    position: 'top',
                    timeout: 3000
                })
            } finally {
                this.confirmDeleteDialog.loading = false
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

.btn-eliminar-monitoreo {
    opacity: 0.25;
    transition: opacity 0.2s ease, color 0.2s ease;
    color: #757575;
}

.monitoreo-card:hover .btn-eliminar-monitoreo {
    opacity: 1;
}

.btn-eliminar-monitoreo:hover {
    color: #c10015 !important;
}

.dte-badge {
    font-size: 11px;
    padding: 2px 6px;
    border-radius: 4px;
}

.option-type-badge {
    font-size: 10px;
    padding: 1px 4px;
}

.expiration-date-label {
    font-size: 11px;
}

.strike-label {
    font-size: 11px;
}
</style>