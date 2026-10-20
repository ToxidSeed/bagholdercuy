<template>
    <q-dialog v-model="open">
        <q-card :style="vista === 'cadena' ? 'width: 900px; max-width: 95vw;' : 'width: 600px; max-width: 90vw;'">
            <q-toolbar>
                <q-btn v-if="vista === 'cadena'" flat round dense icon="arrow_back" color="blue-10"
                    @click="vista = 'busqueda'" class="q-mr-sm">
                    <q-tooltip>Volver a búsqueda</q-tooltip>
                </q-btn>
                <q-toolbar-title class="text-blue-10">
                    <span v-if="vista === 'busqueda'">Añadir Instrumento</span>
                    <span v-else>
                        Cadena de Opciones · <span class="text-bold">{{ instrumento_seleccionado ?
                            instrumento_seleccionado.symbol : '' }}</span>
                    </span>
                </q-toolbar-title>
                <q-btn flat round dense icon="close" v-close-popup />
            </q-toolbar>
            <q-separator />

            <!-- PANEL 1: BÚSQUEDA DE INSTRUMENTOS -->
            <q-card-section v-if="vista === 'busqueda'" class="q-pt-md">
                <q-input v-model="filtro" placeholder="Busqueda de Acciones, ETFs, Indices" outlined dense
                    color="blue-10" clearable autofocus debounce="500" :loading="cargando" @input="buscar">
                    <template v-slot:prepend>
                        <q-icon name="search" color="blue-10" />
                    </template>
                </q-input>

                <!-- Lista de coincidencias -->
                <div v-if="filtro && coincidencias.length > 0" class="q-mt-sm">
                    <q-scroll-area style="height: 320px;">
                        <q-list separator bordered class="rounded-borders">
                            <q-item v-for="item in coincidencias" :key="item.id" clickable v-ripple
                                @click="seleccionar_item(item)">
                                <q-item-section>
                                    <div class="row items-center">
                                        <span class="text-blue-10 text-bold text-subtitle2 q-mr-sm">{{ item.symbol
                                        }}</span>
                                        <q-badge v-if="item.tipo" color="grey-3" text-color="blue-10" :label="item.tipo"
                                            class="text-caption" />
                                        <q-badge v-if="item.exchange" color="grey-2" text-color="grey-8"
                                            :label="item.exchange" class="text-caption q-ml-xs" />
                                    </div>
                                    <q-item-label caption class="text-grey-8">{{ item.name }}</q-item-label>
                                </q-item-section>

                                <q-item-section side>
                                    <div class="row items-center q-gutter-xs no-wrap">
                                        <q-btn flat dense no-caps color="blue-10" icon="tune" label="Cadena"
                                            class="text-weight-medium"
                                            :loading="cargando_cadena && item_cargando_id === item.id"
                                            @click.stop="ver_opciones(item)">
                                            <q-tooltip anchor="top middle" self="bottom middle">Ver contratos de
                                                opciones</q-tooltip>
                                        </q-btn>
                                        <q-btn flat round dense color="green-8" icon="add"
                                            @click.stop="seleccionar_item(item)">
                                            <q-tooltip anchor="top middle" self="bottom middle">Añadir a
                                                monitoreo</q-tooltip>
                                        </q-btn>
                                    </div>
                                </q-item-section>
                            </q-item>
                        </q-list>
                    </q-scroll-area>
                </div>

                <div v-else-if="cargando" class="text-center q-pa-md">
                    <q-spinner color="blue-10" size="2em" />
                </div>

                <div v-else-if="filtro && coincidencias.length === 0" class="text-grey-7 text-center q-pa-md">
                    No se encontraron coincidencias para "{{ filtro }}"
                </div>

                <div v-else class="text-grey-6 text-center q-pa-lg text-caption">
                    Escriba un símbolo o nombre para buscar acciones, ETFs o índices
                </div>
            </q-card-section>

            <!-- PANEL 2: CADENA DE OPCIONES (CALLS Y PUTS UNIFICADOS) -->
            <q-card-section v-else-if="vista === 'cadena'" class="q-pt-md q-px-md">
                <!-- Información del activo y filtro de expiración y strikes -->
                <div class="row items-center justify-between q-mb-sm">
                    <div class="row items-center">
                        <span class="text-h6 text-bold text-blue-10 q-mr-sm">
                            {{ instrumento_seleccionado ? instrumento_seleccionado.symbol : '' }}
                        </span>
                        <span class="text-body2 text-grey-8 q-mr-sm">
                            {{ instrumento_seleccionado ? instrumento_seleccionado.name : '' }}
                        </span>
                        <q-badge v-if="instrumento_seleccionado && instrumento_seleccionado.tipo" color="grey-3"
                            text-color="blue-10" :label="instrumento_seleccionado.tipo" class="text-caption" />
                    </div>

                    <div class="row items-center q-gutter-sm">
                        <span class="text-caption text-bold text-grey-7">Expiración:</span>
                        <q-select v-model="expiracion_seleccionada" :options="expiraciones_disponibles" dense outlined
                            options-dense color="blue-10" style="min-width: 170px;"
                            :loading="cargando_expiraciones || cargando_strikes" :disable="cargando_expiraciones"
                            emit-value map-options>
                            <template v-slot:no-option>
                                <q-item>
                                    <q-item-section class="text-grey">
                                        Sin expiraciones disponibles
                                    </q-item-section>
                                </q-item>
                            </template>
                        </q-select>

                        <span class="text-caption text-bold text-grey-7 q-ml-sm">Strikes:</span>
                        <q-select v-model="num_strikes_seleccionado" :options="num_strikes_opciones" dense outlined
                            options-dense color="blue-10" style="min-width: 100px;"
                            :loading="cargando_strikes" emit-value map-options>
                        </q-select>
                    </div>
                </div>

                <q-separator class="q-mb-sm" />

                <!-- Tabla Unificada de Cadena de Opciones: Calls (izq), Strikes (centro), Puts (der) -->
                <q-card flat bordered class="rounded-borders">
                    <q-table :data="chain_rows" :columns="chain_columns" row-key="strike" dense flat hide-pagination
                        :pagination="{ rowsPerPage: 0 }" :loading="cargando_strikes"
                        style="max-height: 420px; overflow-y: auto;">
                        <template v-slot:header="props">
                            <q-tr>
                                <q-th colspan="4" class="text-center bg-blue-1 text-bold text-blue-10"
                                    style="border-right: 2px solid #90caf9;">
                                    <q-icon name="call_made" color="blue-9" class="q-mr-xs" /> CALLS
                                </q-th>
                                <q-th class="text-center bg-grey-3 text-bold text-grey-9"
                                    style="border-right: 2px solid #e0e0e0; min-width: 90px;">
                                    STRIKE
                                </q-th>
                                <q-th colspan="4" class="text-center bg-red-1 text-bold text-red-10">
                                    <q-icon name="call_received" color="red-9" class="q-mr-xs" /> PUTS
                                </q-th>
                            </q-tr>
                            <q-tr :props="props">
                                <q-th key="call_action" :props="props" class="bg-blue-1 text-blue-10 text-center" style="width: 42px;"></q-th>
                                <q-th key="call_bid" :props="props" class="bg-blue-1 text-blue-10 text-right">Bid</q-th>
                                <q-th key="call_ask" :props="props" class="bg-blue-1 text-blue-10 text-right">Ask</q-th>
                                <q-th key="call_last" :props="props" class="bg-blue-1 text-blue-10 text-right"
                                    style="border-right: 2px solid #90caf9;">Last</q-th>
                                <q-th key="strike" :props="props" class="bg-grey-3 text-bold text-grey-9 text-center"
                                    style="border-right: 2px solid #e0e0e0;">Strike</q-th>
                                <q-th key="put_bid" :props="props" class="bg-red-1 text-red-10 text-right">Bid</q-th>
                                <q-th key="put_ask" :props="props" class="bg-red-1 text-red-10 text-right">Ask</q-th>
                                <q-th key="put_last" :props="props" class="bg-red-1 text-red-10 text-right">Last</q-th>
                                <q-th key="put_action" :props="props" class="bg-red-1 text-red-10 text-center" style="width: 42px;"></q-th>
                            </q-tr>
                        </template>

                        <template v-slot:body="props">
                            <q-tr :props="props">
                                <q-td key="call_action" :props="props" class="text-center q-pa-none" :class="props.row.is_call_itm ? 'bg-blue-1' : ''">
                                    <q-btn flat round dense size="sm" icon="add" color="blue-10"
                                        @click.stop="seleccionar_opcion(props.row, 'CALL')">
                                        <q-tooltip anchor="top middle" self="bottom middle">Añadir Call ${{ props.row.strike }} al monitoreo</q-tooltip>
                                    </q-btn>
                                </q-td>
                                <q-td key="call_bid" :props="props" class="cursor-pointer" :class="props.row.is_call_itm ? 'bg-blue-1 text-bold' : ''"
                                    @click="seleccionar_opcion(props.row, 'CALL')">
                                    {{ props.row.call_bid }}
                                </q-td>
                                <q-td key="call_ask" :props="props" class="cursor-pointer" :class="props.row.is_call_itm ? 'bg-blue-1 text-bold' : ''"
                                    @click="seleccionar_opcion(props.row, 'CALL')">
                                    {{ props.row.call_ask }}
                                </q-td>
                                <q-td key="call_last" :props="props" class="cursor-pointer" :class="props.row.is_call_itm ? 'bg-blue-1 text-bold' : ''"
                                    style="border-right: 2px solid #bbdefb;"
                                    @click="seleccionar_opcion(props.row, 'CALL')">
                                    {{ props.row.call_last }}
                                </q-td>
                                <q-td key="strike" :props="props" class="bg-grey-2 text-bold text-blue-10 text-center"
                                    style="border-right: 2px solid #e0e0e0;">
                                    {{ props.row.strike }}
                                </q-td>
                                <q-td key="put_bid" :props="props" class="cursor-pointer" :class="props.row.is_put_itm ? 'bg-red-1 text-bold' : ''"
                                    @click="seleccionar_opcion(props.row, 'PUT')">
                                    {{ props.row.put_bid }}
                                </q-td>
                                <q-td key="put_ask" :props="props" class="cursor-pointer" :class="props.row.is_put_itm ? 'bg-red-1 text-bold' : ''"
                                    @click="seleccionar_opcion(props.row, 'PUT')">
                                    {{ props.row.put_ask }}
                                </q-td>
                                <q-td key="put_last" :props="props" class="cursor-pointer" :class="props.row.is_put_itm ? 'bg-red-1 text-bold' : ''"
                                    @click="seleccionar_opcion(props.row, 'PUT')">
                                    {{ props.row.put_last }}
                                </q-td>
                                <q-td key="put_action" :props="props" class="text-center q-pa-none" :class="props.row.is_put_itm ? 'bg-red-1' : ''">
                                    <q-btn flat round dense size="sm" icon="add" color="red-10"
                                        @click.stop="seleccionar_opcion(props.row, 'PUT')">
                                        <q-tooltip anchor="top middle" self="bottom middle">Añadir Put ${{ props.row.strike }} al monitoreo</q-tooltip>
                                    </q-btn>
                                </q-td>
                            </q-tr>
                        </template>

                        <template v-slot:no-data>
                            <div class="full-width row flex-center text-grey q-gutter-sm q-py-md">
                                <span>Sin contratos de opciones disponibles</span>
                            </div>
                        </template>
                    </q-table>
                </q-card>
            </q-card-section>

            <q-separator />

            <q-card-actions align="right">
                <q-btn v-if="vista === 'cadena'" label="Volver a búsqueda" class="text-capitalize" color="blue-10" flat
                    icon="arrow_back" @click="vista = 'busqueda'" />
                <q-space v-if="vista === 'cadena'" />
                <q-btn label="Cerrar" class="text-capitalize" color="red-14" flat v-close-popup />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script>
