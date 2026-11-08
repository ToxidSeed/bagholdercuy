<template>
  <div class="panel-estrategia-opciones q-pa-sm">

    <!-- TOOLBAR PRINCIPAL -->
    <q-toolbar class="bg-white rounded-borders shadow-1 q-mb-xs q-py-none" style="min-height: 40px;">
      <q-avatar icon="alt_route" color="blue-10" text-color="white" size="26px" class="q-mr-xs" />
      <q-toolbar-title class="text-subtitle1 text-weight-bold text-dark">
        Simulación · Estrategias de Opciones
      </q-toolbar-title>

      <q-space />

      <!-- Botón principal "Seleccionar Instrumento" -->
      <q-btn
        unelevated
        dense
        color="blue-10"
        icon="search"
        label="Seleccionar Instrumento"
        class="text-weight-bold q-px-sm"
        size="sm"
        @click="abrir_asistente_nuevo_instrumento"
      >
        <q-tooltip>Abrir asistente para seleccionar Acción, ETF o Índice</q-tooltip>
      </q-btn>
    </q-toolbar>

    <!-- ======================================================== -->
    <!-- ESTADO VACÍO INICIAL (SI NO HAY INSTRUMENTO SELECCIONADO)-->
    <!-- ======================================================== -->
    <div v-if="!instrumento" class="text-center q-pa-xl bg-white rounded-borders shadow-1">
      <q-avatar size="80px" color="blue-1" text-color="blue-10" class="q-mb-md">
        <q-icon name="alt_route" size="48px" />
      </q-avatar>
      <div class="text-h5 text-weight-bold text-blue-10 q-mb-xs">
        Comience seleccionando un Instrumento Financiero
      </div>
      <div class="text-body2 text-grey-7 q-mb-lg" style="max-width: 620px; margin-left: auto; margin-right: auto;">
        Elija una <strong>Acción, ETF o Índice</strong> para modelar y comparar múltiples <strong>Grupos de Estrategia</strong> (Grupo 1: Estrategia 1, Grupo 2: Estrategia 2, etc.) con vista resumida y expandida de contratos.
      </div>
      <q-btn
        unelevated
        size="md"
        color="blue-10"
        icon="add_circle"
        label="Seleccionar Instrumento"
        class="q-px-lg text-weight-bold"
        @click="abrir_asistente_nuevo_instrumento"
      />
    </div>

    <!-- ======================================================== -->
    <!-- CONTENIDO PRINCIPAL (CUANDO HAY INSTRUMENTO)             -->
    <!-- ======================================================== -->
    <div v-else>

      <!-- SECCIÓN 1: INSTRUMENTO FINANCIERO Y VALORES DE COTIZACIÓN (COMPACTA) -->
      <q-card flat bordered class="instrumento-card-compact bg-white shadow-1 q-mb-xs q-pa-xs">
        <div class="row items-center justify-between no-wrap-md q-col-gutter-xs">
          
          <!-- Lado Izquierdo: Ticker, Tipo y Nombre -->
          <div class="col-auto row items-center q-gutter-xs no-wrap q-pl-xs">
            <q-avatar size="28px" color="blue-grey-10" text-color="white" class="text-weight-bold">
              {{ instrumento.symbol.substring(0, 2) }}
            </q-avatar>
            <span class="text-subtitle1 text-weight-bolder text-dark">{{ instrumento.symbol }}</span>
            <q-badge color="grey-3" text-color="grey-9" class="text-caption text-weight-bold border-grey">
              {{ instrumento.asset_type || 'STOCK' }}
            </q-badge>
            <span v-if="instrumento.name" class="text-caption text-grey-8 ellipsis gt-xs" style="max-width: 180px;">
              {{ instrumento.name }}
            </span>
            <q-btn
              flat
              dense
              round
              size="sm"
              color="grey-7"
              icon="swap_horiz"
              @click="abrir_asistente_nuevo_instrumento"
            >
              <q-tooltip>Cambiar instrumento financiero</q-tooltip>
            </q-btn>
          </div>

          <!-- Centro: Métricas de cotización -->
          <div class="col-auto row items-center q-gutter-sm no-wrap-sm text-center">
            
            <!-- 1. Cierre Anterior -->
            <div class="metric-pill">
              <span class="text-caption text-grey-6 q-mr-xs">Cierre Ant:</span>
              <span class="text-body2 text-weight-bolder text-grey-9">{{ formatear_cotizacion(cotizacion.imp_cierre_anterior) }}</span>
            </div>

            <q-separator vertical class="gt-xs" />

            <!-- 2. Apertura -->
            <div class="metric-pill">
              <span class="text-caption text-grey-6 q-mr-xs">Apertura:</span>
              <span class="text-body2 text-weight-bolder text-grey-9">{{ formatear_cotizacion(cotizacion.imp_apertura) }}</span>
            </div>

            <q-separator vertical class="gt-xs" />

            <!-- 3. Máximo -->
            <div class="metric-pill">
              <span class="text-caption text-grey-6 q-mr-xs">Máx:</span>
              <span class="text-body2 text-weight-bolder text-grey-9">{{ formatear_cotizacion(cotizacion.imp_maximo) }}</span>
            </div>

            <q-separator vertical class="gt-xs" />

            <!-- 4. Mínimo -->
            <div class="metric-pill">
              <span class="text-caption text-grey-6 q-mr-xs">Mín:</span>
              <span class="text-body2 text-weight-bolder text-grey-9">{{ formatear_cotizacion(cotizacion.imp_minimo) }}</span>
            </div>

            <q-separator vertical class="gt-xs" />

            <!-- 5. Cierre o Último Valor -->
            <div class="metric-pill bg-grey-2 q-px-sm q-py-xs rounded-borders row items-center border-grey">
              <span class="text-caption text-grey-7 text-weight-bold q-mr-xs">Último:</span>
              <span class="text-subtitle2 text-weight-bolder text-dark q-mr-xs">{{ formatear_cotizacion(cotizacion.imp_cierre) }}</span>
              <q-badge
                v-if="cotizacion.imp_variacion !== null"
                :color="cotizacion.imp_variacion >= 0 ? 'positive' : 'negative'"
                dense
                text-color="white"
                class="text-caption text-weight-bold"
              >
                <q-icon :name="cotizacion.imp_variacion >= 0 ? 'arrow_drop_up' : 'arrow_drop_down'" size="14px" />
                <span>{{ cotizacion.imp_variacion >= 0 ? '+' : '' }}{{ formatear_numero(cotizacion.imp_variacion) }}</span>
                <span v-if="cotizacion.pct_variacion !== null" class="q-ml-xs">({{ cotizacion.pct_variacion >= 0 ? '+' : '' }}{{ formatear_numero(cotizacion.pct_variacion) }}%)</span>
              </q-badge>
            </div>

          </div>

          <!-- Lado Derecho: Refrescar cotización -->
          <div class="col-auto row items-center q-pr-xs">
            <q-btn
              flat
              dense
              round
              color="grey-7"
              icon="refresh"
              size="sm"
              :loading="cargando_cotizacion"
              @click="cargar_cotizacion(instrumento.symbol)"
            >
              <q-tooltip>Actualizar cotización</q-tooltip>
            </q-btn>
          </div>

        </div>
      </q-card>

      <!-- ======================================================== -->
      <!-- SECCIÓN 2: BARRA DE CONTROL GLOBAL DE GRUPOS             -->
      <!-- ======================================================== -->
      <div class="row items-center justify-between q-my-xs q-px-xs">
        <div class="row items-center q-gutter-xs">
          <q-icon name="view_week" color="grey-8" size="20px" />
          <span class="text-subtitle1 text-weight-bold text-dark">
            Grupos de Estrategia
          </span>
          <q-badge color="grey-3" text-color="grey-9" class="text-caption text-weight-bold q-ml-xs border-grey">
            {{ estrategias.length }} {{ estrategias.length === 1 ? 'grupo' : 'grupos' }}
          </q-badge>
        </div>

        <div class="row items-center q-gutter-xs">
          <!-- Botón Guardar Estrategia Global -->
          <q-btn
            outline
            dense
            color="grey-8"
            icon="save"
            label="Guardar Estrategia"
            class="q-px-sm text-weight-medium bg-white"
            size="sm"
            :loading="guardandoEstrategia"
            :disable="estrategias.length === 0 || guardandoEstrategia"
            @click="abrir_dialogo_guardar_estrategia()"
          >
            <q-tooltip>Guardar el estado actual de la estrategia (todos los grupos)</q-tooltip>
          </q-btn>

          <!-- Botón Ver Estrategias Guardadas -->
          <q-btn
            outline
            dense
            color="grey-8"
            icon="bookmark"
            label="Estrategias Guardadas"
            size="sm"
            class="q-px-sm text-weight-medium bg-white"
            @click="dialogoEstrategiasGuardadasOpen = true"
          >
            <q-badge
              v-if="estrategias_guardadas.length > 0"
              color="blue-grey-9"
              text-color="white"
              floating
              rounded
            >
              {{ estrategias_guardadas.length }}
            </q-badge>
            <q-tooltip>Ver y gestionar estrategias guardadas</q-tooltip>
          </q-btn>

          <!-- Botón Añadir Nuevo Grupo de Estrategia -->
          <q-btn
            unelevated
            color="blue-10"
            icon="add_circle"
            label="Añadir Estrategia"
            class="text-weight-bold"
            size="sm"
            @click="agregar_nueva_estrategia"
          >
            <q-tooltip>Crear un nuevo grupo de estrategia en esta pantalla</q-tooltip>
          </q-btn>

          <!-- Toggle Expandir / Colapsar todos los grupos -->
          <q-btn
            flat
            dense
            color="grey-7"
            :icon="todos_los_grupos_expandidos ? 'unfold_less' : 'unfold_more'"
            :label="todos_los_grupos_expandidos ? 'Colapsar Grupos' : 'Expandir Grupos'"
            size="sm"
            class="q-px-xs text-weight-medium"
            @click="toggle_expandir_todos_grupos"
          />
        </div>
      </div>

      <!-- ======================================================== -->
      <!-- SECCIÓN 3: LISTA DE GRUPOS DE ESTRATEGIAS (GRUPO 1, 2...)-->
      <!-- ======================================================== -->
      <div class="q-gutter-y-sm">
        <q-card
          v-for="(estrategia, gIdx) in estrategias"
          :key="estrategia.id"
          flat
          bordered
          class="bg-white shadow-1 grupo-estrategia-card"
        >
          <!-- HEADER DEL GRUPO DE ESTRATEGIA -->
          <div class="grupo-header q-pa-sm bg-grey-1 row items-center justify-between no-wrap-md">
            
            <!-- Izquierda: Identificador del Grupo, Días a Expiración y Resumen Colapsado de Patas -->
            <div class="col-12 col-md row items-center q-gutter-xs no-wrap-sm ellipsis">
              <!-- Badge Grupo X -->
              <q-badge color="grey-3" text-color="grey-9" class="text-caption text-weight-bold q-px-sm q-py-xs border-grey">
                Grupo {{ gIdx + 1 }}
              </q-badge>

              <!-- Nombre editable de la Estrategia -->
              <span
                class="text-caption text-weight-bold text-dark cursor-pointer q-mx-xs hover-underline ellipsis"
                style="max-width: 220px;"
                @click="editar_nombre_estrategia(estrategia)"
              >
                {{ estrategia.nombre || ('Estrategia ' + (gIdx + 1)) }}
                <q-icon name="edit" size="11px" class="text-grey-5 q-ml-xs" />
                <q-tooltip>Click para renombrar estrategia</q-tooltip>
              </span>

              <!-- DÍAS PARA LA EXPIRACIÓN MÁS PRÓXIMA (DTE) -->
              <div
                v-if="calcular_dias_expiracion_minima(estrategia)"
                class="badge-dias-exp-min row items-center no-wrap text-caption text-weight-bold cursor-pointer"
                :class="calcular_dias_expiracion_minima(estrategia).badgeClass"
              >
                <q-icon name="schedule" size="13px" class="q-mr-xs" />
                <span>{{ calcular_dias_expiracion_minima(estrategia).textoCorto }}</span>
                <q-tooltip>{{ calcular_dias_expiracion_minima(estrategia).tooltip }}</q-tooltip>
              </div>

              <!-- FÓRMULA DE LAS PATAS DE LA ESTRATEGIA CUANDO ESTÁ COLAPSADA -->
              <div
                v-if="!estrategia.expandida"
                class="resumen-colapsado-badge row items-center no-wrap q-ml-xs q-px-sm q-py-xs rounded-borders text-caption text-weight-bolder font-mono cursor-pointer"
                @click="estrategia.expandida = true"
              >
                <q-icon name="notes" size="14px" class="q-mr-xs text-grey-7" />
                <span class="ellipsis" style="max-width: 580px;">
                  {{ resumen_patas_estrategia(estrategia) }}
                </span>
                <q-tooltip>Click para expandir | {{ resumen_patas_estrategia(estrategia) }}</q-tooltip>
              </div>
            </div>

            <!-- Derecha: Métricas Financieras (Flujo + Mark + PnL alineados en columna) y Controles -->
            <div class="col-12 col-md-auto row items-center justify-end q-gutter-xs q-mt-xs q-mt-md-none">
              
              <!-- BLOQUE FIJO DE PRECIOS Y RENDIMIENTO (ANTES DE VISTA CARDS) -->
              <div
                v-if="!estrategia.expandida"
                class="row items-center no-wrap q-gutter-x-xs q-mr-sm"
              >
                <!-- 1. BADGE VISUAL DE FLUJO (PREMIUM: ENTRADA / SALIDA A SIMPLE VISTA) -->
                <div
                  v-if="resumen_flujo_estrategia(estrategia)"
                  :class="resumen_flujo_estrategia(estrategia).badgeClass"
                  class="text-caption text-weight-bolder q-px-sm q-py-xs font-mono row items-center no-wrap"
                >
                  <q-icon :name="resumen_flujo_estrategia(estrategia).icon" size="13px" class="q-mr-xs" />
                  <span>{{ resumen_flujo_estrategia(estrategia).texto }}</span>
                  <q-tooltip>{{ resumen_flujo_estrategia(estrategia).tooltip }}</q-tooltip>
                </div>

                <!-- 2. CÁPSULA UNIFICADA: MARK + P&L (OPCIÓN D) -->
                <div
                  v-if="calcular_valor_actual_estrategia(estrategia) && calcular_pnl_estrategia(estrategia)"
                  class="capsula-mark-pnl row items-center no-wrap font-mono shadow-1 rounded-borders text-caption"
                  :class="calcular_pnl_estrategia(estrategia).capsulaClass"
                >
                  <!-- Lado izquierdo: Mark (Precio actual de mercado) -->
                  <div class="capsula-seccion-mark row items-center q-px-sm q-py-xs">
                    <q-icon name="show_chart" size="13px" class="q-mr-xs text-grey-5" />
                    <span>{{ calcular_valor_actual_estrategia(estrategia).texto }}</span>
                  </div>

                  <!-- Divisor sutil -->
                  <div class="capsula-divisor"></div>

                  <!-- Lado derecho: P&L (Ganando / Perdiendo) -->
                  <div class="capsula-seccion-pnl row items-center q-px-sm q-py-xs text-weight-bolder">
                    <span>{{ calcular_pnl_estrategia(estrategia).texto }}</span>
                  </div>

                  <q-tooltip>
                    <div>{{ calcular_valor_actual_estrategia(estrategia).tooltip }}</div>
                    <div class="text-weight-bold q-mt-xs">{{ calcular_pnl_estrategia(estrategia).tooltip }}</div>
                  </q-tooltip>
                </div>
              </div>

              <!-- Separador vertical discreto entre métricas de precio y controles -->
              <q-separator v-if="!estrategia.expandida" vertical class="q-mr-xs gt-xs" style="height: 20px;" />

              <!-- TOGGLE VERSIÓN RESUMIDA VS EXPANDIDA DE LAS CARDS -->
              <div class="row items-center q-mr-xs">
                <span class="text-caption text-grey-7 text-weight-medium q-mr-xs gt-xs">Vista:</span>
                <q-btn-toggle
                  v-model="estrategia.vista_cards"
                  dense
                  unelevated
                  toggle-color="grey-9"
                  toggle-text-color="white"
                  color="grey-2"
                  text-color="grey-7"
                  size="xs"
                  class="text-weight-bold"
                  :options="[
                    { label: 'Resumida', value: 'resumida', icon: 'view_agenda' },
                    { label: 'Expandida', value: 'expandida', icon: 'dashboard' }
                  ]"
                >
                  <q-tooltip>Alternar entre versión resumida y versión expandida de las cards</q-tooltip>
                </q-btn-toggle>
              </div>

              <!-- Botón Añadir / Gestionar Patas -->
              <q-btn
                unelevated
                color="blue-10"
                icon="playlist_add"
                label="Añadir Patas"
                class="text-weight-bold"
                size="sm"
                @click="abrir_asistente_para_estrategia(estrategia)"
              >
                <q-tooltip>Abrir asistente para agregar o modificar contratos a esta estrategia</q-tooltip>
              </q-btn>

              <q-separator vertical class="q-mx-xs gt-xs" style="height: 18px;" />

              <!-- Botón Invertir Posiciones Long ⇄ Short -->
              <q-btn
                flat
                dense
                round
                color="grey-7"
                icon="sync_alt"
                size="sm"
                :disable="estrategia.contratos.length === 0"
                @click="invertir_posiciones(estrategia)"
              >
                <q-tooltip>Invertir posiciones (Long a Short y Short a Long) en todas las patas</q-tooltip>
              </q-btn>

              <!-- Botón Duplicar Estrategia -->
              <q-btn
                flat
                dense
                round
                color="grey-7"
                icon="content_copy"
                size="sm"
                @click="duplicar_estrategia(estrategia)"
              >
                <q-tooltip>Duplicar esta estrategia en un nuevo grupo</q-tooltip>
              </q-btn>

              <!-- Botón Eliminar Grupo de Estrategia -->
              <q-btn
                v-if="estrategias.length > 1"
                flat
                dense
                round
                color="grey-6"
                icon="delete_outline"
                size="sm"
                class="hover-text-negative"
                @click="eliminar_estrategia(estrategia.id)"
              >
                <q-tooltip>Eliminar este grupo de estrategia</q-tooltip>
              </q-btn>

              <!-- Botón Colapsar / Expandir Grupo -->
              <q-btn
                flat
                dense
                round
                color="grey-7"
                :icon="estrategia.expandida ? 'expand_less' : 'expand_more'"
                size="sm"
                @click="estrategia.expandida = !estrategia.expandida"
              >
                <q-tooltip>{{ estrategia.expandida ? 'Colapsar grupo' : 'Expandir grupo' }}</q-tooltip>
              </q-btn>

            </div>

          </div>

          <q-separator />

          <!-- CUERPO EXPANDIBLE DEL GRUPO DE ESTRATEGIA -->
          <div v-show="estrategia.expandida" class="q-pa-sm">

            <!-- SUB-SECCIÓN 1: KPIS RESUMEN DE LA ESTRATEGIA -->
            <div v-if="estrategia.contratos.length > 0" class="row q-col-gutter-xs q-mb-sm">
              
              <!-- 1. Flujo / Costo Neto -->
              <div class="col-12 col-sm-6 col-md-3">
                <q-card flat bordered class="q-pa-xs bg-white text-center">
                  <div class="text-caption text-grey-7">Prima Neta (Débito / Crédito)</div>
                  <div class="text-subtitle2 text-weight-bolder row items-center justify-center q-gutter-x-xs">
                    <span :class="calcular_metricas(estrategia).debito_neto >= 0 ? 'text-red-9' : 'text-positive'">
                      {{ calcular_metricas(estrategia).debito_neto >= 0 ? '-$' : '+$' }}{{ Math.abs(calcular_metricas(estrategia).debito_neto).toFixed(2) }}
                    </span>
                    <span
                      class="text-caption text-weight-bold q-px-xs rounded-borders"
                      :class="calcular_metricas(estrategia).debito_neto >= 0 ? 'pill-debito' : 'pill-credito'"
                    >
                      {{ calcular_metricas(estrategia).debito_neto >= 0 ? 'DÉBITO' : 'CRÉDITO' }}
                    </span>
                  </div>
                </q-card>
              </div>

              <!-- 2. Beneficio Máximo -->
              <div class="col-12 col-sm-6 col-md-3">
                <q-card flat bordered class="q-pa-xs bg-white text-center">
                  <div class="text-caption text-grey-7">Beneficio Máximo (Max Profit)</div>
                  <div class="text-subtitle2 text-weight-bolder text-positive">
                    {{ calcular_metricas(estrategia).beneficio_maximo }}
                  </div>
                </q-card>
              </div>

              <!-- 3. Pérdida Máxima -->
              <div class="col-12 col-sm-6 col-md-3">
                <q-card flat bordered class="q-pa-xs bg-white text-center">
                  <div class="text-caption text-grey-7">Pérdida Máxima (Max Loss)</div>
                  <div class="text-subtitle2 text-weight-bolder text-negative">
                    {{ calcular_metricas(estrategia).perdida_maxima }}
                  </div>
                </q-card>
              </div>

              <!-- 4. Puntos de Equilibrio -->
              <div class="col-12 col-sm-6 col-md-3">
                <q-card flat bordered class="q-pa-xs bg-white text-center">
                  <div class="text-caption text-grey-7">Punto(s) de Equilibrio (BE)</div>
                  <div class="text-subtitle2 text-weight-bolder text-dark">
                    {{ calcular_metricas(estrategia).breakevens }}
                  </div>
                </q-card>
              </div>

            </div>

            <!-- SUB-SECCIÓN 2: CARDS DE PATAS (LEGS) -->
            <div>
              <!-- Cabecera de Patas con indicador de modo -->
              <div class="row items-center justify-between q-mb-xs">
                <div class="row items-center">
                  <span class="text-caption text-weight-bold text-grey-8">
                    Patas del {{ estrategia.nombre }} ({{ estrategia.contratos.length }} contratos)
                  </span>
                  <q-badge
                    color="grey-3"
                    text-color="grey-9"
                    class="q-ml-xs text-caption text-weight-bold border-grey"
                  >
                    Modo {{ estrategia.vista_cards === 'resumida' ? 'Resumido' : 'Expandido' }}
                  </q-badge>
                </div>

                <div class="text-caption text-grey-6 gt-xs">
                  LONG en azul · SHORT en rojo · Puede alternar entre vista resumida o expandida
                </div>
              </div>

              <!-- Estado si este grupo aún no tiene contratos -->
              <div
                v-if="estrategia.contratos.length === 0"
                class="text-center q-pa-lg bg-white rounded-borders border-dashed"
              >
                <q-icon name="tune" size="36px" class="text-grey-4 q-mb-xs" />
                <div class="text-caption text-weight-bold text-grey-8">
                  No hay contratos asignados a {{ estrategia.nombre }}
                </div>
                <div class="text-caption text-grey-6 q-mb-sm">
                  Abra la cadena de opciones para agregar contratos a esta estrategia.
                </div>
                <q-btn
                  unelevated
                  color="blue-10"
                  icon="playlist_add"
                  label="Abrir Cadena de Opciones"
                  size="sm"
                  class="text-weight-bold"
                  @click="abrir_asistente_para_estrategia(estrategia)"
                />
              </div>

              <!-- GRID DE CARDS: VERSIÓN RESUMIDA O EXPANDIDA SEGÚN CONFIGURACIÓN -->
              <div v-else class="row q-col-gutter-xs">
                
                <div
                  v-for="(contrato, idx) in estrategia.contratos"
                  :key="contrato.cod_symbol"
                  class="col-12 col-sm-6 col-md-4 col-lg-3"
                >

                  <!-- ============================================== -->
                  <!-- OPCIÓN A: VERSIÓN RESUMIDA (COMPACTA)          -->
                  <!-- ============================================== -->
                  <q-card
                    v-if="estrategia.vista_cards === 'resumida' && !contrato.forzar_expandida"
                    class="pata-card-resumida shadow-1 q-pa-xs column justify-between"
                    :class="contrato.tipo === 'CALL' ? 'pata-borde-call' : 'pata-borde-put'"
                  >
                    <!-- Fila 1: Badges Tipo, Posición, Strike, Vencimiento, ITM y Acciones -->
                    <div class="row items-center justify-between no-wrap q-gutter-x-xs q-mb-xs">
                      <div class="row items-center no-wrap q-gutter-x-xs">
                        <span
                          class="text-weight-bolder text-caption q-px-xs rounded-borders"
                          :class="contrato.tipo === 'CALL' ? 'pill-call' : 'pill-put'"
                        >
                          {{ contrato.tipo }}
                        </span>
                        <!-- BADGE LONG / SHORT -->
                        <span
                          class="text-weight-bolder text-caption q-px-xs rounded-borders"
                          :class="contrato.posicion === 'LONG' ? 'pill-long' : 'pill-short'"
                        >
                          {{ contrato.posicion }}
                        </span>
                        <span class="text-caption text-weight-bolder text-dark">
                          ${{ Number(contrato.strike).toFixed(2) }}
                        </span>
                        <span class="text-caption text-grey-8 text-weight-medium">
                          {{ contrato.expiracion_corta || contrato.fch_vencimiento }}
                        </span>
                        <span
                          class="text-caption q-px-xs rounded-borders text-weight-medium"
                          :class="contrato.is_itm ? 'pill-itm' : 'pill-otm'"
                        >
                          {{ contrato.is_itm ? 'ITM' : 'OTM' }} · {{ formatear_dias_expiracion(contrato) }}
                        </span>
                      </div>

                      <div class="row items-center no-wrap">
                        <!-- Botón para expandir solo esta card -->
                        <q-btn
                          flat
                          round
                          dense
                          icon="open_in_full"
                          size="xs"
                          color="grey-7"
                          @click="$set(contrato, 'forzar_expandida', true)"
                        >
                          <q-tooltip>Ver detalles expandidos</q-tooltip>
                        </q-btn>
                        <!-- Botón remover pata -->
                        <q-btn
                          flat
                          round
                          dense
                          icon="close"
                          size="xs"
                          color="grey-7"
                          @click="remover_pata(estrategia, contrato.cod_symbol)"
                        >
                          <q-tooltip>Quitar esta pata</q-tooltip>
                        </q-btn>
                      </div>
                    </div>

                    <!-- Fila 2: Selector LONG / SHORT, Cantidad y Flujo Estimado -->
                    <div class="row items-center justify-between no-wrap q-gutter-x-xs bg-grey-1 q-px-xs rounded-borders" style="min-height: 26px;">
                      <!-- Toggle LONG (Azul) / SHORT (Rojo) -->
                      <q-btn-toggle
                        v-model="contrato.posicion"
                        dense
                        unelevated
                        :toggle-color="contrato.posicion === 'LONG' ? 'blue-10' : 'red-9'"
                        toggle-text-color="white"
                        color="grey-3"
                        text-color="grey-8"
                        :options="[
                          { label: 'LONG', value: 'LONG' },
                          { label: 'SHORT', value: 'SHORT' }
                        ]"
                        size="xs"
                        class="text-weight-bold"
                      />

                      <!-- Cantidad -->
                      <div class="row items-center no-wrap">
                        <q-btn
                          flat
                          round
                          dense
                          size="xs"
                          icon="remove"
                          @click="decrementar_cantidad(contrato)"
                        />
                        <span class="text-caption text-weight-bold q-px-xs">{{ contrato.cantidad || 1 }}</span>
                        <q-btn
                          flat
                          round
                          dense
                          size="xs"
                          icon="add"
                          @click="incrementar_cantidad(contrato)"
                        />
                      </div>

                      <!-- Flujo Estimado (Azul si LONG / Rojo si SHORT) -->
                      <div
                        class="text-caption text-weight-bolder"
                        :class="contrato.posicion === 'LONG' ? 'text-blue-10' : 'text-red-9'"
                      >
                        {{ contrato.posicion === 'LONG' ? '-$' : '+$' }}{{ calcular_prima_total(contrato) }}
                      </div>
                    </div>
                  </q-card>

                  <!-- ============================================== -->
                  <!-- OPCIÓN B: VERSIÓN EXPANDIDA (DETALLADA)        -->
                  <!-- ============================================== -->
                  <q-card
                    v-else
                    class="pata-card shadow-1 full-height column justify-between"
                  >
                    <!-- Header de la Pata Expandida -->
                    <q-card-section
                      class="q-py-xs q-px-sm row items-center justify-between bg-grey-1"
                      style="border-bottom: 1px solid #edf2f7;"
                    >
                      <div class="row items-center no-wrap">
                        <q-icon
                          :name="contrato.tipo === 'CALL' ? 'call_made' : 'call_received'"
                          size="16px"
                          class="q-mr-xs text-grey-7"
                        />
                        <span
                          class="text-weight-bolder text-caption q-px-xs rounded-borders"
                          :class="contrato.tipo === 'CALL' ? 'pill-call' : 'pill-put'"
                        >
                          {{ contrato.tipo }}
                        </span>
                        <span
                          class="text-weight-bolder text-caption q-px-xs rounded-borders q-ml-xs"
                          :class="contrato.posicion === 'LONG' ? 'pill-long' : 'pill-short'"
                        >
                          {{ contrato.posicion }}
                        </span>
                        <span class="text-caption text-weight-bold text-grey-8 q-ml-xs">
                          Pata #{{ idx + 1 }}
                        </span>
                      </div>

                      <div class="row items-center no-wrap">
                        <!-- Botón para colapsar a resumida individualmente -->
                        <q-btn
                          v-if="contrato.forzar_expandida"
                          flat
                          round
                          dense
                          icon="close_fullscreen"
                          size="xs"
                          color="grey-7"
                          @click="$set(contrato, 'forzar_expandida', false)"
                        >
                          <q-tooltip>Colapsar a vista resumida</q-tooltip>
                        </q-btn>
                        <!-- Botón remover pata -->
                        <q-btn
                          flat
                          round
                          dense
                          icon="close"
                          size="xs"
                          color="grey-7"
                          @click="remover_pata(estrategia, contrato.cod_symbol)"
                        >
                          <q-tooltip>Quitar esta pata de la estrategia</q-tooltip>
                        </q-btn>
                      </div>
                    </q-card-section>

                    <!-- Contenido Detallado de la Pata -->
                    <q-card-section class="q-pa-sm">
                      <!-- Símbolo OSI y Estado ITM/OTM -->
                      <div class="row items-center justify-between q-mb-xs">
                        <div class="text-caption text-weight-bold font-mono text-grey-9 ellipsis" style="max-width: 170px;">
                          {{ contrato.cod_symbol }}
                        </div>
                        <span
                          class="text-caption text-weight-medium q-px-xs rounded-borders"
                          :class="contrato.is_itm ? 'pill-itm' : 'pill-otm'"
                        >
                          {{ contrato.is_itm ? 'ITM' : 'OTM' }}
                        </span>
                      </div>

                      <!-- Strike y Fecha de Vencimiento -->
                      <div class="row items-baseline justify-between q-my-xs">
                        <div>
                          <span class="text-caption text-grey-6 text-uppercase">Strike:</span>
                          <span class="text-h6 text-weight-bolder text-dark q-ml-xs">
                            ${{ Number(contrato.strike).toFixed(2) }}
                          </span>
                        </div>
                        <div class="text-caption text-grey-8 text-weight-bold">
                          {{ contrato.expiracion_corta || contrato.fch_vencimiento }}
                        </div>
                      </div>

                      <!-- Días para Expiración -->
                      <div
                        class="row items-center justify-between q-py-xs q-px-sm rounded-borders q-my-xs"
                        :class="'bg-' + obtener_badge_dias_bg(contrato)"
                      >
                        <div class="row items-center text-caption" :class="obtener_color_dias_expiracion(contrato)">
                          <q-icon name="schedule" size="14px" class="q-mr-xs" />
                          <span class="text-weight-medium">Días exp.:</span>
                        </div>
                        <div class="text-caption text-weight-bolder" :class="obtener_color_dias_expiracion(contrato)">
                          {{ formatear_dias_expiracion(contrato) }}
                        </div>
                      </div>

                      <q-separator class="q-my-xs" />

                      <!-- Grilla de Precios (Bid / Ask / Last) -->
                      <div class="row text-center q-col-gutter-xs q-mt-xs">
                        <div class="col-4">
                          <div class="text-caption text-grey-6">Bid</div>
                          <div class="text-weight-bold text-dark">${{ formatear_numero(contrato.bid) }}</div>
                        </div>
                        <div class="col-4">
                          <div class="text-caption text-grey-6">Ask</div>
                          <div class="text-weight-bold text-dark">${{ formatear_numero(contrato.ask) }}</div>
                        </div>
                        <div class="col-4">
                          <div class="text-caption text-grey-6">Last</div>
                          <div class="text-weight-bolder text-dark">${{ formatear_numero(contrato.last) }}</div>
                        </div>
                      </div>

                      <!-- Griegas (Delta, Theta) -->
                      <div class="row items-center justify-around bg-grey-2 q-py-xs rounded-borders q-mt-xs text-caption">
                        <span class="text-grey-7">Δ Delta: <strong class="text-dark">{{ calcular_delta(contrato) }}</strong></span>
                        <span class="text-grey-7">Θ Theta: <strong class="text-dark">{{ calcular_theta(contrato) }}</strong></span>
                      </div>
                    </q-card-section>

                    <!-- Footer de la Pata Expandida: Posición Long/Short, Cantidad y Prima -->
                    <q-card-section class="bg-grey-1 q-pa-sm rounded-borders-bottom">
                      <div class="row items-center justify-between q-gutter-xs">
                        
                        <!-- Posición Long / Short (AZUL / ROJO) -->
                        <div class="row items-center">
                          <q-btn-toggle
                            v-model="contrato.posicion"
                            dense
                            unelevated
                            :toggle-color="contrato.posicion === 'LONG' ? 'blue-10' : 'red-9'"
                            toggle-text-color="white"
                            color="grey-3"
                            text-color="grey-8"
                            :options="[
                              { label: 'LONG', value: 'LONG' },
                              { label: 'SHORT', value: 'SHORT' }
                            ]"
                            size="xs"
                            class="text-weight-bold"
                          />
                        </div>

                        <!-- Cantidad de contratos -->
                        <div class="row items-center q-gutter-xs">
                          <span class="text-caption text-grey-7">Cant:</span>
                          <q-btn
                            flat
                            round
                            dense
                            size="xs"
                            icon="remove"
                            @click="decrementar_cantidad(contrato)"
                          />
                          <span class="text-caption text-weight-bold">{{ contrato.cantidad || 1 }}</span>
                          <q-btn
                            flat
                            round
                            dense
                            size="xs"
                            icon="add"
                            @click="incrementar_cantidad(contrato)"
                          />
                        </div>
                      </div>

                      <!-- Prima Total Estimada de esta pata -->
                      <div class="row items-center justify-between q-mt-xs text-caption">
                        <span class="text-grey-6">Flujo estimado:</span>
                        <span class="text-weight-bolder" :class="contrato.posicion === 'LONG' ? 'text-blue-10' : 'text-red-9'">
                          {{ contrato.posicion === 'LONG' ? '-$' : '+$' }}{{ calcular_prima_total(contrato) }}
                        </span>
                      </div>
                    </q-card-section>

                  </q-card>

                </div>

              </div>
            </div>



          </div>
        </q-card>
      </div>

    </div>

    <!-- DIÁLOGO ASISTENTE DE SELECCIÓN DE INSTRUMENTO Y OPCIONES -->
    <WinAsistenteSeleccionOpciones
      v-model="asistenteOpen"
      :instrumento-inicial="asistenteInstrumentoInicial"
      :contratos-iniciales="asistenteContratosIniciales"
      :estrategias-guardadas="estrategias_guardadas"
      :cargando-estrategias-guardadas="cargandoEstrategiasGuardadas"
      @confirmar="on_confirmar_asistente"
      @cargar-estrategia-guardada="cargar_estrategia_guardada"
    />

    <!-- ======================================================== -->
    <!-- DIÁLOGO PARA GUARDAR ESTRATEGIA                          -->
    <!-- ======================================================== -->
    <q-dialog v-model="dialogoGuardarOpen" persistent>
      <q-card style="min-width: 520px; max-width: 660px; width: 92vw;" class="shadow-4">
        <!-- Cabecera del diálogo -->
        <q-toolbar class="bg-blue-grey-10 text-white q-py-xs">
          <q-avatar icon="save" color="blue-grey-8" text-color="white" size="32px" />
          <q-toolbar-title class="text-subtitle1 text-weight-bold">
            {{ idEstrategiaGuardadaEnEdicion ? 'Actualizar Estrategia Guardada' : 'Guardar Estrategia de Opciones' }}
          </q-toolbar-title>
          <q-btn flat round dense icon="close" v-close-popup />
        </q-toolbar>

        <q-card-section class="q-pt-md q-pb-xs">
          <!-- Campos de Entrada -->
          <div class="row q-col-gutter-sm items-center q-mb-sm">
            <div class="col-12 col-md-8">
              <q-input
                v-model="formularioGuardar.nombre"
                label="Nombre de la Estrategia *"
                outlined
                dense
                color="blue-10"
                autofocus
                placeholder="Ej: Estrategia SPY Multi-Grupo"
                :rules="[val => !!val && val.trim().length > 0 || 'El nombre es obligatorio']"
                @keydown.enter.prevent="confirmar_guardar_estrategia"
              >
                <template v-slot:prepend>
                  <q-icon name="label" color="blue-10" />
                </template>
              </q-input>
            </div>

            <div class="col-12 col-md-4">
              <q-input
                v-model="formularioGuardar.etiqueta"
                label="Etiqueta / Categoría"
                outlined
                dense
                color="blue-10"
                placeholder="Ej: Alcista, Spread, Demo..."
                @keydown.enter.prevent="confirmar_guardar_estrategia"
              >
                <template v-slot:prepend>
                  <q-icon name="sell" color="blue-10" />
                </template>
              </q-input>
            </div>
          </div>

          <!-- Resumen del Estado de la Estrategia (Todos los Grupos) -->
          <div class="q-pa-sm bg-grey-1 rounded-borders border-grey q-mb-sm">
            <div class="row items-center justify-between text-caption q-mb-xs">
              <div class="row items-center q-gutter-x-xs">
                <span class="text-weight-bolder text-blue-10">
                  {{ instrumento ? instrumento.symbol : 'N/A' }}
                </span>
                <span v-if="instrumento && instrumento.name" class="text-grey-7 gt-xs">
                  ({{ instrumento.name }})
                </span>
                <span class="text-grey-7">
                  · Último: {{ formatear_cotizacion(cotizacion.imp_cierre) }}
                </span>
              </div>
              <div class="row items-center q-gutter-x-xs">
                <q-badge color="grey-3" text-color="grey-9" class="text-weight-bold border-grey">
                  {{ estrategias.length }} {{ estrategias.length === 1 ? 'Grupo' : 'Grupos' }}
                </q-badge>
                <q-badge color="blue-grey-1" text-color="blue-grey-9" class="text-weight-bold border-grey">
                  {{ total_contratos_simulacion }} {{ total_contratos_simulacion === 1 ? 'Contrato' : 'Contratos' }}
                </q-badge>
              </div>
            </div>

            <q-separator class="q-my-xs" />

            <!-- Lista y detalle de cada grupo a guardar -->
            <div style="max-height: 200px; overflow-y: auto;" class="q-pr-xs">
              <div
                v-for="(grupo, idx) in estrategias"
                :key="grupo.id"
                class="q-py-xs"
                :class="{ 'border-bottom-light': idx < estrategias.length - 1 }"
              >
                <div class="row items-center justify-between text-caption">
                  <div class="row items-center q-gutter-x-xs">
                    <q-badge color="blue-grey-9" text-color="white" class="text-caption text-weight-bold">
                      G{{ idx + 1 }}
                    </q-badge>
                    <span class="text-weight-bold text-dark">{{ grupo.nombre || `Grupo ${idx + 1}` }}</span>
                    <span class="text-grey-6 text-caption">({{ (grupo.contratos || []).length }} patas)</span>
                  </div>
                  <div v-if="resumen_flujo_estrategia(grupo)" class="text-caption">
                    <span
                      class="text-weight-bold"
                      :class="resumen_flujo_estrategia(grupo).tipo === 'CREDITO' ? 'text-positive' : 'text-negative'"
                    >
                      {{ resumen_flujo_estrategia(grupo).texto }}
                    </span>
                  </div>
                </div>
                <div class="font-mono text-caption text-grey-8 q-ml-sm q-mt-xs text-weight-medium">
                  {{ resumen_patas_estrategia(grupo) || 'Sin contratos' }}
                </div>
              </div>
            </div>
          </div>

          <!-- Notas opcionales -->
          <q-input
            v-model="formularioGuardar.notas"
            label="Notas / Observaciones (Opcional)"
            outlined
            dense
            type="textarea"
            rows="2"
            color="blue-10"
            placeholder="Añada hipótesis, objetivo de ganancia, stop-loss o fecha estimada..."
          >
            <template v-slot:prepend>
              <q-icon name="edit_note" color="blue-10" />
            </template>
          </q-input>
        </q-card-section>

        <q-separator class="q-my-xs" />

        <q-card-actions align="right" class="q-px-md q-pb-sm">
          <q-btn flat label="Cancelar" color="grey-8" v-close-popup />
          <q-btn
            unelevated
            icon="save"
            :label="idEstrategiaGuardadaEnEdicion ? 'Confirmar y Actualizar' : 'Confirmar y Guardar'"
            color="blue-10"
            class="text-weight-bold q-px-md"
            :loading="guardandoEstrategia"
            :disable="guardandoEstrategia"
            @click="confirmar_guardar_estrategia"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- ======================================================== -->
    <!-- DIÁLOGO DE ESTRATEGIAS GUARDADAS                         -->
    <!-- ======================================================== -->
    <q-dialog v-model="dialogoEstrategiasGuardadasOpen">
      <q-card style="min-width: 650px; max-width: 850px; width: 92vw;" class="shadow-4">
        <q-toolbar class="bg-blue-grey-10 text-white q-py-xs">
          <q-avatar icon="bookmark" color="blue-grey-8" text-color="white" size="32px" />
          <q-toolbar-title class="text-subtitle1 text-weight-bold">
            Estrategias Guardadas
          </q-toolbar-title>
          <q-badge color="grey-3" text-color="grey-9" class="text-weight-bold q-mr-sm border-grey">
            {{ estrategias_guardadas.length }} {{ estrategias_guardadas.length === 1 ? 'guardada' : 'guardadas' }}
          </q-badge>
          <q-btn flat round dense icon="close" v-close-popup />
        </q-toolbar>

        <!-- Barra de búsqueda / filtro -->
        <div class="q-pa-sm bg-grey-1 row items-center justify-between">
          <q-input
            v-model="filtroEstrategiasGuardadas"
            dense
            outlined
            clearable
            placeholder="Buscar por símbolo, nombre, etiqueta o patas..."
            class="col-12 col-sm-8 bg-white"
            color="blue-10"
          >
            <template v-slot:prepend>
              <q-icon name="search" size="18px" color="grey-7" />
            </template>
          </q-input>

          <span class="text-caption text-grey-6 gt-xs">
            Persistido en la base de datos
          </span>
        </div>

        <q-separator />

        <!-- Lista de estrategias -->
        <q-card-section class="q-pa-none" style="max-height: 60vh; overflow-y: auto;">
          <div v-if="cargandoEstrategiasGuardadas" class="text-center q-pa-xl text-grey-7">
            <q-spinner color="blue-10" size="2em" />
            <div class="text-caption q-mt-sm">Cargando estrategias guardadas...</div>
          </div>

          <!-- Estado vacío -->
          <div
            v-else-if="estrategias_guardadas_filtradas.length === 0"
            class="text-center q-pa-xl text-grey-7"
          >
            <q-avatar size="54px" color="blue-1" text-color="blue-10" class="q-mb-sm">
              <q-icon name="bookmark_border" size="32px" />
            </q-avatar>
            <div class="text-subtitle2 text-weight-bold text-dark q-mb-xs">
              {{ estrategias_guardadas.length === 0 ? 'Aún no tiene estrategias guardadas' : 'No se encontraron estrategias con ese filtro' }}
            </div>
            <div class="text-caption text-grey-6" style="max-width: 420px; margin: 0 auto;">
              {{ estrategias_guardadas.length === 0 ? 'Para guardar una estrategia, configure los grupos en el simulador y haga clic en el botón "Guardar Estrategia".' : 'Intente buscar con otro término.' }}
            </div>
          </div>

          <!-- Items guardados -->
          <q-list v-else separator>
            <q-item
              v-for="guardada in estrategias_guardadas_filtradas"
              :key="guardada.id"
              class="q-py-sm hover-bg-grey-1"
            >
              <q-item-section avatar top>
                <q-avatar color="blue-10" text-color="white" size="36px" class="text-weight-bold">
                  {{ guardada.instrumento ? guardada.instrumento.symbol.substring(0, 3) : 'EST' }}
                </q-avatar>
              </q-item-section>

              <q-item-section top>
                <!-- Nombre, Ticker, Tipo y Fecha -->
                <div class="row items-center q-gutter-x-xs no-wrap q-mb-xs">
                  <span class="text-subtitle2 text-weight-bolder text-dark ellipsis">
                    {{ guardada.nombre }}
                  </span>
                  <q-badge color="grey-3" text-color="grey-9" class="text-caption text-weight-bold border-grey">
                    {{ guardada.instrumento ? guardada.instrumento.symbol : 'N/A' }}
                  </q-badge>
                  <q-badge v-if="guardada.tipo" color="blue-grey-1" text-color="blue-grey-9" class="text-caption text-weight-bold border-grey">
                    {{ guardada.tipo }}
                  </q-badge>
                  <q-badge color="grey-3" text-color="grey-9" class="text-caption border-grey">
                    {{ guardada.grupos ? guardada.grupos.length : 1 }} {{ (guardada.grupos ? guardada.grupos.length : 1) === 1 ? 'grupo' : 'grupos' }}
                  </q-badge>
                  <q-space />
                  <span class="text-caption text-grey-6">
                    <q-icon name="event" size="12px" class="q-mr-xs" />
                    {{ guardada.fecha_corta || guardada.fecha_guardado }}
                  </span>
                </div>

                <!-- Resumen de patas / fórmula -->
                <div class="font-mono text-caption text-weight-bold text-grey-9 bg-grey-2 q-px-xs q-py-xs rounded-borders q-mb-xs">
                  {{ guardada.resumen_patas }}
                </div>

                <!-- Métricas y flujo -->
                <div class="row items-center q-gutter-x-sm text-caption">
                  <span v-if="guardada.resumen_flujo" class="text-weight-bold text-dark">
                    Flujo: {{ guardada.resumen_flujo }}
                  </span>
                  <span v-if="guardada.metricas && guardada.metricas.breakevens" class="text-grey-7">
                    | BE: {{ guardada.metricas.breakevens }}
                  </span>
                  <span v-if="guardada.cotizacion_referencia" class="text-grey-7">
                    | Ref: ${{ formatear_numero(guardada.cotizacion_referencia) }}
                  </span>
                  <span class="text-weight-medium text-grey-7">
                    · {{ contar_total_contratos_guardada(guardada) }} patas
                  </span>
                </div>

                <!-- Notas si existen -->
                <div v-if="guardada.notas" class="text-caption text-grey-8 italic q-mt-xs bg-grey-2 q-px-xs rounded-borders">
                  <q-icon name="sticky_note_2" size="12px" class="q-mr-xs text-grey-6" />
                  {{ guardada.notas }}
                </div>
              </q-item-section>

              <!-- Acciones: Cargar y Eliminar -->
              <q-item-section side top class="q-pl-sm column justify-center q-gutter-y-xs">
                <q-btn
                  unelevated
                  color="blue-10"
                  icon="file_download"
                  label="Cargar"
                  size="sm"
                  class="text-weight-bold"
                  @click="cargar_estrategia_guardada(guardada)"
                >
                  <q-tooltip>Cargar el estado completo de esta estrategia en el simulador</q-tooltip>
                </q-btn>

                <q-btn
                  flat
                  dense
                  color="negative"
                  icon="delete_outline"
                  label="Eliminar"
                  size="xs"
                  class="q-px-xs"
                  @click="eliminar_estrategia_guardada(guardada.id)"
                >
                  <q-tooltip>Eliminar esta estrategia guardada</q-tooltip>
                </q-btn>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>

        <q-separator />

        <q-card-actions align="right" class="q-pa-sm">
          <q-btn flat label="Cerrar" color="grey-8" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

  </div>
