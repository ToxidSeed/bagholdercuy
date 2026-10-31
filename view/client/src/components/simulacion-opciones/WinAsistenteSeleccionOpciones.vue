<template>
  <q-dialog v-model="open" persistent>
    <q-card class="asistente-card" style="width: 1500px; max-width: 98vw; height: 92vh; max-height: 94vh; display: flex; flex-direction: column;">
      
      <!-- HEADER DEL ASISTENTE -->
      <q-toolbar class="bg-blue-10 text-white q-py-sm">
        <q-btn
          v-if="paso_actual === 2"
          flat
          round
          dense
          icon="arrow_back"
          color="white"
          class="q-mr-sm"
          @click="volver_a_paso_1"
        >
          <q-tooltip>Cambiar Instrumento</q-tooltip>
        </q-btn>
        
        <q-avatar icon="auto_graph" size="32px" class="bg-blue-9 text-white q-mr-sm" />
        
        <q-toolbar-title class="text-subtitle1 text-weight-bold">
          <span v-if="paso_actual === 1">Asistente · Paso 1: Seleccionar Instrumento</span>
          <span v-else>
            Asistente · Paso 2: Cadena de Opciones · 
            <span class="text-amber-3 text-weight-bolder">{{ instrumento_seleccionado ? instrumento_seleccionado.symbol : '' }}</span>
          </span>
        </q-toolbar-title>

        <!-- Indicador de pasos -->
        <div class="row items-center q-gutter-xs q-mr-md gt-xs">
          <q-badge :color="paso_actual === 1 ? 'amber-8' : 'blue-8'" text-color="white" class="text-caption text-weight-bold">
            1. Instrumento
          </q-badge>
          <q-icon name="chevron_right" size="14px" color="blue-3" />
          <q-badge :color="paso_actual === 2 ? 'amber-8' : 'blue-8'" text-color="white" class="text-caption text-weight-bold">
            2. Contratos de Opciones
          </q-badge>
        </div>

        <q-btn flat round dense icon="close" color="white" v-close-popup />
      </q-toolbar>

      <!-- CUERPO DEL ASISTENTE -->
      <q-card-section class="q-pa-none col" style="overflow-y: auto;">

        <!-- ======================================================== -->
        <!-- PASO 1: SELECCIONAR INSTRUMENTO (STOCKS, ETFS, INDICES)  -->
        <!-- ======================================================== -->
        <div v-if="paso_actual === 1" class="q-pa-md">
          <div class="q-mb-md">
            <div class="text-subtitle1 text-weight-bold text-blue-10 q-mb-xs">
              Buscar Activo Subyacente
            </div>
            <div class="text-caption text-grey-7">
              Seleccione una Acción, ETF o Índice para consultar su cadena de opciones. 
              <span class="text-primary text-weight-medium">(No añade el instrumento a la watchlist ni a la base de datos).</span>
            </div>
          </div>

          <!-- Input de búsqueda -->
          <q-input
            v-model="filtro_texto"
            placeholder="Buscar por símbolo o nombre (ej: AAPL, SPY, QQQ, NVDA, TSLA)..."
            outlined
            dense
            color="blue-10"
            clearable
            autofocus
            debounce="400"
            :loading="cargando_busqueda"
            @input="buscar_instrumentos"
          >
            <template v-slot:prepend>
              <q-icon name="search" color="blue-10" />
            </template>
          </q-input>

          <!-- Filtros de Tipo de Activo: STOCKS, ETFS, INDICES -->
          <div class="row items-center q-gutter-xs q-mt-sm q-mb-md">
            <span class="text-caption text-grey-8 text-weight-medium q-mr-xs">Filtrar por:</span>
            <q-chip
              clickable
              dense
              :color="filtro_tipo === 'TODOS' ? 'blue-10' : 'grey-2'"
              :text-color="filtro_tipo === 'TODOS' ? 'white' : 'grey-8'"
              @click="cambiar_filtro_tipo('TODOS')"
            >
              Todos (Permitidos)
            </q-chip>
            <q-chip
              clickable
              dense
              icon="business"
              :color="filtro_tipo === 'STOCK' ? 'blue-10' : 'grey-2'"
              :text-color="filtro_tipo === 'STOCK' ? 'white' : 'grey-8'"
              @click="cambiar_filtro_tipo('STOCK')"
            >
              Acciones (Stocks)
            </q-chip>
            <q-chip
              clickable
              dense
              icon="layers"
              :color="filtro_tipo === 'ETF' ? 'blue-10' : 'grey-2'"
              :text-color="filtro_tipo === 'ETF' ? 'white' : 'grey-8'"
              @click="cambiar_filtro_tipo('ETF')"
            >
              ETFs
            </q-chip>
            <q-chip
              clickable
              dense
              icon="show_chart"
              :color="filtro_tipo === 'INDICE' ? 'blue-10' : 'grey-2'"
              :text-color="filtro_tipo === 'INDICE' ? 'white' : 'grey-8'"
              @click="cambiar_filtro_tipo('INDICE')"
            >
              Índices
            </q-chip>
          </div>

          <!-- Sugerencias rápidas cuando el buscador está vacío -->
          <div v-if="!filtro_texto && coincidencias.length === 0" class="q-py-sm">
            <div class="text-caption text-grey-6 text-weight-medium q-mb-xs">
              Instrumentos populares para análisis de opciones:
            </div>
            <div class="row q-gutter-sm">
              <q-btn
                v-for="sug in sugerencias_populares"
                :key="sug.symbol"
                outline
                dense
                no-caps
                size="sm"
                color="blue-10"
                class="q-px-sm"
                @click="seleccionar_sugerencia(sug)"
              >
                <span class="text-weight-bold q-mr-xs">{{ sug.symbol }}</span>
                <span class="text-caption text-grey-7">{{ sug.tipo }}</span>
              </q-btn>
            </div>
          </div>

          <!-- Lista de resultados -->
          <div v-if="coincidencias_filtradas.length > 0" class="q-mt-sm">
            <q-scroll-area style="height: calc(92vh - 280px); min-height: 380px;">
              <q-list separator bordered class="rounded-borders">
                <q-item
                  v-for="item in coincidencias_filtradas"
                  :key="item.id || item.symbol"
                  clickable
                  v-ripple
                  class="instrumento-item"
                  @click="elegir_instrumento(item)"
                >
                  <q-item-section avatar>
                    <q-avatar
                      size="36px"
                      :color="obtener_color_tipo(item.asset_type)"
                      text-color="white"
                      class="text-weight-bold"
                    >
                      {{ item.symbol.substring(0, 2) }}
                    </q-avatar>
                  </q-item-section>

                  <q-item-section>
                    <div class="row items-center no-wrap">
                      <span class="text-subtitle1 text-weight-bolder text-blue-10 q-mr-sm">
                        {{ item.symbol }}
                      </span>
                      <q-badge
                        :color="obtener_badge_bg(item.asset_type)"
                        :text-color="obtener_badge_txt(item.asset_type)"
                        :label="item.asset_type || 'STOCK'"
                        class="text-caption text-weight-bold"
                      />
                      <span v-if="item.exchange" class="text-caption text-grey-6 q-ml-sm">
                        {{ item.exchange }}
                      </span>
                    </div>
                    <q-item-label caption class="text-grey-8 ellipsis" style="max-width: 480px;">
                      {{ item.name }}
                    </q-item-label>
                  </q-item-section>

                  <q-item-section side>
                    <q-btn
                      unelevated
                      dense
                      no-caps
                      color="blue-10"
                      label="Seleccionar"
                      icon-right="arrow_forward"
                      size="sm"
                      class="q-px-sm text-weight-medium"
                      @click.stop="elegir_instrumento(item)"
                    />
                  </q-item-section>
                </q-item>
              </q-list>
            </q-scroll-area>
          </div>

          <div v-else-if="cargando_busqueda" class="text-center q-pa-xl">
            <q-spinner color="blue-10" size="2.5em" />
            <div class="text-caption text-grey-7 q-mt-sm">Buscando instrumentos...</div>
          </div>

          <div v-else-if="filtro_texto && coincidencias_filtradas.length === 0" class="text-center text-grey-7 q-pa-xl">
            <q-icon name="search_off" size="40px" class="text-grey-5 q-mb-sm" />
            <div class="text-body2">No se encontraron Stocks, ETFs o Índices para "{{ filtro_texto }}"</div>
            <div class="text-caption text-grey-5">Pruebe con otro símbolo como SPY, QQQ, AAPL o MSFT</div>
          </div>
        </div>

        <!-- ======================================================== -->
        <!-- PASO 2: CADENA DE OPCIONES (SELECCIÓN MÚLTIPLE)          -->
        <!-- ======================================================== -->
        <div v-else-if="paso_actual === 2" class="q-pa-md">
          
          <!-- Resumen del activo seleccionado + Filtros de la cadena -->
          <div class="row items-center justify-between q-col-gutter-sm q-mb-sm">
            <div class="col-12 col-md-auto row items-center">
              <span class="text-h6 text-weight-bolder text-blue-10 q-mr-sm">
                {{ instrumento_seleccionado ? instrumento_seleccionado.symbol : '' }}
              </span>
              <span class="text-body2 text-grey-8 q-mr-sm ellipsis" style="max-width: 240px;">
                {{ instrumento_seleccionado ? instrumento_seleccionado.name : '' }}
              </span>
              <q-badge
                :color="obtener_badge_bg(instrumento_seleccionado ? instrumento_seleccionado.asset_type : '')"
                :text-color="obtener_badge_txt(instrumento_seleccionado ? instrumento_seleccionado.asset_type : '')"
                :label="(instrumento_seleccionado && instrumento_seleccionado.asset_type) || 'STOCK'"
                class="text-caption text-weight-bold"
              />
              <q-btn
                flat
                dense
                no-caps
                size="sm"
                color="primary"
                icon="swap_horiz"
                label="Cambiar"
                class="q-ml-sm"
                @click="volver_a_paso_1"
              />
            </div>

            <div class="col-12 col-md-auto row items-center q-gutter-sm">
              <div class="row items-center no-wrap">
                <span class="text-caption text-weight-bold text-grey-8 q-mr-xs">Expiración:</span>
                <q-select
                  v-model="expiracion_seleccionada"
                  :options="expiraciones_disponibles"
                  dense
                  outlined
                  options-dense
                  color="blue-10"
                  style="min-width: 170px;"
                  :loading="cargando_expiraciones || cargando_strikes"
                  emit-value
                  map-options
                />
              </div>

              <div class="row items-center no-wrap">
                <span class="text-caption text-weight-bold text-grey-8 q-mr-xs">Strikes:</span>
                <q-select
                  v-model="num_strikes_seleccionado"
                  :options="num_strikes_opciones"
                  dense
                  outlined
                  options-dense
                  color="blue-10"
                  style="min-width: 90px;"
                  :loading="cargando_strikes"
                  emit-value
                  map-options
                />
              </div>
            </div>
          </div>

          <!-- Barra de ayuda para selección múltiple -->
          <div class="row items-center justify-between bg-blue-1 text-blue-10 q-pa-xs rounded-borders q-mb-sm text-caption">
            <div class="row items-center">
              <q-icon name="touch_app" size="16px" class="q-mr-xs" />
              <span>Marque las casillas para <strong>selección múltiple</strong> de contratos CALLs y PUTs.</span>
            </div>
            <div class="row items-center q-gutter-xs">
              <span class="text-weight-bold">
                {{ contratos_seleccionados_temporal.length }} seleccionados
              </span>
              <q-btn
                v-if="contratos_seleccionados_temporal.length > 0"
                flat
                dense
                no-caps
                size="xs"
                color="red-9"
                label="Limpiar selección"
                @click="contratos_seleccionados_temporal = []"
              />
            </div>
          </div>

          <!-- Tabla Unificada de Cadena de Opciones con Selección Múltiple -->
          <q-card flat bordered class="rounded-borders">
            <q-table
              :data="chain_rows"
              :columns="chain_columns"
              row-key="strike"
              dense
              flat
              hide-pagination
              :pagination="{ rowsPerPage: 0 }"
              :loading="cargando_strikes"
              style="height: calc(92vh - 270px); max-height: calc(92vh - 270px); overflow-y: auto;"
            >
              <template v-slot:header="props">
                <q-tr>
                  <q-th colspan="5" class="text-center bg-blue-1 text-bold text-blue-10" style="border-right: 2px solid #90caf9;">
                    <q-icon name="call_made" color="blue-9" class="q-mr-xs" /> CALLS
                  </q-th>
                  <q-th class="text-center bg-grey-3 text-bold text-grey-9" style="border-right: 2px solid #e0e0e0; min-width: 90px;">
                    STRIKE
                  </q-th>
                  <q-th colspan="5" class="text-center bg-purple-1 text-bold text-purple-10">
                    <q-icon name="call_received" color="purple-9" class="q-mr-xs" /> PUTS
                  </q-th>
                </q-tr>
                <q-tr :props="props">
                  <!-- CALLS -->
                  <q-th key="call_sel" :props="props" class="bg-blue-1 text-blue-10 text-center" style="width: 44px;">Sel</q-th>
                  <q-th key="call_bid" :props="props" class="bg-blue-1 text-blue-10 text-right">Bid</q-th>
                  <q-th key="call_ask" :props="props" class="bg-blue-1 text-blue-10 text-right">Ask</q-th>
                  <q-th key="call_last" :props="props" class="bg-blue-1 text-blue-10 text-right">Last</q-th>
                  <q-th key="call_vol" :props="props" class="bg-blue-1 text-blue-10 text-right" style="border-right: 2px solid #90caf9;">Vol</q-th>

                  <!-- STRIKE -->
                  <q-th key="strike" :props="props" class="bg-grey-3 text-bold text-grey-9 text-center" style="border-right: 2px solid #e0e0e0;">
                    Strike
                  </q-th>

                  <!-- PUTS -->
                  <q-th key="put_vol" :props="props" class="bg-purple-1 text-purple-10 text-left">Vol</q-th>
                  <q-th key="put_last" :props="props" class="bg-purple-1 text-purple-10 text-left">Last</q-th>
                  <q-th key="put_bid" :props="props" class="bg-purple-1 text-purple-10 text-right">Bid</q-th>
                  <q-th key="put_ask" :props="props" class="bg-purple-1 text-purple-10 text-right">Ask</q-th>
                  <q-th key="put_sel" :props="props" class="bg-purple-1 text-purple-10 text-center" style="width: 44px;">Sel</q-th>
                </q-tr>
              </template>

              <template v-slot:body="props">
                <q-tr :props="props">
                  <!-- CALL SEL -->
                  <q-td
                    key="call_sel"
                    :props="props"
                    class="text-center q-pa-none"
                    :class="esta_contrato_seleccionado(props.row.strike, 'CALL') ? 'bg-blue-2' : (props.row.is_call_itm ? 'bg-blue-1' : '')"
                  >
                    <q-checkbox
                      :value="esta_contrato_seleccionado(props.row.strike, 'CALL')"
                      color="blue-10"
                      dense
                      size="sm"
                      @input="toggle_seleccion_contrato(props.row, 'CALL')"
                    />
                  </q-td>

                  <!-- CALL BID -->
                  <q-td
                    key="call_bid"
                    :props="props"
                    class="cursor-pointer"
                    :class="esta_contrato_seleccionado(props.row.strike, 'CALL') ? 'bg-blue-2 text-weight-bold' : (props.row.is_call_itm ? 'bg-blue-1' : '')"
                    @click="toggle_seleccion_contrato(props.row, 'CALL')"
                  >
                    {{ formatear_precio(props.row.call_bid) }}
                  </q-td>

                  <!-- CALL ASK -->
                  <q-td
                    key="call_ask"
                    :props="props"
                    class="cursor-pointer"
                    :class="esta_contrato_seleccionado(props.row.strike, 'CALL') ? 'bg-blue-2 text-weight-bold' : (props.row.is_call_itm ? 'bg-blue-1' : '')"
                    @click="toggle_seleccion_contrato(props.row, 'CALL')"
                  >
                    {{ formatear_precio(props.row.call_ask) }}
                  </q-td>

                  <!-- CALL LAST -->
                  <q-td
                    key="call_last"
                    :props="props"
                    class="cursor-pointer"
                    :class="esta_contrato_seleccionado(props.row.strike, 'CALL') ? 'bg-blue-2 text-weight-bold' : (props.row.is_call_itm ? 'bg-blue-1' : '')"
                    @click="toggle_seleccion_contrato(props.row, 'CALL')"
                  >
                    {{ formatear_precio(props.row.call_last) }}
                  </q-td>

                  <!-- CALL VOL -->
                  <q-td
                    key="call_vol"
                    :props="props"
                    style="border-right: 2px solid #bbdefb;"
                    :class="esta_contrato_seleccionado(props.row.strike, 'CALL') ? 'bg-blue-2' : (props.row.is_call_itm ? 'bg-blue-1' : '')"
                  >
                    {{ props.row.call_vol || '-' }}
                  </q-td>

                  <!-- STRIKE CENTRAL -->
                  <q-td
                    key="strike"
                    :props="props"
                    class="bg-grey-2 text-bold text-blue-10 text-center"
                    style="border-right: 2px solid #e0e0e0; font-size: 13px;"
                  >
                    ${{ Number(props.row.strike).toFixed(2) }}
                  </q-td>

                  <!-- PUT VOL -->
                  <q-td
                    key="put_vol"
                    :props="props"
                    :class="esta_contrato_seleccionado(props.row.strike, 'PUT') ? 'bg-purple-2' : (props.row.is_put_itm ? 'bg-purple-1' : '')"
                  >
                    {{ props.row.put_vol || '-' }}
                  </q-td>

                  <!-- PUT LAST -->
                  <q-td
                    key="put_last"
                    :props="props"
                    class="cursor-pointer"
                    :class="esta_contrato_seleccionado(props.row.strike, 'PUT') ? 'bg-purple-2 text-weight-bold' : (props.row.is_put_itm ? 'bg-purple-1' : '')"
                    @click="toggle_seleccion_contrato(props.row, 'PUT')"
                  >
                    {{ formatear_precio(props.row.put_last) }}
                  </q-td>

                  <!-- PUT BID -->
                  <q-td
                    key="put_bid"
                    :props="props"
                    class="cursor-pointer"
                    :class="esta_contrato_seleccionado(props.row.strike, 'PUT') ? 'bg-purple-2 text-weight-bold' : (props.row.is_put_itm ? 'bg-purple-1' : '')"
                    @click="toggle_seleccion_contrato(props.row, 'PUT')"
                  >
                    {{ formatear_precio(props.row.put_bid) }}
                  </q-td>

                  <!-- PUT ASK -->
                  <q-td
                    key="put_ask"
                    :props="props"
                    class="cursor-pointer"
                    :class="esta_contrato_seleccionado(props.row.strike, 'PUT') ? 'bg-purple-2 text-weight-bold' : (props.row.is_put_itm ? 'bg-purple-1' : '')"
                    @click="toggle_seleccion_contrato(props.row, 'PUT')"
                  >
                    {{ formatear_precio(props.row.put_ask) }}
                  </q-td>

                  <!-- PUT SEL -->
                  <q-td
                    key="put_sel"
                    :props="props"
                    class="text-center q-pa-none"
                    :class="esta_contrato_seleccionado(props.row.strike, 'PUT') ? 'bg-purple-2' : (props.row.is_put_itm ? 'bg-purple-1' : '')"
                  >
                    <q-checkbox
                      :value="esta_contrato_seleccionado(props.row.strike, 'PUT')"
                      color="purple-9"
                      dense
                      size="sm"
                      @input="toggle_seleccion_contrato(props.row, 'PUT')"
                    />
                  </q-td>
                </q-tr>
              </template>

              <template v-slot:no-data>
                <div class="full-width text-center text-grey-6 q-pa-lg">
                  <q-spinner v-if="cargando_strikes" color="blue-10" size="2em" class="q-mb-xs" />
                  <div v-else>No hay contratos de opciones disponibles para esta expiración</div>
                </div>
              </template>
            </q-table>
          </q-card>

          <!-- Chips preview de los contratos seleccionados -->
          <div v-if="contratos_seleccionados_temporal.length > 0" class="q-mt-sm">
            <div class="text-caption text-weight-bold text-grey-8 q-mb-xs">
              Contratos seleccionados para la pantalla principal ({{ contratos_seleccionados_temporal.length }}):
            </div>
            <div class="row q-gutter-xs items-center" style="max-height: 70px; overflow-y: auto;">
              <q-chip
                v-for="item in contratos_seleccionados_temporal"
                :key="item.cod_symbol"
                removable
                dense
                size="sm"
                :color="item.tipo === 'CALL' ? 'blue-2' : 'purple-2'"
                :text-color="item.tipo === 'CALL' ? 'blue-10' : 'purple-10'"
                @remove="remover_contrato_temporal(item.cod_symbol)"
              >
                <q-icon :name="item.tipo === 'CALL' ? 'call_made' : 'call_received'" size="12px" class="q-mr-xs" />
                <span class="text-weight-bold">{{ item.tipo }} ${{ item.strike }}</span>
                <span class="q-ml-xs text-grey-8">({{ item.expiracion_corta }} · {{ formatear_dias_expiracion(item) }})</span>
              </q-chip>
            </div>
          </div>
        </div>
      </q-card-section>

      <!-- BARRA INFERIOR / ACCIONES DEL ASISTENTE -->
      <q-separator />
      <q-card-actions align="between" class="bg-grey-1 q-px-md q-py-sm">
        <div>
          <q-btn
            v-if="paso_actual === 2"
            flat
            no-caps
            color="grey-8"
            icon="arrow_back"
            label="Elegir otro instrumento"
            @click="volver_a_paso_1"
          />
        </div>

        <div class="row q-gutter-sm items-center">
          <q-btn flat no-caps label="Cancelar" color="grey-8" v-close-popup />
          
          <q-btn
            v-if="paso_actual === 2"
            unelevated
            no-caps
            color="blue-10"
            icon="check_circle"
            :label="`Confirmar Selección (${contratos_seleccionados_temporal.length})`"
            @click="confirmar_seleccion_final"
          />
        </div>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { headers } from '@/common/common.js'