import { headers } from '@/common/common.js'
import Ibkr from '@/api/ibkr.js'

export default {
    name: "WinSeleccionInstrumento",
    props: {
        value: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            open: this.value,
            vista: "busqueda", // 'busqueda' | 'cadena'
            instrumento_seleccionado: null,
            filtro: "",
            cargando: false,
            coincidencias: [],
            // Expiraciones de IBKR
            expiracion_seleccionada: null,
            expiraciones_disponibles: [],
            // Num strikes
            num_strikes_seleccionado: 10,
            num_strikes_opciones: [
                { label: "10", value: 10 },
                { label: "20", value: 20 },
                { label: "30", value: 30 },
                { label: "40", value: 40 },
                { label: "50", value: 50 },
                { label: "Todos", value: 0 }
            ],
            cargando_cadena: false,
            item_cargando_id: null,
            cargando_expiraciones: false,
            cargando_strikes: false,
            chain_columns: [
                { name: "call_action", label: "", field: "call_action", align: "center" },
                { name: "call_bid", label: "Bid", field: "call_bid", align: "right" },
                { name: "call_ask", label: "Ask", field: "call_ask", align: "right" },
                { name: "call_last", label: "Last", field: "call_last", align: "right" },
                { name: "strike", label: "Strike", field: "strike", align: "center" },
                { name: "put_bid", label: "Bid", field: "put_bid", align: "right" },
                { name: "put_ask", label: "Ask", field: "put_ask", align: "right" },
                { name: "put_last", label: "Last", field: "put_last", align: "right" },
                { name: "put_action", label: "", field: "put_action", align: "center" }
            ],
            chain_rows: []
        }
    },
    watch: {
        value(newval) {
            this.open = newval
            if (newval) {
                this.vista = "busqueda"
                this.instrumento_seleccionado = null
                this.filtro = ""
                this.coincidencias = []
                this.cargando = false
                this.cargando_cadena = false
                this.item_cargando_id = null
                this.cargando_expiraciones = false
                this.cargando_strikes = false
                this.expiraciones_disponibles = []
                this.expiracion_seleccionada = null
                this.num_strikes_seleccionado = 10
                this.chain_rows = []
            }
        },
        open(newval) {
            this.$emit("input", newval)
        },
        expiracion_seleccionada(newval) {
            if (newval && this.vista === "cadena") {
                this.obtener_strikes()
            }
        },
        num_strikes_seleccionado() {
            if (this.vista === "cadena" && this.instrumento_seleccionado && this.expiracion_seleccionada) {
                this.obtener_strikes()
            }
        }
    },
    methods: {
        buscar(val) {
            if (!val || !val.trim()) {
                this.coincidencias = []
                this.cargando = false
                return
            }

            this.cargando = true
            this.$http.post(
                'SymbolManager/SymbolFinder/buscar_por_texto',
                {
                    texto: val.trim()
                },
                {
                    headers: headers()
                }
            ).then(httpresponse => {
                const appresponse = httpresponse.data
                const options = []
                if (appresponse && appresponse.data) {
                    for (let element of appresponse.data) {
                        const idSymbol = element["id_symbol"] || element["id"]
                        options.push({
                            id: idSymbol,
                            id_symbol: idSymbol,
                            symbol: element["symbol"],
                            name: element["name"],
                            tipo: element["asset_type"] || "",
                            asset_type: element["asset_type"] || "",
                            exchange: element["exchange"] || "",
                            id_symbol_type: element["id_symbol_type"] || 1,
                            value: element["symbol"],
                            label: element["name"]
                        })
                    }
                }
                this.coincidencias = options
            }).catch(error => {
                console.error("Error buscando symbol:", error)
                this.coincidencias = []
            }).then(() => {
                this.cargando = false
            })
        },
        seleccionar_item(item) {
            const symbolPayload = {
                id: item.id,
                id_symbol: item.id,
                value: item.symbol,
                label: item.name,
                symbol: item.symbol,
                name: item.name,
                tipo: item.tipo,
                asset_type: item.asset_type,
                exchange: item.exchange,
                id_symbol_type: item.id_symbol_type || 1
            }
            this.$emit("select-instrumento", symbolPayload)
            this.open = false
        },
        formatear_cod_opcion_osi(symbol, fch_vencimiento, tipo, strike) {
            const sym = (symbol || '').trim().toUpperCase()
            let cleanDate = ''
            if (fch_vencimiento) {
                const parts = String(fch_vencimiento).replace(/-/g, '')
                if (parts.length >= 8) {
                    cleanDate = parts.substring(2, 8)
                } else if (parts.length === 6) {
                    cleanDate = parts
                }
            }
            if (!cleanDate) {
                const now = new Date()
                cleanDate = `${String(now.getFullYear()).substring(2)}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}`
            }

            const tipoChar = (tipo || 'CALL').toUpperCase().startsWith('C') ? 'C' : 'P'
            const numStrike = Number(strike) || 0
            const strikeMillis = Math.round(numStrike * 1000)
            const strikeStr = String(strikeMillis).padStart(8, '0')

            return `${sym}${cleanDate}${tipoChar}${strikeStr}`
        },
        seleccionar_opcion(row, tipo) {
            if (!row) return
            const strike = row.strike
            const contract = tipo === 'CALL' ? row.call_contract : row.put_contract
            const symbol = this.instrumento_seleccionado ? this.instrumento_seleccionado.symbol : ''
            const id_symbol = this.instrumento_seleccionado
                ? (this.instrumento_seleccionado.id || this.instrumento_seleccionado.id_symbol)
                : null
            const fch = this.expiracion_seleccionada || (contract && (contract.fch_vencimiento || contract.maturityDate)) || ''

            // Validar que cod_symbol sea un ticker OSI real y nunca el símbolo subyacente
            let cod_symbol = (contract && contract.cod_symbol) ? String(contract.cod_symbol).trim() : ''
            if (!cod_symbol || cod_symbol === symbol || cod_symbol.length <= symbol.length) {
                cod_symbol = this.formatear_cod_opcion_osi(symbol, fch, tipo, strike)
            }

            let fch_iso = fch
            if (fch && fch.length === 8 && !fch.includes('-')) {
                fch_iso = `${fch.substring(0, 4)}-${fch.substring(4, 6)}-${fch.substring(6, 8)}`
            } else if (!fch_iso) {
                fch_iso = new Date().toISOString().substring(0, 10)
            }

            const optionPayload = {
                id_symbol: id_symbol,
                id_symbol_subyacente: id_symbol,
                id_contrato_opcion: (contract && contract.id_contrato_opcion) ? contract.id_contrato_opcion : null,
                conid: (contract && contract.conid) ? Number(contract.conid) : null,
                cod_symbol: cod_symbol,
                cod_subyacente: symbol,
                symbol: cod_symbol,
                tipo_opcion: tipo.toUpperCase(),
                fch_vencimiento: fch_iso,
                imp_strike: Number(strike),
                tam_contrato: (contract && contract.multiplier) ? Number(contract.multiplier) : 100,
                cod_moneda: (contract && contract.currency) || 'USD',
                descripcion: `${symbol} ${fch_iso} $${strike} ${tipo.toUpperCase()}`,
                id_symbol_type: 2
            }

            this.$emit("select-instrumento", optionPayload)
            this.open = false
        },
        ver_opciones(item) {
            this.instrumento_seleccionado = item
            this.cargando_cadena = true
            this.item_cargando_id = item.id
            this.cargando_expiraciones = true
            this.expiraciones_disponibles = []
            this.expiracion_seleccionada = null
            this.num_strikes_seleccionado = 10
            this.chain_rows = []

            // Consultar la cadena de opciones de IBKR que devuelve contracts, fch_vencimiento real y fechas_vencimiento antes de filtrar
            Ibkr.get_options_chain({
                cod_subyacente: item.symbol,
                num_strikes: this.num_strikes_seleccionado
            }).then(httpresponse => {
                const res = httpresponse.data
                const data = (res && res.data) ? res.data : (res || {})
                const fechas = (data && Array.isArray(data.fechas_vencimiento))
                    ? data.fechas_vencimiento
                    : (data && Array.isArray(data.exp_dates) ? data.exp_dates : [])

                this.vista = "cadena"
                if (fechas.length > 0) {
                    this.expiraciones_disponibles = fechas.map(f => ({
                        label: `${f} (${this.formatear_expiracion(f)})`,
                        value: f
                    }))
                    this.expiracion_seleccionada = data.fch_vencimiento || fechas[0]
                } else {
                    this.expiraciones_disponibles = []
                    this.expiracion_seleccionada = null
                    this.$q.notify({
                        type: 'info',
                        message: `No se encontraron fechas de expiración para ${item.symbol}`,
                        timeout: 2500
                    })
                }

                this.cargar_datos_cadena(data)
                this.$emit("opciones", item)
            }).catch(error => {
                console.error("Error al obtener cadena de opciones de IBKR, intentando expiraciones:", error)
                // Fallback a get_expiration_dates si get_options_chain falla
                Ibkr.get_expiration_dates({
                    cod_symbol: item.symbol
                }).then(httpresponse => {
                    const res = httpresponse.data
                    let fechas = []
                    if (res && res.data && Array.isArray(res.data)) {
                        fechas = res.data
                    }

                    this.vista = "cadena"
                    if (fechas.length > 0) {
                        this.expiraciones_disponibles = fechas.map(f => ({
                            label: `${f} (${this.formatear_expiracion(f)})`,
                            value: f
                        }))
                        this.expiracion_seleccionada = this.expiraciones_disponibles[0].value
                    } else {
                        this.expiraciones_disponibles = []
                        this.expiracion_seleccionada = null
                        this.$q.notify({
                            type: 'info',
                            message: `No se encontraron fechas de expiración para ${item.symbol}`,
                            timeout: 2500
                        })
                    }
                    this.$emit("opciones", item)
                }).catch(errFallback => {
                    console.error("Error al obtener expiraciones de IBKR:", errFallback)
                    const msg = errFallback.response && errFallback.response.data && errFallback.response.data.message
                        ? errFallback.response.data.message
                        : (errFallback.message || "Error al conectar con IBKR")
                    this.$q.notify({
                        type: 'warning',
                        message: `No se pudieron cargar expiraciones de IBKR (${msg}).`,
                        timeout: 3000
                    })
                    this.vista = "cadena"
                    this.$emit("opciones", item)
                })
            }).finally(() => {
                this.cargando_cadena = false
                this.item_cargando_id = null
                this.cargando_expiraciones = false
            })
        },
        cargar_datos_cadena(data) {
            const rawCalls = Array.isArray(data.calls) ? data.calls : []
            const rawPuts = Array.isArray(data.puts) ? data.puts : []
            const imp_underlying = typeof data.imp_underlying === "number" ? data.imp_underlying : null

            // Recopilar todos los strikes disponibles y ordenarlos
            const strikesSet = new Set(Array.isArray(data.strikes) ? data.strikes.map(s => Number(s)) : [])
            rawCalls.forEach(c => {
                const s = c.strike !== undefined ? c.strike : c.imp_strike
                if (s !== undefined && s !== null) strikesSet.add(Number(s))
            })
            rawPuts.forEach(p => {
                const s = p.strike !== undefined ? p.strike : p.imp_strike
                if (s !== undefined && s !== null) strikesSet.add(Number(s))
            })

            const sortedStrikes = Array.from(strikesSet).sort((a, b) => a - b)

            // Indexar por strike para asociación rápida
            const callsByStrike = new Map()
            rawCalls.forEach(c => {
                const s = Number(c.strike !== undefined ? c.strike : c.imp_strike)
                callsByStrike.set(s, c)
            })

            const putsByStrike = new Map()
            rawPuts.forEach(p => {
                const s = Number(p.strike !== undefined ? p.strike : p.imp_strike)
                putsByStrike.set(s, p)
            })

            this.chain_rows = sortedStrikes.map(strike => {
                const call = callsByStrike.get(strike)
                const put = putsByStrike.get(strike)

                return {
                    strike: strike,
                    is_call_itm: imp_underlying !== null ? strike < imp_underlying : false,
                    is_put_itm: imp_underlying !== null ? strike > imp_underlying : false,

                    // CALLS (Izquierda)
                    call_bid: call && call.bid !== undefined && call.bid !== null ? call.bid : "-",
                    call_ask: call && call.ask !== undefined && call.ask !== null ? call.ask : "-",
                    call_last: call && call.last !== undefined && call.last !== null ? call.last : (call && call.price !== undefined && call.price !== null ? call.price : "-"),
                    call_contract: call,

                    // PUTS (Derecha)
                    put_bid: put && put.bid !== undefined && put.bid !== null ? put.bid : "-",
                    put_ask: put && put.ask !== undefined && put.ask !== null ? put.ask : "-",
                    put_last: put && put.last !== undefined && put.last !== null ? put.last : (put && put.price !== undefined && put.price !== null ? put.price : "-"),
                    put_contract: put
                }
            })
        },
        obtener_strikes() {
            if (!this.instrumento_seleccionado || !this.expiracion_seleccionada) {
                this.chain_rows = []
                return
            }

            const symbol = this.instrumento_seleccionado.symbol
            const expiracion = this.expiracion_seleccionada

            this.cargando_strikes = true
            const params = {
                cod_subyacente: symbol,
                fch_expiracion: expiracion,
                num_strikes: this.num_strikes_seleccionado
            }

            Ibkr.get_options_chain(params)
                .then(httpresponse => {
                    if (
                        !this.instrumento_seleccionado ||
                        this.instrumento_seleccionado.symbol !== symbol ||
                        this.expiracion_seleccionada !== expiracion
                    ) {
                        return
                    }

                    const res = httpresponse.data
                    const data = (res && res.data) ? res.data : (res || {})

                    // Colocar fechas_vencimiento en el select si se recibieron del backend
                    const fechas = (data && Array.isArray(data.fechas_vencimiento))
                        ? data.fechas_vencimiento
                        : (data && Array.isArray(data.exp_dates) ? data.exp_dates : [])

                    if (fechas.length > 0 && this.expiraciones_disponibles.length <= 1) {
                        this.expiraciones_disponibles = fechas.map(f => ({
                            label: `${f} (${this.formatear_expiracion(f)})`,
                            value: f
                        }))
                    }

                    this.cargar_datos_cadena(data)
                })
                .catch(error => {
                    console.log(error)
                    // Fallback a get_strikes si get_options_chain no estuviera disponible
                    Ibkr.get_strikes({
                        cod_subyacente: symbol,
                        expiracion: expiracion
                    }).then(httpresponse => {
                        if (
                            !this.instrumento_seleccionado ||
                            this.instrumento_seleccionado.symbol !== symbol ||
                            this.expiracion_seleccionada !== expiracion
                        ) {
                            return
                        }

                        const res = httpresponse.data
                        const data = (res && res.data) ? res.data : (res || {})
                        const callStrikes = Array.isArray(data.call) ? data.call : []
                        const putStrikes = Array.isArray(data.put) ? data.put : []

                        const strikesSet = new Set([...callStrikes, ...putStrikes].map(s => Number(s)))
                        const sortedStrikes = Array.from(strikesSet).sort((a, b) => a - b)
                        const callSet = new Set(callStrikes.map(s => Number(s)))
                        const putSet = new Set(putStrikes.map(s => Number(s)))

                        this.chain_rows = sortedStrikes.map(strike => ({
                            strike: strike,
                            is_call_itm: false,
                            is_put_itm: false,
                            call_bid: callSet.has(strike) ? "-" : "",
                            call_ask: callSet.has(strike) ? "-" : "",
                            call_last: callSet.has(strike) ? "-" : "",
                            call_contract: null,
                            put_bid: putSet.has(strike) ? "-" : "",
                            put_ask: putSet.has(strike) ? "-" : "",
                            put_last: putSet.has(strike) ? "-" : "",
                            put_contract: null
                        }))
                    }).catch(errStrikes => {
                        if (
                            this.instrumento_seleccionado &&
                            this.instrumento_seleccionado.symbol === symbol &&
                            this.expiracion_seleccionada === expiracion
                        ) {
                            console.error("Error al obtener strikes de IBKR:", errStrikes)
                            const msg = errStrikes.response && errStrikes.response.data && errStrikes.response.data.message
                                ? errStrikes.response.data.message
                                : (errStrikes.message || "Error al conectar con IBKR")
                            this.$q.notify({
                                type: 'warning',
                                message: `No se pudieron cargar strikes de IBKR (${msg}).`,
                                timeout: 3000
                            })
                            this.chain_rows = []
                        }
                    })
                })
                .finally(() => {
                    if (
                        this.instrumento_seleccionado &&
                        this.instrumento_seleccionado.symbol === symbol &&
                        this.expiracion_seleccionada === expiracion
                    ) {
                        this.cargando_strikes = false
                    }
                })
        },
        formatear_expiracion(raw) {
            if (!raw) return ""
            const str = String(raw).trim()

            const meses = {
                JAN: { nombre: "Enero", abrev: "Ene" },
                ENE: { nombre: "Enero", abrev: "Ene" },
                FEB: { nombre: "Febrero", abrev: "Feb" },
                MAR: { nombre: "Marzo", abrev: "Mar" },
                APR: { nombre: "Abril", abrev: "Abr" },
                ABR: { nombre: "Abril", abrev: "Abr" },
                MAY: { nombre: "Mayo", abrev: "May" },
                JUN: { nombre: "Junio", abrev: "Jun" },
                JUL: { nombre: "Julio", abrev: "Jul" },
                AUG: { nombre: "Agosto", abrev: "Ago" },
                AGO: { nombre: "Agosto", abrev: "Ago" },
                SEP: { nombre: "Septiembre", abrev: "Sep" },
                SET: { nombre: "Septiembre", abrev: "Sep" },
                OCT: { nombre: "Octubre", abrev: "Oct" },
                NOV: { nombre: "Noviembre", abrev: "Nov" },
                DEC: { nombre: "Diciembre", abrev: "Dic" },
                DIC: { nombre: "Diciembre", abrev: "Dic" }
            }

            const mesesNum = [
                "", "Ene", "Feb", "Mar", "Abr", "May", "Jun",
                "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
            ]

            // Caso 1: YYYYMMDD (ej: 20261017) o YYYY-MM-DD
            const matchYMD = str.match(/^(\d{4})[-/]?(\d{2})[-/]?(\d{2})$/)
            if (matchYMD) {
                const y = matchYMD[1]
                const m = parseInt(matchYMD[2], 10)
                const d = parseInt(matchYMD[3], 10)
                const mesTxt = mesesNum[m] || matchYMD[2]
                return `${d} ${mesTxt} ${y}`
            }

            // Caso 2: DDMMMYY o DD-MMM-YYYY (ej: 17OCT26, 17-OCT-2026)
            const matchDMY = str.match(/^(\d{1,2})[-/]?([A-Za-z]{3})[-/]?(\d{2,4})$/)
            if (matchDMY) {
                const d = parseInt(matchDMY[1], 10)
                const mKey = matchDMY[2].toUpperCase()
                let y = matchDMY[3]
                if (y.length === 2) y = `20${y}`
                const mesTxt = meses[mKey] ? meses[mKey].abrev : mKey
                return `${d} ${mesTxt} ${y}`
            }

            // Caso 3: MMMYY (ej: OCT26, NOV26, JAN27)
            const matchMY = str.match(/^([A-Za-z]{3})[-/]?(\d{2,4})$/)
            if (matchMY) {
                const mKey = matchMY[1].toUpperCase()
                let y = matchMY[2]
                if (y.length === 2) y = `20${y}`
                const mesTxt = meses[mKey] ? meses[mKey].nombre : mKey
                return `${mesTxt} ${y}`
            }

            // Caso 4: YYYYMM (ej: 202610)
            const matchYM = str.match(/^(\d{4})[-/]?(\d{2})$/)
            if (matchYM) {
                const y = matchYM[1]
                const m = parseInt(matchYM[2], 10)
                const mesTxt = mesesNum[m] || matchYM[2]
                return `${mesTxt} ${y}`
            }

            return str
        }
    }
}
</script>