</template>

<script>
import WinAsistenteSeleccionOpciones from "./WinAsistenteSeleccionOpciones.vue"
import Cotizacion from "@/api/cotizacion.js"
import VariacionSemanal from "@/api/variacion-semanal.js"
import SimulacionEstrategiaApi from "@/api/simulacion-estrategia.js"
import moment from "moment"
import _ from "lodash"

export default {
  name: "PanelEstrategiaOpciones",
  components: {
    WinAsistenteSeleccionOpciones
  },
  data() {
    return {
      asistenteOpen: false,
      asistenteInstrumentoInicial: null,
      asistenteContratosIniciales: [],
      asistenteEstrategiaId: null,

      // Modales de Guardar y Ver Estrategias Guardadas
      dialogoGuardarOpen: false,
      dialogoEstrategiasGuardadasOpen: false,
      filtroEstrategiasGuardadas: "",
      estrategias_guardadas: [],
      guardandoEstrategia: false,
      cargandoEstrategiasGuardadas: false,
      idEstrategiaGuardadaEnEdicion: null,
      formularioGuardar: {
        nombre: "",
        etiqueta: "ESTRATEGIA",
        notas: ""
      },

      // Instrumento financiero actualmente seleccionado
      instrumento: null,

      // Valores de cotización del instrumento
      cotizacion: {
        imp_cierre_anterior: null,
        imp_apertura: null,
        imp_maximo: null,
        imp_minimo: null,
        imp_cierre: null,
        imp_variacion: null,
        pct_variacion: null
      },
      cargando_cotizacion: false,
      timerCotizaciones: null,
      actualizandoCotizaciones: false,

      // LISTA DE GRUPOS DE ESTRATEGIAS (Grupo 1: Estrategia 1, Grupo 2: Estrategia 2, etc.)
      estrategias: []
    }
  },
  computed: {
    todos_los_grupos_expandidos() {
      if (this.estrategias.length === 0) return false
      return this.estrategias.every(e => e.expandida)
    },
    total_contratos_simulacion() {
      return (this.estrategias || []).reduce(
        (acc, e) => acc + (e.contratos ? e.contratos.length : 0),
        0
      )
    },
    estrategias_guardadas_filtradas() {
      if (!this.filtroEstrategiasGuardadas || this.filtroEstrategiasGuardadas.trim() === "") {
        return this.estrategias_guardadas
      }
      const q = this.filtroEstrategiasGuardadas.toLowerCase().trim()
      return this.estrategias_guardadas.filter(item => {
        const nom = (item.nombre || "").toLowerCase()
        const sym = (item.instrumento && item.instrumento.symbol ? item.instrumento.symbol : "").toLowerCase()
        const tipo = (item.tipo || "").toLowerCase()
        const notas = (item.notas || "").toLowerCase()
        const resumen = (item.resumen_patas || "").toLowerCase()
        return nom.includes(q) || sym.includes(q) || tipo.includes(q) || notas.includes(q) || resumen.includes(q)
      })
    }
  },
  created() {
    this.cargar_estrategias_guardadas()
    this.timerCotizaciones = setInterval(() => {
      this.actualizar_cotizaciones_vivas()
    }, 5000)
  },
  beforeDestroy() {
    if (this.timerCotizaciones) {
      clearInterval(this.timerCotizaciones)
      this.timerCotizaciones = null
    }
  },
  methods: {
    abrir_asistente_nuevo_instrumento() {
      this.asistenteInstrumentoInicial = null
      this.asistenteContratosIniciales = []
      this.asistenteEstrategiaId = null
      this.idEstrategiaGuardadaEnEdicion = null
      this.asistenteOpen = true
    },
    abrir_asistente_para_estrategia(estrategia) {
      this.asistenteInstrumentoInicial = this.instrumento ? { ...this.instrumento } : null
      this.asistenteContratosIniciales = estrategia.contratos || []
      this.asistenteEstrategiaId = estrategia.id
      this.asistenteOpen = true
    },
    on_confirmar_asistente(payload) {
      if (payload && payload.instrumento) {
        const cambioSymbol = !this.instrumento || this.instrumento.symbol !== payload.instrumento.symbol
        this.instrumento = payload.instrumento
        if (cambioSymbol) {
          this.cargar_cotizacion(this.instrumento.symbol)
        }
      }

      if (payload && Array.isArray(payload.contratos)) {
        const nuevosContratos = payload.contratos.map(c => ({
          ...c,
          posicion: c.posicion || "LONG",
          cantidad: c.cantidad || 1,
          forzar_expandida: false
        }))

        if (this.asistenteEstrategiaId) {
          const est = this.estrategias.find(e => e.id === this.asistenteEstrategiaId)
          if (est) {
            est.contratos = nuevosContratos
            this.actualizar_cotizaciones_vivas()
            return
          }
        }

        // Si se abrió desde el botón global de nuevo instrumento
        if (this.estrategias.length > 0) {
          this.estrategias[0].contratos = nuevosContratos
        } else {
          this.agregar_nueva_estrategia_con_contratos("Estrategia 1", "CUSTOM", nuevosContratos)
        }
        this.actualizar_cotizaciones_vivas()
      }
    },
    agregar_nueva_estrategia() {
      const num = this.estrategias.length + 1
      const nueva = {
        id: Date.now(),
        nombre: `Estrategia ${num}`,
        tipo: "CUSTOM",
        expandida: true,
        vista_cards: "expandida",
        contratos: [],
        precio_simulado: this.cotizacion.imp_cierre
      }
      this.estrategias.push(nueva)
    },
    agregar_nueva_estrategia_con_contratos(nombre, tipo, contratos) {
      const nueva = {
        id: Date.now(),
        nombre: nombre,
        tipo: tipo,
        expandida: true,
        vista_cards: "expandida",
        contratos: contratos || [],
        precio_simulado: this.cotizacion.imp_cierre
      }
      this.estrategias.push(nueva)
    },
    duplicar_estrategia(estrategia) {
      const num = this.estrategias.length + 1
      const clonContratos = (estrategia.contratos || []).map(c => ({ ...c }))
      const clon = {
        id: Date.now(),
        nombre: `Estrategia ${num} (Copia)`,
        tipo: estrategia.tipo,
        expandida: true,
        vista_cards: estrategia.vista_cards || "expandida",
        contratos: clonContratos,
        precio_simulado: estrategia.precio_simulado !== undefined
          ? estrategia.precio_simulado
          : this.cotizacion.imp_cierre
      }
      this.estrategias.push(clon)
    },
    eliminar_estrategia(estrategiaId) {
      this.estrategias = this.estrategias.filter(e => e.id !== estrategiaId)
    },
    editar_nombre_estrategia(estrategia) {
      const actual = estrategia.nombre
      const nuevo = prompt("Ingrese el nombre para esta estrategia:", actual)
      if (nuevo && nuevo.trim().length > 0) {
        estrategia.nombre = nuevo.trim()
      }
    },
    toggle_expandir_todos_grupos() {
      const nuevoEstado = !this.todos_los_grupos_expandidos
      this.estrategias.forEach(e => {
        e.expandida = nuevoEstado
      })
    },
    invertir_posiciones(estrategia) {
      if (!estrategia || !Array.isArray(estrategia.contratos)) return
      estrategia.contratos.forEach(c => {
        c.posicion = c.posicion === "LONG" ? "SHORT" : "LONG"
      })
    },
    remover_pata(estrategia, cod_symbol) {
      estrategia.contratos = estrategia.contratos.filter(
        c => c.cod_symbol !== cod_symbol
      )
    },
    incrementar_cantidad(contrato) {
      if (!contrato.cantidad) this.$set(contrato, "cantidad", 1)
      contrato.cantidad += 1
    },
    decrementar_cantidad(contrato) {
      if (!contrato.cantidad) this.$set(contrato, "cantidad", 1)
      if (contrato.cantidad > 1) {
        contrato.cantidad -= 1
      }
    },

    calcular_metricas(estrategia) {
      if (!estrategia || !Array.isArray(estrategia.contratos) || estrategia.contratos.length === 0) {
        return {
          debito_neto: 0,
          beneficio_maximo: "$0.00",
          perdida_maxima: "$0.00",
          breakevens: "N/A"
        }
      }

      let debitoNeto = 0
      let strikes = []

      estrategia.contratos.forEach(c => {
        const precio = this.obtener_precio_actual_contrato(c) || 0
        const cantidad = Number(c.cantidad || 1)
        const primaTotal = precio * 100 * cantidad
        if (c.posicion === "LONG") {
          debitoNeto += primaTotal
        } else {
          debitoNeto -= primaTotal
        }
        if (c.strike) strikes.push(Number(c.strike))
      })

      strikes.sort((a, b) => a - b)

      let beneficioMaximo = "Ilimitado"
      let perdidaMaxima = "Limitada"
      let beStr = "N/A"

      if (debitoNeto > 0) {
        perdidaMaxima = `-$${debitoNeto.toFixed(2)}`
        if (strikes.length >= 2) {
          const spreadWidth = (strikes[strikes.length - 1] - strikes[0]) * 100
          const maxProfit = Math.max(0, spreadWidth - debitoNeto)
          beneficioMaximo = `+$${maxProfit.toFixed(2)}`
          beStr = `$${(strikes[0] + debitoNeto / 100).toFixed(2)}`
        } else if (strikes.length === 1) {
          beStr = `$${(strikes[0] + debitoNeto / 100).toFixed(2)}`
        }
      } else {
        const credito = Math.abs(debitoNeto)
        beneficioMaximo = `+$${credito.toFixed(2)}`
        if (strikes.length >= 2) {
          const spreadWidth = (strikes[strikes.length - 1] - strikes[0]) * 100
          const maxLoss = Math.max(0, spreadWidth - credito)
          perdidaMaxima = `-$${maxLoss.toFixed(2)}`
          beStr = `$${(strikes[0] - credito / 100).toFixed(2)}`
        } else if (strikes.length === 1) {
          beStr = `$${(strikes[0] - credito / 100).toFixed(2)}`
        }
      }

      return {
        debito_neto: debitoNeto,
        beneficio_maximo: beneficioMaximo,
        perdida_maxima: perdidaMaxima,
        breakevens: beStr
      }
    },

    calcular_prima_total(contrato) {
      const precio = this.obtener_precio_actual_contrato(contrato) || 0
      const cant = Number(contrato.cantidad || 1)
      return (precio * 100 * cant).toFixed(2)
    },
    obtener_precio_actual_contrato(contrato) {
      if (!contrato) return null
      const last = Number(contrato.last)
      if (contrato.last !== null && contrato.last !== undefined && Number.isFinite(last)) {
        return last
      }
      const bid = Number(contrato.bid)
      const ask = Number(contrato.ask)
      const tieneBid = contrato.bid !== null && contrato.bid !== undefined && Number.isFinite(bid)
      const tieneAsk = contrato.ask !== null && contrato.ask !== undefined && Number.isFinite(ask)
      if (tieneBid && tieneAsk) return (bid + ask) / 2
      if (tieneBid) return bid
      if (tieneAsk) return ask
      return null
    },
    calcular_delta(contrato) {
      if (contrato.delta) return contrato.delta
      const sign = contrato.tipo === "CALL" ? "+" : "-"
      return contrato.is_itm ? `${sign}0.65` : `${sign}0.35`
    },
    calcular_theta(contrato) {
      if (contrato.theta) return contrato.theta
      return "-0.04"
    },
    calcular_dias_expiracion(contrato) {
      if (!contrato) return 0
      const fechaVenc = contrato.fch_vencimiento || contrato.expiracion
      if (!fechaVenc) return 0
      const fechaFin = moment(fechaVenc, ["YYYY-MM-DD", "YYYYMMDD", "DD/MM/YYYY"])
      if (!fechaFin.isValid()) return 0
      const hoy = moment().startOf("day")
      const diff = fechaFin.diff(hoy, "days")
      return diff >= 0 ? diff : 0
    },
    formatear_dias_expiracion(contrato) {
      const dias = this.calcular_dias_expiracion(contrato)
      if (dias === 0) return "Vence hoy"
      if (dias === 1) return "1d"
      return `${dias}d`
    },
    obtener_color_dias_expiracion(contrato) {
      const dias = this.calcular_dias_expiracion(contrato)
      if (dias <= 3) return "text-red-9 text-weight-bolder"
      if (dias <= 14) return "text-orange-9 text-weight-bold"
      return "text-grey-8"
    },
    obtener_badge_dias_bg(contrato) {
      const dias = this.calcular_dias_expiracion(contrato)
      if (dias <= 3) return "red-1"
      if (dias <= 14) return "orange-1"
      return "grey-2"
    },
    calcular_dias_expiracion_minima(estrategia) {
      if (!estrategia || !Array.isArray(estrategia.contratos) || estrategia.contratos.length === 0) {
        return null
      }

      let minDias = Infinity
      let fechaMasCercana = null

      estrategia.contratos.forEach(c => {
        const dias = this.calcular_dias_expiracion(c)
        if (dias < minDias) {
          minDias = dias
          fechaMasCercana = c.expiracion_corta || c.fch_vencimiento
        }
      })

      if (minDias === Infinity) return null

      let badgeClass = "badge-dias-normal"
      if (minDias <= 3) {
        badgeClass = "badge-dias-urgente"
      } else if (minDias <= 14) {
        badgeClass = "badge-dias-alerta"
      }

      return {
        dias: minDias,
        fecha: fechaMasCercana,
        textoCorto: minDias === 0 ? "0d (hoy)" : `${minDias}d`,
        badgeClass,
        tooltip: `Expiración más próxima de la estrategia: ${minDias === 0 ? 'Vence hoy' : minDias + ' días'} (${fechaMasCercana || ''})`
      }
    },
    resumen_patas_estrategia(estrategia) {
      if (!estrategia || !Array.isArray(estrategia.contratos) || estrategia.contratos.length === 0) {
        return "Sin contratos configurados"
      }

      return estrategia.contratos.map(c => {
        const accion = c.posicion === "SHORT" ? "SELL" : "BUY"
        const tipo = c.tipo || "CALL"
        const strikeNum = Number(c.strike || 0)
        const strike = strikeNum % 1 === 0 ? strikeNum.toFixed(0) : strikeNum.toFixed(2)
        const precio = c.precio_apertura !== undefined
          ? Number(c.precio_apertura)
          : (this.obtener_precio_actual_contrato(c) || 0)
        const cant = Number(c.cantidad || 1)
        const primaTotal = Math.round(precio * 100 * cant)
        const cantTxt = cant > 1 ? ` (${cant}x)` : ""
        return `${accion} ${tipo} ${strike} $${primaTotal}${cantTxt}`
      }).join(" / ")
    },
    resumen_flujo_estrategia(estrategia) {
      if (!estrategia || !Array.isArray(estrategia.contratos) || estrategia.contratos.length === 0) {
        return null
      }

      let flujoNeto = 0
      estrategia.contratos.forEach(c => {
        const precio = c.precio_apertura !== undefined
          ? Number(c.precio_apertura)
          : (this.obtener_precio_actual_contrato(c) || 0)
        const cant = Number(c.cantidad || 1)
        const total = precio * 100 * cant
        if (c.posicion === "SHORT") {
          flujoNeto += total // Crédito recibido (dinero entra)
        } else {
          flujoNeto -= total // Débito pagado (dinero sale)
        }
      })

      const monto = Math.round(Math.abs(flujoNeto))

      if (flujoNeto > 0) {
        return {
          tipo: "CREDITO",
          texto: `+$${monto} CR`,
          tooltip: `Entra dinero a tu balance: recibes un crédito neto de $${monto} (CR)`,
          icon: "arrow_downward",
          color: "positive",
          badgeClass: "badge-flujo-credito"
        }
      } else if (flujoNeto < 0) {
        return {
          tipo: "DEBITO",
          texto: `-$${monto} DB`,
          tooltip: `Sale dinero de tu balance: pagas un débito neto de $${monto} (DB)`,
          icon: "arrow_upward",
          color: "negative",
          badgeClass: "badge-flujo-debito"
        }
      } else {
        return {
          tipo: "NEUTRO",
          texto: `$0`,
          tooltip: "Estrategia con costo/flujo neto cero",
          icon: "remove",
          color: "grey-7",
          badgeClass: "badge-flujo-neutro"
        }
      }
    },
    calcular_valor_actual_estrategia(estrategia) {
      if (!estrategia || !Array.isArray(estrategia.contratos) || estrategia.contratos.length === 0) {
        return null
      }

      let totalLong = 0
      let totalShort = 0

      estrategia.contratos.forEach(c => {
        const precio = this.obtener_precio_actual_contrato(c) || 0
        const cant = Number(c.cantidad || 1)
        const valorPata = precio * 100 * cant

        if (c.posicion === "LONG") {
          totalLong += valorPata
        } else {
          totalShort += valorPata
        }
      })

      // Valor actual de liquidación a mercado (Mark-to-Market de la combinación)
      const valorLiquidacion = totalLong - totalShort
      const valorSpread = Math.abs(valorLiquidacion)
      const montoFormateado = Math.round(valorSpread)

      const tooltipText = `Mark (Precio actual de mercado): $${valorSpread.toFixed(2)} | Patas LONG: +$${totalLong.toFixed(2)} | Patas SHORT: -$${totalShort.toFixed(2)}`

      return {
        valor_spread: valorSpread,
        valor_liquidacion: valorLiquidacion,
        monto_redondeado: montoFormateado,
        texto: `Mark: $${montoFormateado}`,
        tooltip: tooltipText
      }
    },
    calcular_pnl_estrategia(estrategia) {
      if (!estrategia || !Array.isArray(estrategia.contratos) || estrategia.contratos.length === 0) {
        return null
      }

      // 1. Costo/Flujo neto inicial de apertura (>0 débito pagado, <0 crédito cobrado)
      let costoAperturaNeto = 0
      estrategia.contratos.forEach(c => {
        const precioApertura = c.precio_apertura !== undefined
          ? Number(c.precio_apertura)
          : (this.obtener_precio_actual_contrato(c) || 0)
        const cant = Number(c.cantidad || 1)
        const total = precioApertura * 100 * cant
        if (c.posicion === "LONG") {
          costoAperturaNeto += total
        } else {
          costoAperturaNeto -= total
        }
      })

      // 2. Valor actual de liquidación de mercado
      let totalLong = 0
      let totalShort = 0
      estrategia.contratos.forEach(c => {
        const precioActual = this.obtener_precio_actual_contrato(c) || 0
        const cant = Number(c.cantidad || 1)
        const total = precioActual * 100 * cant
        if (c.posicion === "LONG") {
          totalLong += total
        } else {
          totalShort += total
        }
      })
      const valorLiquidacionActual = totalLong - totalShort

      // 3. P&L No Realizado
      const pnlTotal = valorLiquidacionActual - costoAperturaNeto
      const baseCalculo = Math.abs(costoAperturaNeto) || 1
      const pnlPct = (pnlTotal / baseCalculo) * 100

      const montoAbs = Math.round(Math.abs(pnlTotal))
      const pctAbs = Math.abs(pnlPct).toFixed(1)

      if (pnlTotal > 0.01) {
        return {
          estado: "GANANDO",
          monto: pnlTotal,
          pct: pnlPct,
          texto: `▲ +$${montoAbs} (+${pctAbs}%)`,
          badgeClass: "badge-pnl-positivo",
          capsulaClass: "capsula-pnl-positivo",
          tooltip: `Posición GANANDO: +$${pnlTotal.toFixed(2)} (+${pnlPct.toFixed(1)}%) respecto al costo de apertura`
        }
      } else if (pnlTotal < -0.01) {
        return {
          estado: "PERDIENDO",
          monto: pnlTotal,
          pct: pnlPct,
          texto: `▼ -$${montoAbs} (-${pctAbs}%)`,
          badgeClass: "badge-pnl-negativo",
          capsulaClass: "capsula-pnl-negativo",
          tooltip: `Posición PERDIENDO: -$${Math.abs(pnlTotal).toFixed(2)} (-${pctAbs}%) respecto al costo de apertura`
        }
      } else {
        return {
          estado: "NEUTRO",
          monto: 0,
          pct: 0,
          texto: `= $0 (0.0%)`,
          badgeClass: "badge-pnl-neutro",
          capsulaClass: "capsula-pnl-neutro",
          tooltip: "Posición en equilibrio / break-even (P&L: $0.00)"
        }
      }
    },
    resumen_texto_estrategia(estrategia) {
      const patas = this.resumen_patas_estrategia(estrategia)
      const flujo = this.resumen_flujo_estrategia(estrategia)
      const actual = this.calcular_valor_actual_estrategia(estrategia)
      const pnl = this.calcular_pnl_estrategia(estrategia)
      let res = patas
      if (flujo) res += `: ${flujo.texto}`
      if (actual) res += ` | ${actual.texto}`
      if (pnl) res += ` | ${pnl.texto}`
      return res
    },
    formatear_numero(val) {
      if (val === null || val === undefined || isNaN(Number(val))) return "0.00"
      return Number(val).toFixed(2)
    },
    formatear_cotizacion(val) {
      if (val === null || val === undefined || isNaN(Number(val))) return "N/D"
      return `$${Number(val).toFixed(2)}`
    },
    async actualizar_cotizaciones_vivas() {
      if (this.actualizandoCotizaciones || !this.instrumento || !this.instrumento.symbol) return

      const symbol = this.instrumento.symbol
      const optionQuotesByConid = new Map()
      const optionIds = new Set()
      const fallbackSymbols = new Set()
      const estrategias = this.estrategias || []
      estrategias.forEach(grupo => {
        const contratos = grupo.contratos || []
        contratos.forEach(contrato => {
          const conid = Number(contrato.conid)
          if (Number.isInteger(conid) && conid > 0) {
            if (!optionQuotesByConid.has(conid)) optionQuotesByConid.set(conid, contrato.cod_symbol)
          } else if (contrato.id_contrato_opcion) {
            optionIds.add(contrato.id_contrato_opcion)
          } else if (contrato.cod_symbol) {
            fallbackSymbols.add(contrato.cod_symbol)
          }
        })
      })

      const quoteParams = {
        provider: "ibkr",
        id_symbol: this.instrumento.id_symbol || this.instrumento.id,
        id_contrato_opcion: Array.from(optionIds),
        conid: Array.from(optionQuotesByConid.keys()),
        cod_symbol: [
          ...Array.from(optionQuotesByConid.values()),
          ...Array.from(fallbackSymbols),
          ...((this.instrumento.id_symbol || this.instrumento.id) ? [] : [symbol])
        ]
      }

      this.actualizandoCotizaciones = true
      try {
        const quotes = await Cotizacion.get_cotizaciones(quoteParams)
        if (!Array.isArray(quotes) || !this.instrumento || this.instrumento.symbol !== symbol) return

        const quotesByOptionId = new Map()
        const quotesByCode = new Map()
        quotes.forEach(quote => {
          if (quote.id_symbol && String(quote.id_symbol) === String(this.instrumento.id_symbol || this.instrumento.id)) {
            this.actualizar_cotizacion_subyacente(quote)
          }
          if (String(quote.cod_symbol || "").toUpperCase() === String(symbol).toUpperCase()) {
            this.actualizar_cotizacion_subyacente(quote)
          }
          if (quote.id_contrato_opcion) quotesByOptionId.set(String(quote.id_contrato_opcion), quote)
          if (quote.cod_symbol) quotesByCode.set(String(quote.cod_symbol).toUpperCase(), quote)
        })

        estrategias.forEach(grupo => {
          const contratos = grupo.contratos || []
          contratos.forEach(contrato => {
            const quote = (contrato.id_contrato_opcion && quotesByOptionId.get(String(contrato.id_contrato_opcion)))
              || quotesByCode.get(String(contrato.cod_symbol || "").toUpperCase())
            if (!quote) return
            contrato.bid = quote.bid !== null && quote.bid !== undefined ? Number(quote.bid) : null
            contrato.ask = quote.ask !== null && quote.ask !== undefined ? Number(quote.ask) : null
            contrato.last = quote.last !== null && quote.last !== undefined ? Number(quote.last) : null
          })
        })
      } finally {
        this.actualizandoCotizaciones = false
      }
    },
    actualizar_cotizacion_subyacente(quote) {
      if (quote.imp_cierre !== null && quote.imp_cierre !== undefined) {
        this.cotizacion.imp_cierre = Number(quote.imp_cierre)
      }
      if (quote.imp_cierre_anterior !== null && quote.imp_cierre_anterior !== undefined) {
        this.cotizacion.imp_cierre_anterior = Number(quote.imp_cierre_anterior)
      }
      if (quote.imp_variacion !== null && quote.imp_variacion !== undefined) {
        this.cotizacion.imp_variacion = Number(quote.imp_variacion)
      }
      if (quote.pct_variacion !== null && quote.pct_variacion !== undefined) {
        this.cotizacion.pct_variacion = Number(quote.pct_variacion)
      }
    },
    cargar_cotizacion(symbol) {
      if (!symbol) return
      this.cargando_cotizacion = true
      this.cotizacion = {
        imp_cierre_anterior: null,
        imp_apertura: null,
        imp_maximo: null,
        imp_minimo: null,
        imp_cierre: null,
        imp_variacion: null,
        pct_variacion: null
      }

      Cotizacion.get_cotizacion(symbol)
        .then(data => {
          if (data && data.imp_cierre !== null && data.imp_cierre !== undefined) {
            this.cotizacion.imp_cierre = Number(data.imp_cierre)
            this.cotizacion.imp_cierre_anterior = data.imp_cierre_anterior !== null
              && data.imp_cierre_anterior !== undefined
              ? Number(data.imp_cierre_anterior)
              : null
            this.cotizacion.imp_variacion = data.imp_variacion !== null
              && data.imp_variacion !== undefined
              ? Number(data.imp_variacion)
              : null
            this.cotizacion.pct_variacion = data.pct_variacion !== null
              && data.pct_variacion !== undefined
              ? Number(data.pct_variacion)
              : null
            this.estrategias.forEach(e => {
              if (e.precio_simulado === null || e.precio_simulado === undefined) {
                e.precio_simulado = this.cotizacion.imp_cierre
              }
            })
          }
        })
        .catch(err => {
          console.error("No se pudo obtener la cotización del backend:", err)
        })
        .finally(() => {
          this.cargando_cotizacion = false
          this.consultar_variacion_semanal(symbol)
        })
    },
    consultar_variacion_semanal(symbol) {
      try {
        const anyo = moment().year()
        const semana = moment().week()
        const cod_semana = `${anyo}${_.padStart(semana, 2, "0")}`
        const variacionSemanal = new VariacionSemanal()

        variacionSemanal.get_variacion_semana_actual({
          cod_symbol: symbol,
          cod_semana: cod_semana
        }).then(res => {
          if (res && res.data && res.data.data) {
            const d = res.data.data
            if (d.imp_cierre_ant) this.cotizacion.imp_cierre_anterior = d.imp_cierre_ant
            if (d.imp_apertura) this.cotizacion.imp_apertura = d.imp_apertura
            if (d.imp_maximo) this.cotizacion.imp_maximo = d.imp_maximo
            if (d.imp_minimo) this.cotizacion.imp_minimo = d.imp_minimo
            if (d.imp_cierre) {
              this.cotizacion.imp_cierre = d.imp_cierre
              this.estrategias.forEach(e => {
              if (e.precio_simulado === null || e.precio_simulado === undefined) {
                e.precio_simulado = d.imp_cierre
              }
              })
            }
            if (d.imp_variacion_cierre !== undefined) this.cotizacion.imp_variacion = d.imp_variacion_cierre
            if (d.pct_variacion_cierre !== undefined) this.cotizacion.pct_variacion = d.pct_variacion_cierre
          }
        }).catch(err => {
          console.debug("Variación semanal no disponible:", err)
        })
      } catch (e) {
        console.debug("Error procesando variación semanal:", e)
      }
    },
    // ========================================================
    // MÉTODOS PARA GUARDAR Y GESTIONAR ESTRATEGIAS (SOLO GUI)
    // ========================================================
    abrir_dialogo_guardar_estrategia() {
      if (this.estrategias.length === 0) {
        if (this.$q && this.$q.notify) {
          this.$q.notify({
            type: "warning",
            icon: "warning",
            message: "No hay grupos de estrategia en el simulador para guardar."
          })
        }
        return
      }

      const totalContratos = this.total_contratos_simulacion
      if (totalContratos === 0) {
        if (this.$q && this.$q.notify) {
          this.$q.notify({
            type: "warning",
            icon: "warning",
            message: "Ninguno de los grupos tiene contratos asignados. Añada al menos una pata antes de guardar la estrategia."
          })
        }
        return
      }

      const sym = this.instrumento ? this.instrumento.symbol : ""
      const cantGrupos = this.estrategias.length
      const sugerenciaNombre = cantGrupos === 1 && this.estrategias[0].nombre
        ? this.estrategias[0].nombre
        : `Estrategia ${sym} (${cantGrupos} ${cantGrupos === 1 ? 'grupo' : 'grupos'})`
      const guardadaEnEdicion = this.estrategias_guardadas.find(
        guardada => String(guardada.id) === String(this.idEstrategiaGuardadaEnEdicion)
      )

      this.formularioGuardar = {
        nombre: guardadaEnEdicion ? guardadaEnEdicion.nombre : sugerenciaNombre,
        etiqueta: guardadaEnEdicion ? (guardadaEnEdicion.tipo || "ESTRATEGIA") : "ESTRATEGIA",
        notas: guardadaEnEdicion ? (guardadaEnEdicion.notas || "") : ""
      }
      this.dialogoGuardarOpen = true
    },
    async confirmar_guardar_estrategia() {
      if (this.guardandoEstrategia) return
      if (!this.formularioGuardar.nombre || this.formularioGuardar.nombre.trim().length === 0) {
        if (this.$q && this.$q.notify) {
          this.$q.notify({
            type: "negative",
            message: "Por favor, ingrese un nombre para la estrategia."
          })
        }
        return
      }

      const contratoSinFechaValida = (this.estrategias || []).some(grupo =>
        (grupo.contratos || []).some(contrato => !this.normalizar_fecha_vencimiento(
          contrato.fch_vencimiento || contrato.fecha_vencimiento
        ))
      )
      if (contratoSinFechaValida) {
        if (this.$q && this.$q.notify) {
          this.$q.notify({
            type: "negative",
            message: "Hay contratos con una fecha de vencimiento inválida. Vuelva a seleccionar la expiración antes de guardar."
          })
        }
        return
      }

      this.guardandoEstrategia = true
      const totalContratos = this.total_contratos_simulacion
      const payload = {
        id_subyacente_symbol: this.instrumento && (this.instrumento.id_symbol || this.instrumento.id),
        cod_subyacente: this.instrumento && this.instrumento.symbol,
        nombre: this.formularioGuardar.nombre.trim(),
        etiqueta: (this.formularioGuardar.etiqueta || "ESTRATEGIA").trim(),
        notas: (this.formularioGuardar.notas || "").trim() || null,
        moneda_id: (this.instrumento && this.instrumento.moneda_id) || "USD",
        grupos: this.estrategias.map((grupo, indice) => ({
          orden: indice + 1,
          nombre: (grupo.nombre || `Grupo ${indice + 1}`).trim(),
          tipo: (grupo.tipo || "CUSTOM").trim(),
          contratos: (grupo.contratos || []).map((contrato, pataIndice) => ({
            id_contrato_opcion: contrato.id_contrato_opcion || null,
            cod_symbol: contrato.cod_symbol,
            tipo_opcion: String(contrato.tipo || contrato.tipo_opcion || "CALL").toUpperCase(),
            fecha_vencimiento: this.normalizar_fecha_vencimiento(
              contrato.fch_vencimiento || contrato.fecha_vencimiento
            ),
            strike: Number(contrato.strike),
            posicion: String(contrato.posicion || "LONG").toUpperCase(),
            cantidad: Number(contrato.cantidad || 1),
            multiplicador: Number(contrato.multiplicador || 100),
            precio_apertura: contrato.precio_apertura !== undefined && contrato.precio_apertura !== null
              ? Number(contrato.precio_apertura)
              : (contrato.last !== undefined && contrato.last !== null
                ? Number(contrato.last)
                : (contrato.ask !== undefined && contrato.ask !== null
                  ? Number(contrato.ask)
                  : (contrato.bid !== undefined && contrato.bid !== null ? Number(contrato.bid) : null))),
            moneda_id: contrato.moneda_id || (this.instrumento && this.instrumento.moneda_id) || "USD",
            orden: pataIndice + 1
          }))
        }))
      }

      try {
        const idGuardada = this.idEstrategiaGuardadaEnEdicion
        const response = idGuardada
          ? await SimulacionEstrategiaApi.actualizar(idGuardada, payload)
          : await SimulacionEstrategiaApi.guardar(payload)
        const appResponse = response.data || {}
        if (!appResponse.success || !appResponse.data) {
          throw new Error(appResponse.message || "No se pudo guardar la estrategia.")
        }
        const indiceGuardada = this.estrategias_guardadas.findIndex(
          guardada => String(guardada.id) === String(appResponse.data.id)
        )
        if (indiceGuardada >= 0) {
          this.$set(this.estrategias_guardadas, indiceGuardada, appResponse.data)
        } else {
          this.estrategias_guardadas.unshift(appResponse.data)
        }
        this.idEstrategiaGuardadaEnEdicion = appResponse.data.id
        this.dialogoGuardarOpen = false
        if (this.$q && this.$q.notify) {
          this.$q.notify({
            type: "positive",
            icon: "check_circle",
            message: `Estrategia "${appResponse.data.nombre}" ${idGuardada ? 'actualizada' : 'guardada'} con éxito`,
            caption: `${appResponse.data.num_grupos} grupos (${totalContratos} contratos) guardados en la base de datos`,
            position: "top-right",
            timeout: 3000
          })
        }
      } catch (err) {
        console.error("Error guardando estrategia:", err)
        const message = err.response && err.response.data
          ? err.response.data.message
          : err.message
        if (this.$q && this.$q.notify) {
          this.$q.notify({
            type: "negative",
            icon: "error",
            message: message || "No se pudo guardar la estrategia.",
            position: "top-right"
          })
        }
      } finally {
        this.guardandoEstrategia = false
      }
    },
    normalizar_fecha_vencimiento(valor) {
      if (!valor) return null

      if (valor instanceof Date) {
        if (Number.isNaN(valor.getTime())) return null
        return valor.toISOString().slice(0, 10)
      }

      const texto = String(valor).trim()
      const fechaIso = texto.match(/^(\d{4}-\d{2}-\d{2})/)
      if (fechaIso) {
        const fechaParseada = moment(fechaIso[1], "YYYY-MM-DD", true)
        return fechaParseada.isValid() ? fechaParseada.format("YYYY-MM-DD") : null
      }

      const fechaCompacta = texto.match(/^(\d{4})(\d{2})(\d{2})$/)
      if (fechaCompacta) {
        const fechaNormalizada = `${fechaCompacta[1]}-${fechaCompacta[2]}-${fechaCompacta[3]}`
        const fechaParseada = moment(fechaNormalizada, "YYYY-MM-DD", true)
        return fechaParseada.isValid() ? fechaParseada.format("YYYY-MM-DD") : null
      }

      const fechaParseada = moment(
        texto,
        ["YYYY-MM-DD", "YYYYMMDD", "YYYY/MM/DD", "DD/MM/YYYY", "DD-MM-YYYY"],
        true
      )
      return fechaParseada.isValid() ? fechaParseada.format("YYYY-MM-DD") : null
    },
    async cargar_estrategias_guardadas() {
      this.cargandoEstrategiasGuardadas = true
      try {
        const response = await SimulacionEstrategiaApi.listar()
        const appResponse = response.data || {}
        if (!appResponse.success || !Array.isArray(appResponse.data)) {
          throw new Error(appResponse.message || "No se pudieron cargar las estrategias guardadas.")
        }
        this.estrategias_guardadas = appResponse.data
      } catch (err) {
        console.error("Error cargando estrategias guardadas:", err)
        this.estrategias_guardadas = []
        if (this.$q && this.$q.notify) {
          this.$q.notify({
            type: "negative",
            message: err.response && err.response.data
              ? err.response.data.message
              : "No se pudieron cargar las estrategias de la base de datos.",
            position: "top-right"
          })
        }
      } finally {
        this.cargandoEstrategiasGuardadas = false
      }
    },
    cargar_estrategia_guardada(guardada) {
      if (!guardada) return
      this.idEstrategiaGuardadaEnEdicion = guardada.id

      // Si tiene un instrumento guardado y es distinto al actual, actualizar instrumento
      if (guardada.instrumento && (!this.instrumento || this.instrumento.symbol !== guardada.instrumento.symbol)) {
        this.instrumento = { ...guardada.instrumento }
        this.cargar_cotizacion(this.instrumento.symbol)
      }

      if (guardada.grupos && Array.isArray(guardada.grupos) && guardada.grupos.length > 0) {
        // Restaurar estado completo de todos los grupos
        const clonGrupos = JSON.parse(JSON.stringify(guardada.grupos))
        this.estrategias = clonGrupos.map((g, idx) => ({
          ...g,
          id: Date.now() + idx,
          expandida: true,
          vista_cards: g.vista_cards || "expandida"
        }))
      } else if (guardada.contratos && Array.isArray(guardada.contratos)) {
        // Retrocompatibilidad con guardados antiguos de un solo grupo
        const clonContratos = JSON.parse(JSON.stringify(guardada.contratos))
        const nueva = {
          id: Date.now(),
          nombre: guardada.nombre || `Estrategia 1`,
          tipo: guardada.tipo || "CUSTOM",
          expandida: true,
          vista_cards: "expandida",
          contratos: clonContratos,
          precio_simulado: guardada.cotizacion_referencia || this.cotizacion.imp_cierre,
          notas: guardada.notas || ""
        }
        this.estrategias = [nueva]
      }

      this.dialogoEstrategiasGuardadasOpen = false
      this.asistenteOpen = false
      this.actualizar_cotizaciones_vivas()

      if (this.$q && this.$q.notify) {
        const cant = this.estrategias.length
        this.$q.notify({
          type: "positive",
          icon: "file_download_done",
          message: `Estrategia "${guardada.nombre}" cargada en el simulador`,
          caption: `Se ${cant === 1 ? 'restauró 1 grupo' : `restauraron ${cant} grupos`} en el simulador`,
          position: "top-right"
        })
      }
    },
    contar_total_contratos_guardada(guardada) {
      if (!guardada) return 0
      if (guardada.total_contratos !== undefined) return guardada.total_contratos
      if (guardada.grupos && Array.isArray(guardada.grupos)) {
        return guardada.grupos.reduce((acc, g) => acc + (g.contratos ? g.contratos.length : 0), 0)
      }
      if (guardada.contratos && Array.isArray(guardada.contratos)) {
        return guardada.contratos.length
      }
      return 0
    },
    async eliminar_estrategia_guardada(guardadaId) {
      try {
        const response = await SimulacionEstrategiaApi.eliminar(guardadaId)
        const appResponse = response.data || {}
        if (!appResponse.success) {
          throw new Error(appResponse.message || "No se pudo eliminar la estrategia.")
        }
        this.estrategias_guardadas = this.estrategias_guardadas.filter(g => g.id !== guardadaId)
        if (String(this.idEstrategiaGuardadaEnEdicion) === String(guardadaId)) {
          this.idEstrategiaGuardadaEnEdicion = null
        }
        if (this.$q && this.$q.notify) {
          this.$q.notify({
            type: "info",
            icon: "delete",
            message: "Estrategia eliminada de guardadas",
            position: "top-right"
          })
        }
      } catch (err) {
        console.error("Error eliminando estrategia guardada:", err)
        if (this.$q && this.$q.notify) {
          this.$q.notify({
            type: "negative",
            message: err.response && err.response.data
              ? err.response.data.message
              : "No se pudo eliminar la estrategia guardada.",
            position: "top-right"
          })
        }
      }
    }
  }
}
</script>