import Ibkr from '@/api/ibkr.js'
import moment from 'moment'

export default {
  name: "WinAsistenteSeleccionOpciones",
  props: {
    value: {
      type: Boolean,
      default: false
    },
    // Contratos previamente seleccionados para mantener sincronizados los checkboxes
    contratosIniciales: {
      type: Array,
      default: () => []
    },
    // Instrumento previamente seleccionado
    instrumentoInicial: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      open: this.value,
      paso_actual: 1, // 1: Seleccionar instrumento, 2: Cadena de opciones
      filtro_texto: "",
      filtro_tipo: "TODOS", // TODOS, STOCK, ETF, INDICE
      cargando_busqueda: false,
      coincidencias: [],
      sugerencias_populares: [
        { symbol: "AAPL", name: "Apple Inc.", tipo: "STOCK", asset_type: "STOCK", exchange: "NASDAQ" },
        { symbol: "SPY", name: "SPDR S&P 500 ETF Trust", tipo: "ETF", asset_type: "ETF", exchange: "ARCA" },
        { symbol: "QQQ", name: "Invesco QQQ Trust", tipo: "ETF", asset_type: "ETF", exchange: "NASDAQ" },
        { symbol: "NVDA", name: "NVIDIA Corporation", tipo: "STOCK", asset_type: "STOCK", exchange: "NASDAQ" },
        { symbol: "MSFT", name: "Microsoft Corporation", tipo: "STOCK", asset_type: "STOCK", exchange: "NASDAQ" },
        { symbol: "TSLA", name: "Tesla Inc.", tipo: "STOCK", asset_type: "STOCK", exchange: "NASDAQ" },
        { symbol: "SPX", name: "S&P 500 Index", tipo: "INDICE", asset_type: "INDICE", exchange: "CBOE" }
      ],
      instrumento_seleccionado: null,

      // Estado cadena de opciones
      cargando_expiraciones: false,
      cargando_strikes: false,
      expiraciones_disponibles: [],
      expiracion_seleccionada: null,
      num_strikes_seleccionado: 20,
      num_strikes_opciones: [
        { label: "10 Strikes", value: 10 },
        { label: "20 Strikes", value: 20 },
        { label: "30 Strikes", value: 30 },
        { label: "40 Strikes", value: 40 },
        { label: "Todos", value: 0 }
      ],
      chain_rows: [],
      chain_columns: [
        { name: "call_sel", label: "", field: "call_sel", align: "center" },
        { name: "call_bid", label: "Bid", field: "call_bid", align: "right" },
        { name: "call_ask", label: "Ask", field: "call_ask", align: "right" },
        { name: "call_last", label: "Last", field: "call_last", align: "right" },
        { name: "call_vol", label: "Vol", field: "call_vol", align: "right" },
        { name: "strike", label: "Strike", field: "strike", align: "center" },
        { name: "put_vol", label: "Vol", field: "put_vol", align: "left" },
        { name: "put_last", label: "Last", field: "put_last", align: "left" },
        { name: "put_bid", label: "Bid", field: "put_bid", align: "right" },
        { name: "put_ask", label: "Ask", field: "put_ask", align: "right" },
        { name: "put_sel", label: "", field: "put_sel", align: "center" }
      ],
      // Lista de contratos seleccionados temporalmente en el asistente
      contratos_seleccionados_temporal: []
    }
  },
  computed: {
    coincidencias_filtradas() {
      if (!this.coincidencias || this.coincidencias.length === 0) return []
      if (this.filtro_tipo === "TODOS") return this.coincidencias

      return this.coincidencias.filter(item => {
        const tipoNorm = String(item.asset_type || item.tipo || "").toUpperCase()
        if (this.filtro_tipo === "STOCK") {
          return tipoNorm.includes("STOCK") || tipoNorm.includes("EQUITY") || tipoNorm.includes("ACCION")
        }
        if (this.filtro_tipo === "ETF") {
          return tipoNorm.includes("ETF") || tipoNorm.includes("FUND")
        }
        if (this.filtro_tipo === "INDICE") {
          return tipoNorm.includes("IND") || tipoNorm.includes("INDEX")
        }
        return true
      })
    }
  },
  watch: {
    value(newval) {
      this.open = newval
      if (newval) {
        // Inicializar datos
        if (this.instrumentoInicial) {
          this.instrumento_seleccionado = { ...this.instrumentoInicial }
          this.contratos_seleccionados_temporal = [...this.contratosIniciales]
          this.paso_actual = 2
          this.cargar_cadena_instrumento(this.instrumento_seleccionado)
        } else {
          this.paso_actual = 1
          this.filtro_texto = ""
          this.coincidencias = []
          this.contratos_seleccionados_temporal = [...this.contratosIniciales]
        }
      }
    },
    open(newval) {
      this.$emit("input", newval)
    },
    expiracion_seleccionada(newval) {
      if (newval && this.paso_actual === 2 && this.instrumento_seleccionado) {
        this.obtener_strikes()
      }
    },
    num_strikes_seleccionado() {
      if (this.paso_actual === 2 && this.instrumento_seleccionado && this.expiracion_seleccionada) {
        this.obtener_strikes()
      }
    }
  },
  methods: {
    cambiar_filtro_tipo(tipo) {
      this.filtro_tipo = tipo
    },
    volver_a_paso_1() {
      this.paso_actual = 1
    },
    obtener_color_tipo(asset_type) {
      const tipo = String(asset_type || "").toUpperCase()
      if (tipo.includes("ETF")) return "purple-8"
      if (tipo.includes("IND")) return "teal-8"
      return "blue-9"
    },
    obtener_badge_bg(asset_type) {
      const tipo = String(asset_type || "").toUpperCase()
      if (tipo.includes("ETF")) return "purple-1"
      if (tipo.includes("IND")) return "teal-1"
      return "blue-1"
    },
    obtener_badge_txt(asset_type) {
      const tipo = String(asset_type || "").toUpperCase()
      if (tipo.includes("ETF")) return "purple-10"
      if (tipo.includes("IND")) return "teal-10"
      return "blue-10"
    },
    buscar_instrumentos(val) {
      if (!val || !val.trim()) {
        this.coincidencias = []
        this.cargando_busqueda = false
        return
      }

      this.cargando_busqueda = true
      this.$http.post(
        'SymbolManager/SymbolFinder/buscar_por_texto',
        { texto: val.trim() },
        { headers: headers() }
      ).then(httpresp => {
        const appresponse = httpresp.data
        const items = []
        if (appresponse && Array.isArray(appresponse.data)) {
          for (let el of appresponse.data) {
            const rawType = String(el.asset_type || "STOCK").toUpperCase()
            // Filtrar SOLO Stocks, ETFs e Índices (excluir opciones, forex, etc.)
            const esPermitido = 
              rawType.includes("STOCK") || 
              rawType.includes("EQUITY") || 
              rawType.includes("ACCION") || 
              rawType.includes("ETF") || 
              rawType.includes("FUND") || 
              rawType.includes("INDEX") || 
              rawType.includes("INDICE") ||
              !el.asset_type // Por defecto si viene vacío se asume stock

            if (esPermitido) {
              const idSymbol = el.id_symbol || el.id
              items.push({
                id: idSymbol,
                id_symbol: idSymbol,
                symbol: el.symbol,
                name: el.name || el.symbol,
                tipo: rawType,
                asset_type: rawType,
                exchange: el.exchange || "",
                id_symbol_type: el.id_symbol_type || 1
              })
            }
          }
        }
        this.coincidencias = items
      }).catch(err => {
        console.error("Error buscando instrumentos:", err)
        // Fallback local con sugerencias si el backend está en desarrollo
        const q = val.trim().toUpperCase()
        this.coincidencias = this.sugerencias_populares.filter(s => 
          s.symbol.includes(q) || s.name.toUpperCase().includes(q)
        )
      }).finally(() => {
        this.cargando_busqueda = false
      })
    },
    seleccionar_sugerencia(sug) {
      this.elegir_instrumento({ ...sug })
    },
    elegir_instrumento(item) {
      this.instrumento_seleccionado = { ...item }
      this.paso_actual = 2
      this.cargar_cadena_instrumento(this.instrumento_seleccionado)
    },
    cargar_cadena_instrumento(item) {
      this.cargando_expiraciones = true
      this.cargando_strikes = true
      this.expiraciones_disponibles = []
      this.expiracion_seleccionada = null
      this.chain_rows = []

      // Intentar llamar a Ibkr.get_options_chain
      Ibkr.get_options_chain({
        cod_subyacente: item.symbol,
        num_strikes: this.num_strikes_seleccionado
      }).then(httpresponse => {
        const res = httpresponse.data
        const data = (res && res.data) ? res.data : (res || {})
        const fechas = (data && Array.isArray(data.fechas_vencimiento))
          ? data.fechas_vencimiento
          : (data && Array.isArray(data.exp_dates) ? data.exp_dates : [])

        if (fechas.length > 0) {
          this.expiraciones_disponibles = fechas.map(f => ({
            label: `${f} (${this.formatear_expiracion(f)})`,
            value: f
          }))
          this.expiracion_seleccionada = data.fch_vencimiento || fechas[0]
          this.cargar_datos_cadena(data)
        } else {
          this.generar_cadena_mock(item)
        }
      }).catch(error => {
        console.warn("IBKR options chain no disponible en este momento, usando simulador de opciones:", error)
        this.generar_cadena_mock(item)
      }).finally(() => {
        this.cargando_expiraciones = false
        this.cargando_strikes = false
      })
    },
    obtener_strikes() {
      if (!this.instrumento_seleccionado || !this.expiracion_seleccionada) return
      
      this.cargando_strikes = true
      Ibkr.get_options_chain({
        cod_subyacente: this.instrumento_seleccionado.symbol,
        fch_expiracion: this.expiracion_seleccionada,
        num_strikes: this.num_strikes_seleccionado
      }).then(httpresponse => {
        const res = httpresponse.data
        const data = (res && res.data) ? res.data : (res || {})
        this.cargar_datos_cadena(data)
      }).catch(() => {
        this.generar_cadena_mock(this.instrumento_seleccionado)
      }).finally(() => {
        this.cargando_strikes = false
      })
    },
    cargar_datos_cadena(data) {
      const rawCalls = Array.isArray(data.calls) ? data.calls : []
      const rawPuts = Array.isArray(data.puts) ? data.puts : []
      const imp_underlying = typeof data.imp_underlying === "number" ? data.imp_underlying : 200

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
      if (sortedStrikes.length === 0) {
        this.generar_cadena_mock(this.instrumento_seleccionado)
        return
      }

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
          is_call_itm: strike < imp_underlying,
          is_put_itm: strike > imp_underlying,
          call_bid: call && call.bid !== undefined ? call.bid : "-",
          call_ask: call && call.ask !== undefined ? call.ask : "-",
          call_last: call && (call.last !== undefined ? call.last : call.price) || "-",
          call_vol: call && call.volume !== undefined ? call.volume : Math.floor(Math.random() * 500 + 20),
          call_contract: call,

          put_bid: put && put.bid !== undefined ? put.bid : "-",
          put_ask: put && put.ask !== undefined ? put.ask : "-",
          put_last: put && (put.last !== undefined ? put.last : put.price) || "-",
          put_vol: put && put.volume !== undefined ? put.volume : Math.floor(Math.random() * 500 + 20),
          put_contract: put
        }
      })
    },
    generar_cadena_mock(item) {
      // Generador de contingencia para pruebas de la GUI si IBKR no está conectado
      const today = new Date()
      const d1 = new Date(today.getTime() + 14 * 86400000).toISOString().substring(0, 10)
      const d2 = new Date(today.getTime() + 35 * 86400000).toISOString().substring(0, 10)
      const d3 = new Date(today.getTime() + 70 * 86400000).toISOString().substring(0, 10)
      const d4 = new Date(today.getTime() + 150 * 86400000).toISOString().substring(0, 10)

      this.expiraciones_disponibles = [
        { label: `${d1} (${this.formatear_expiracion(d1)})`, value: d1 },
        { label: `${d2} (${this.formatear_expiracion(d2)})`, value: d2 },
        { label: `${d3} (${this.formatear_expiracion(d3)})`, value: d3 },
        { label: `${d4} (${this.formatear_expiracion(d4)})`, value: d4 }
      ]
      if (!this.expiracion_seleccionada) {
        this.expiracion_seleccionada = d2
      }

      // Base de strike de referencia según activo
      let basePrice = 220
      if (item && item.symbol === "SPY") basePrice = 580
      else if (item && item.symbol === "QQQ") basePrice = 490
      else if (item && item.symbol === "NVDA") basePrice = 140
      else if (item && item.symbol === "TSLA") basePrice = 250
      else if (item && item.symbol === "SPX") basePrice = 5850

      const step = basePrice > 1000 ? 25 : (basePrice > 200 ? 5 : 2.5)
      const numStrikes = this.num_strikes_seleccionado || 20
      const half = Math.floor(numStrikes / 2)

      const rows = []
      for (let i = -half; i <= half; i++) {
        const strike = Number((basePrice + i * step).toFixed(2))
        const diff = strike - basePrice
        
        // Simular precios realistas Call y Put
        const callBid = Math.max(0.1, Number((Math.max(0, -diff) + 4.5 - diff * 0.15).toFixed(2)))
        const callAsk = Number((callBid + 0.15).toFixed(2))
        const putBid = Math.max(0.1, Number((Math.max(0, diff) + 4.5 + diff * 0.15).toFixed(2)))
        const putAsk = Number((putBid + 0.15).toFixed(2))

        rows.push({
          strike: strike,
          is_call_itm: strike < basePrice,
          is_put_itm: strike > basePrice,
          call_bid: callBid,
          call_ask: callAsk,
          call_last: Number(((callBid + callAsk) / 2).toFixed(2)),
          call_vol: Math.floor(Math.random() * 800 + 50),
          put_bid: putBid,
          put_ask: putAsk,
          put_last: Number(((putBid + putAsk) / 2).toFixed(2)),
          put_vol: Math.floor(Math.random() * 800 + 50)
        })
      }
      this.chain_rows = rows
    },
    formatear_precio(val) {
      if (val === null || val === undefined || val === "-") return "-"
      const num = Number(val)
      return isNaN(num) ? val : num.toFixed(2)
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
    formatear_expiracion(raw) {
      if (!raw) return ""
      const str = String(raw).trim()
      const matchYMD = str.match(/^(\d{4})[-/]?(\d{2})[-/]?(\d{2})$/)
      if (matchYMD) {
        const mesesNum = ["", "Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        const m = parseInt(matchYMD[2], 10)
        return `${matchYMD[3]} ${mesesNum[m] || matchYMD[2]} ${matchYMD[1]}`
      }
      return str
    },
    esta_contrato_seleccionado(strike, tipo) {
      const sym = this.instrumento_seleccionado ? this.instrumento_seleccionado.symbol : ''
      const exp = this.expiracion_seleccionada
      const cod = this.formatear_cod_opcion_osi(sym, exp, tipo, strike)
      return this.contratos_seleccionados_temporal.some(c => c.cod_symbol === cod)
    },
    toggle_seleccion_contrato(row, tipo) {
      const sym = this.instrumento_seleccionado ? this.instrumento_seleccionado.symbol : ''
      const exp = this.expiracion_seleccionada
      const strike = row.strike
      const cod = this.formatear_cod_opcion_osi(sym, exp, tipo, strike)

      const index = this.contratos_seleccionados_temporal.findIndex(c => c.cod_symbol === cod)
      if (index >= 0) {
        // Deseleccionar
        this.contratos_seleccionados_temporal.splice(index, 1)
      } else {
        // Seleccionar
        const bid = tipo === 'CALL' ? row.call_bid : row.put_bid
        const ask = tipo === 'CALL' ? row.call_ask : row.put_ask
        const last = tipo === 'CALL' ? row.call_last : row.put_last
        const vol = tipo === 'CALL' ? row.call_vol : row.put_vol

        this.contratos_seleccionados_temporal.push({
          cod_symbol: cod,
          symbol_subyacente: sym,
          nombre_subyacente: this.instrumento_seleccionado ? this.instrumento_seleccionado.name : sym,
          tipo: tipo.toUpperCase(),
          strike: Number(strike),
          fch_vencimiento: exp,
          expiracion_corta: this.formatear_expiracion(exp),
          dias_expiracion: this.calcular_dias_expiracion_fecha(exp),
          bid: Number(bid) || 0,
          ask: Number(ask) || 0,
          last: Number(last) || 0,
          volumen: vol || 0,
          is_itm: tipo === 'CALL' ? row.is_call_itm : row.is_put_itm,
          cantidad: 1,
          posicion: 'LONG' // LONG (compra) | SHORT (venta) para futura simulación
        })
      }
    },
    calcular_dias_expiracion_fecha(fch) {
      if (!fch) return null
      if (typeof fch === 'string' && fch.length === 8 && !fch.includes('-')) {
        fch = `${fch.substring(0, 4)}-${fch.substring(4, 6)}-${fch.substring(6, 8)}`
      }
      const expDate = moment(fch, ["YYYY-MM-DD", "YYYYMMDD", "DD-MMM-YYYY", "YYYY/MM/DD"])
      if (!expDate.isValid()) return null
      return expDate.startOf('day').diff(moment().startOf('day'), 'days')
    },
    formatear_dias_expiracion(item) {
      const dias = item.dias_expiracion !== undefined && item.dias_expiracion !== null
        ? item.dias_expiracion
        : this.calcular_dias_expiracion_fecha(item.fch_vencimiento)
      if (dias === null || dias === undefined) return ""
      if (dias === 0) return "0d (hoy)"
      return `${dias}d`
    },
    remover_contrato_temporal(cod_symbol) {
      this.contratos_seleccionados_temporal = this.contratos_seleccionados_temporal.filter(
        c => c.cod_symbol !== cod_symbol
      )
    },
    confirmar_seleccion_final() {
      this.$emit("confirmar", {
        instrumento: this.instrumento_seleccionado,
        contratos: [...this.contratos_seleccionados_temporal]
      })
      this.open = false
    }
  }
}
</script>

<style scoped>
.asistente-card {
  border-radius: 12px;
}
.instrumento-item {
  transition: background-color 0.15s ease;
}
.instrumento-item:hover {
  background-color: #f1f5f9;
}
</style>