<style scoped>
.panel-estrategia-opciones {
  background-color: #f4f6f9;
  min-height: calc(100vh - 60px);
}

.instrumento-card-compact {
  border-left: 4px solid #1e293b;
}

.grupo-estrategia-card {
  border-left: 4px solid #334155;
  border-radius: 6px;
  overflow: hidden;
}

.grupo-header {
  border-bottom: 1px solid #e0e0e0;
}

.metric-pill {
  padding: 2px 6px;
  border-radius: 4px;
  background-color: #f8fafc;
}

.pata-card {
  border-radius: 6px;
  border: 1px solid #e0e0e0;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.pata-card:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

.pata-card-resumida {
  border-radius: 6px;
  border: 1px solid #dcdcdc;
  background-color: #ffffff;
  transition: box-shadow 0.2s ease;
  min-height: 58px;
}

.pata-borde-call {
  border-left: 3px solid #0d47a1;
}

.pata-borde-put {
  border-left: 3px solid #7b1fa2;
}

.pata-card-resumida:hover {
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
}

.resumen-colapsado-badge {
  background-color: #f8fafc;
  color: #334155;
  border: 1px solid #e2e8f0;
  letter-spacing: 0.2px;
  transition: all 0.15s ease;
}

.resumen-colapsado-badge:hover {
  background-color: #f1f5f9;
  border-color: #cbd5e1;
}

/* BADGES DE FLUJO: SOFT TINTS SOFISTICADOS */
.badge-flujo-credito {
  background-color: #ecfdf5;
  color: #065f46;
  border: 1px solid #a7f3d0;
  letter-spacing: 0.3px;
  border-radius: 4px;
  min-width: 90px;
  justify-content: center;
  text-align: center;
}

.badge-flujo-debito {
  background-color: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
  letter-spacing: 0.3px;
  border-radius: 4px;
  min-width: 90px;
  justify-content: center;
  text-align: center;
}

.badge-flujo-neutro {
  background-color: #f1f5f9;
  color: #475569;
  border: 1px solid #cbd5e1;
  letter-spacing: 0.3px;
  border-radius: 4px;
  min-width: 90px;
  justify-content: center;
  text-align: center;
}

/* CÁPSULA UNIFICADA: MARK + P&L WIDGET SLATE OSCURO */
.capsula-mark-pnl {
  display: inline-flex;
  overflow: hidden;
  border-radius: 5px;
  letter-spacing: 0.3px;
  min-width: 210px;
  background-color: #1e293b;
  border: 1px solid #334155;
}

.capsula-seccion-mark {
  background-color: #1e293b;
  color: #cbd5e1;
  min-width: 90px;
  justify-content: center;
}

.capsula-divisor {
  width: 1px;
  background-color: #334155;
}

.capsula-seccion-pnl {
  flex: 1;
  justify-content: center;
  background-color: #0f172a;
}

.capsula-pnl-positivo {
  border-color: #059669;
}

.capsula-pnl-positivo .capsula-seccion-pnl {
  color: #34d399;
}

.capsula-pnl-negativo {
  border-color: #dc2626;
}

.capsula-pnl-negativo .capsula-seccion-pnl {
  color: #f87171;
}

.capsula-pnl-neutro {
  border-color: #475569;
}

.capsula-pnl-neutro .capsula-seccion-pnl {
  color: #94a3b8;
}

.font-mono {
  font-family: monospace;
}

.border-dashed {
  border: 2px dashed #cfd8dc;
}

/* BADGE DE DÍAS A EXPIRACIÓN MÍNIMA DE LA ESTRATEGIA (DTE) */
.badge-dias-exp-min {
  border-radius: 4px;
  font-size: 11px;
  padding: 2px 6px;
  letter-spacing: 0.2px;
}

.badge-dias-normal {
  background-color: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
}

.badge-dias-alerta {
  background-color: #fffbeb;
  color: #b45309;
  border: 1px solid #fde68a;
}

.badge-dias-urgente {
  background-color: #fef2f2;
  color: #b91c1c;
  border: 1px solid #fecaca;
}

/* SOFT PILLS PARA CONTRATOS */
.pill-call {
  background-color: #e0f2fe;
  color: #0369a1;
  border: 1px solid #bae6fd;
}

.pill-put {
  background-color: #f3e8ff;
  color: #7e22ce;
  border: 1px solid #e9d5ff;
}

.pill-long {
  background-color: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #bfdbfe;
}

.pill-short {
  background-color: #fef2f2;
  color: #b91c1c;
  border: 1px solid #fecaca;
}

.pill-itm {
  background-color: #ecfdf5;
  color: #047857;
  border: 1px solid #a7f3d0;
}

.pill-otm {
  background-color: #f1f5f9;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.pill-credito {
  background-color: #ecfdf5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.pill-debito {
  background-color: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.hover-bg-grey-1:hover {
  background-color: #f8fafc;
}

.hover-underline:hover {
  text-decoration: underline;
}

.hover-text-negative:hover {
  color: #dc2626 !important;
}

.border-grey {
  border: 1px solid #e2e8f0;
}

.border-bottom-light {
  border-bottom: 1px solid #e2e8f0;
}
</style>
