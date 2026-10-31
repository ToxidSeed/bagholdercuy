<template>
  <div class="panel-estrategia-opciones q-pa-sm">

    <!-- TOOLBAR PRINCIPAL -->
    <q-toolbar class="bg-white rounded-borders shadow-1 q-mb-xs q-py-none" style="min-height: 40px;">
      <q-avatar icon="alt_route" color="blue-10" text-color="white" size="26px" class="q-mr-xs" />
      <q-toolbar-title class="text-subtitle1 text-weight-bold text-blue-10">
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
            <q-avatar size="28px" color="blue-10" text-color="white" class="text-weight-bold">
              {{ instrumento.symbol.substring(0, 2) }}
            </q-avatar>
            <span class="text-subtitle1 text-weight-bolder text-blue-10">{{ instrumento.symbol }}</span>
            <q-badge color="amber-8" text-color="dark" class="text-caption text-weight-bold">
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
              color="primary"
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
              <span class="text-body2 text-weight-bolder text-grey-9">${{ formatear_numero(cotizacion.imp_cierre_anterior) }}</span>
            </div>

            <q-separator vertical class="gt-xs" />

            <!-- 2. Apertura -->
            <div class="metric-pill">
              <span class="text-caption text-grey-6 q-mr-xs">Apertura:</span>
              <span class="text-body2 text-weight-bolder text-grey-9">${{ formatear_numero(cotizacion.imp_apertura) }}</span>
            </div>

            <q-separator vertical class="gt-xs" />

            <!-- 3. Máximo -->
            <div class="metric-pill">
              <span class="text-caption text-green-9 q-mr-xs">Máx:</span>
              <span class="text-body2 text-weight-bolder text-green-9">${{ formatear_numero(cotizacion.imp_maximo) }}</span>
            </div>

            <q-separator vertical class="gt-xs" />

            <!-- 4. Mínimo -->
            <div class="metric-pill">
              <span class="text-caption text-red-9 q-mr-xs">Mín:</span>
              <span class="text-body2 text-weight-bolder text-red-9">${{ formatear_numero(cotizacion.imp_minimo) }}</span>
            </div>

            <q-separator vertical class="gt-xs" />

            <!-- 5. Cierre o Último Valor -->
            <div class="metric-pill bg-blue-1 q-px-sm q-py-xs rounded-borders row items-center">
              <span class="text-caption text-blue-10 text-weight-bold q-mr-xs">Último:</span>
              <span class="text-subtitle2 text-weight-bolder text-blue-10 q-mr-xs">${{ formatear_numero(cotizacion.imp_cierre) }}</span>
              <q-badge
                :color="cotizacion.imp_variacion >= 0 ? 'positive' : 'negative'"
                dense
                text-color="white"
                class="text-caption text-weight-bold"
              >
                <q-icon :name="cotizacion.imp_variacion >= 0 ? 'arrow_drop_up' : 'arrow_drop_down'" size="14px" />
                <span>{{ cotizacion.imp_variacion >= 0 ? '+' : '' }}{{ formatear_numero(cotizacion.imp_variacion) }}</span>
                <span class="q-ml-xs">({{ cotizacion.pct_variacion >= 0 ? '+' : '' }}{{ formatear_numero(cotizacion.pct_variacion) }}%)</span>
              </q-badge>
            </div>

          </div>

          <!-- Lado Derecho: Refrescar cotización -->
          <div class="col-auto row items-center q-pr-xs">
            <q-btn
              flat
              dense
              round
              color="primary"
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
          <q-icon name="view_week" color="blue-10" size="20px" />
          <span class="text-subtitle1 text-weight-bold text-blue-10">
            Grupos de Estrategia
          </span>
          <q-badge color="blue-10" text-color="white" class="text-caption text-weight-bold q-ml-xs">
            {{ estrategias.length }} {{ estrategias.length === 1 ? 'grupo' : 'grupos' }}
          </q-badge>
        </div>

        <div class="row items-center q-gutter-xs">
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
            outline
            dense
            color="primary"
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
            
            <!-- Izquierda: Identificador del Grupo, Nombre y Plantilla -->
            <div class="col-12 col-md-auto row items-center q-gutter-xs no-wrap-sm">
              <!-- Badge Grupo X -->
              <q-badge color="blue-10" text-color="white" class="text-caption text-weight-bold q-px-sm q-py-xs">
                Grupo {{ gIdx + 1 }}
              </q-badge>

              <!-- Nombre editable de la Estrategia -->
              <div class="row items-center no-wrap">
                <span class="text-subtitle2 text-weight-bolder text-dark q-mx-xs">
                  {{ estrategia.nombre }}
                </span>
                <q-btn
                  flat
                  round
                  dense
                  icon="edit"
                  size="xs"
                  color="grey-7"
                  @click="editar_nombre_estrategia(estrategia)"
                >
                  <q-tooltip>Renombrar esta estrategia</q-tooltip>
                </q-btn>
              </div>

              <!-- Selector de Plantilla de Estrategia -->
              <q-select
                v-model="estrategia.tipo"
                :options="estrategias_disponibles"
                dense
                outlined
                emit-value
                map-options
                color="blue-10"
                class="q-ml-sm"
                style="min-width: 220px;"
                @input="tipo => aplicar_plantilla(estrategia, tipo)"
              >
                <template v-slot:option="scope">
                  <q-item v-bind="scope.itemProps" v-on="scope.itemEvents" dense>
                    <q-item-section avatar>
                      <q-icon :name="scope.opt.icon || 'timeline'" color="blue-10" size="18px" />
                    </q-item-section>
                    <q-item-section>
                      <q-item-label class="text-weight-medium">{{ scope.opt.label }}</q-item-label>
                      <q-item-label caption class="text-grey-7">{{ scope.opt.descripcion }}</q-item-label>
                    </q-item-section>
                    <q-item-section side>
                      <q-badge
                        :color="scope.opt.tipo_badge === 'BULLISH' ? 'positive' : scope.opt.tipo_badge === 'BEARISH' ? 'negative' : 'primary'"
                        text-color="white"
                        class="text-caption"
                      >
                        {{ scope.opt.tipo_badge }}
                      </q-badge>
                    </q-item-section>
                  </q-item>
                </template>
              </q-select>

              <!-- Badge de Sesgo (Bullish/Bearish/Neutral) -->
              <q-badge
                :color="obtener_badge_tipo_color(estrategia.tipo)"
                text-color="white"
                class="text-caption text-weight-bold gt-xs"
              >
                {{ obtener_badge_tipo_label(estrategia.tipo) }}
              </q-badge>
            </div>

            <!-- Derecha: Controles de Cards (Resumida / Expandida) y Acciones -->
            <div class="col-12 col-md-auto row items-center justify-end q-gutter-xs q-mt-xs q-mt-md-none">
              
              <!-- TOGGLE VERSIÓN RESUMIDA VS EXPANDIDA DE LAS CARDS -->
              <div class="row items-center q-mr-xs">
                <span class="text-caption text-grey-8 text-weight-medium q-mr-xs gt-xs">Vista Cards:</span>
                <q-btn-toggle
                  v-model="estrategia.vista_cards"
                  dense
                  unelevated
                  toggle-color="blue-10"
                  toggle-text-color="white"
                  color="grey-3"
                  text-color="grey-8"
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

              <!-- Botón Invertir Posiciones Long ⇄ Short -->
              <q-btn
                outline
                color="indigo-9"
                icon="sync_alt"
                dense
                size="sm"
                class="q-px-xs"
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
                color="primary"
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
                color="negative"
                icon="delete_outline"
                size="sm"
                @click="eliminar_estrategia(estrategia.id)"
              >
                <q-tooltip>Eliminar este grupo de estrategia</q-tooltip>
              </q-btn>

              <!-- Botón Colapsar / Expandir Grupo -->
              <q-btn
                flat
                dense
                round
                color="grey-8"
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
                  <div class="text-subtitle2 text-weight-bolder" :class="calcular_metricas(estrategia).debito_neto >= 0 ? 'text-primary' : 'text-positive'">
                    {{ calcular_metricas(estrategia).debito_neto >= 0 ? '-$' : '+$' }}{{ Math.abs(calcular_metricas(estrategia).debito_neto).toFixed(2) }}
                    <q-badge :color="calcular_metricas(estrategia).debito_neto >= 0 ? 'blue-9' : 'positive'" text-color="white" class="q-ml-xs text-caption">
                      {{ calcular_metricas(estrategia).debito_neto >= 0 ? 'DÉBITO' : 'CRÉDITO' }}
                    </q-badge>
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
                  <div class="text-subtitle2 text-weight-bolder text-blue-10">
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
                    :color="estrategia.vista_cards === 'resumida' ? 'blue-8' : 'indigo-8'"
                    text-color="white"
                    class="q-ml-xs text-caption text-weight-bold"
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
                  Seleccione una plantilla predefinida o abra la cadena de opciones.
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
                    class="pata-card-resumida shadow-1 full-height column justify-between"
                  >
                    <!-- Cabecera de Card Resumida -->
                    <div
                      class="q-py-xs q-px-sm row items-center justify-between"
                      :class="contrato.tipo === 'CALL' ? 'bg-blue-1 text-blue-10' : 'bg-purple-1 text-purple-10'"
                    >
                      <div class="row items-center no-wrap">
                        <q-badge
                          :color="contrato.tipo === 'CALL' ? 'blue-10' : 'purple-10'"
                          text-color="white"
                          class="text-weight-bolder text-caption"
                        >
                          {{ contrato.tipo }}
                        </q-badge>
                        <!-- BADGE LONG / SHORT (AZUL / ROJO) -->
                        <q-badge
                          :color="contrato.posicion === 'LONG' ? 'blue-10' : 'red-9'"
                          text-color="white"
                          class="text-weight-bolder text-caption q-ml-xs"
                        >
                          {{ contrato.posicion }}
                        </q-badge>
                        <span class="text-caption text-weight-bolder text-dark q-ml-xs">
                          ${{ Number(contrato.strike).toFixed(2) }}
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
                          <q-tooltip>Ver detalles expandidos de esta pata</q-tooltip>
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

                    <!-- Cuerpo Resumido -->
                    <div class="q-pa-xs">
                      <div class="row items-center justify-between text-caption q-px-xs">
                        <span class="text-grey-7">Venc: <strong>{{ contrato.expiracion_corta || contrato.fch_vencimiento }}</strong></span>
                        <q-badge
                          :color="contrato.is_itm ? 'positive' : 'grey-5'"
                          text-color="white"
                          class="text-caption"
                        >
                          {{ contrato.is_itm ? 'ITM' : 'OTM' }} · {{ formatear_dias_expiracion(contrato) }}
                        </q-badge>
                      </div>
                      <div class="row items-center justify-between text-caption q-px-xs q-mt-xs">
                        <span class="text-grey-6">Last: <strong class="text-dark">${{ formatear_numero(contrato.last) }}</strong></span>
                        <span class="text-grey-6">Δ: <strong class="text-dark">{{ calcular_delta(contrato) }}</strong></span>
                      </div>
                    </div>

                    <!-- Footer Resumido: Posición Long/Short, Cantidad y Flujo -->
                    <div class="bg-grey-1 q-pa-xs rounded-borders-bottom">
                      <div class="row items-center justify-between no-wrap q-gutter-xs">
                        <!-- TOGGLE LONG (AZUL) / SHORT (ROJO) -->
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

                        <!-- Flujo Estimado -->
                        <div class="text-caption text-weight-bolder" :class="contrato.posicion === 'LONG' ? 'text-blue-10' : 'text-red-9'">
                          {{ contrato.posicion === 'LONG' ? '-$' : '+$' }}{{ calcular_prima_total(contrato) }}
                        </div>
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
                      class="q-py-xs q-px-sm row items-center justify-between"
                      :class="contrato.tipo === 'CALL' ? 'bg-blue-1 text-blue-10' : 'bg-purple-1 text-purple-10'"
                    >
                      <div class="row items-center no-wrap">
                        <q-icon
                          :name="contrato.tipo === 'CALL' ? 'call_made' : 'call_received'"
                          size="18px"
                          class="q-mr-xs"
                        />
                        <q-badge
                          :color="contrato.tipo === 'CALL' ? 'blue-10' : 'purple-10'"
                          text-color="white"
                          class="text-weight-bolder text-caption"
                        >
                          {{ contrato.tipo }}
                        </q-badge>
                        <!-- BADGE LONG / SHORT (AZUL / ROJO) -->
                        <q-badge
                          :color="contrato.posicion === 'LONG' ? 'blue-10' : 'red-9'"
                          text-color="white"
                          class="text-weight-bolder text-caption q-ml-xs"
                        >
                          {{ contrato.posicion }}
                        </q-badge>
                        <span class="text-caption text-weight-bold q-ml-xs">
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
                        <q-badge
                          :color="contrato.is_itm ? 'positive' : 'grey-6'"
                          text-color="white"
                          class="text-caption text-weight-bold"
                        >
                          {{ contrato.is_itm ? 'ITM' : 'OTM' }}
                        </q-badge>
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
                          <div class="text-weight-bolder text-primary">${{ formatear_numero(contrato.last) }}</div>
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

            <!-- SUB-SECCIÓN 3: SIMULADOR DE PAYOFF DE ESTA ESTRATEGIA -->
            <div v-if="estrategia.contratos.length > 0" class="q-mt-sm">
              <q-expansion-item
                dense
                dense-toggle
                header-class="text-weight-bold text-caption text-blue-10 bg-blue-1 rounded-borders"
                icon="show_chart"
                label="Simulador de Payoff a Expiración para este Grupo"
              >
                <q-card flat bordered class="q-pa-sm q-mt-xs bg-white">
                  <div class="row items-center q-col-gutter-md">
                    <!-- Slider interactivo de precio -->
                    <div class="col-12 col-md-7">
                      <div class="row items-center justify-between text-caption text-grey-8 q-mb-xs">
                        <span>Precio proyectado del subyacente: <strong class="text-primary text-subtitle2">${{ (estrategia.precio_simulado || cotizacion.imp_cierre).toFixed(2) }}</strong></span>
                        <span>Variación: <strong :class="calcular_variacion_precio_simulado(estrategia) >= 0 ? 'text-positive' : 'text-negative'">{{ calcular_variacion_precio_simulado(estrategia) >= 0 ? '+' : '' }}{{ calcular_variacion_precio_simulado(estrategia).toFixed(2) }}%</strong></span>
                      </div>
                      <q-slider
                        v-model="estrategia.precio_simulado"
                        :min="rango_precio_simulado.min"
                        :max="rango_precio_simulado.max"
                        :step="0.5"
                        label
                        color="blue-10"
                      />
                      <div class="row justify-between text-caption text-grey-6">
                        <span>Min: ${{ rango_precio_simulado.min.toFixed(2) }}</span>
                        <span class="text-weight-bold text-dark">Actual: ${{ cotizacion.imp_cierre.toFixed(2) }}</span>
                        <span>Max: ${{ rango_precio_simulado.max.toFixed(2) }}</span>
                      </div>
                    </div>

                    <!-- Resultado Proyectado -->
                    <div class="col-12 col-md-5">
                      <q-card flat bordered class="q-pa-sm text-center" :class="calcular_pnl(estrategia) >= 0 ? 'bg-green-1' : 'bg-red-1'">
                        <div class="text-caption text-grey-8">Ganancia / Pérdida Proyectada (P&L):</div>
                        <div class="text-h6 text-weight-bolder" :class="calcular_pnl(estrategia) >= 0 ? 'text-positive' : 'text-negative'">
                          {{ calcular_pnl(estrategia) >= 0 ? '+$' : '-$' }}{{ Math.abs(calcular_pnl(estrategia)).toFixed(2) }}
                        </div>
                        <div class="text-caption text-grey-7">
                          Retorno (ROI):
                          <strong :class="calcular_roi(estrategia) >= 0 ? 'text-positive' : 'text-negative'">
                            {{ calcular_roi(estrategia) >= 0 ? '+' : '' }}{{ calcular_roi(estrategia).toFixed(1) }}%
                          </strong>
                        </div>
                      </q-card>
                    </div>
                  </div>
                </q-card>
              </q-expansion-item>
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
      @confirmar="on_confirmar_asistente"
    />

  </div>
</template>

<script>
import WinAsistenteSeleccionOpciones from "./WinAsistenteSeleccionOpciones.vue"
import Cotizacion from "@/api/cotizacion.js"
import VariacionSemanal from "@/api/variacion-semanal.js"
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

      // Instrumento financiero actualmente seleccionado
      instrumento: null,

      // Valores de cotización del instrumento
      cotizacion: {
        imp_cierre_anterior: 0,
        imp_apertura: 0,
        imp_maximo: 0,
        imp_minimo: 0,
        imp_cierre: 0,
        imp_variacion: 0,
        pct_variacion: 0
      },
      cargando_cotizacion: false,

      // Opciones de plantillas de estrategias
      estrategias_disponibles: [
        {
          label: "Personalizada (Custom)",
          value: "CUSTOM",
          icon: "tune",
          tipo_badge: "NEUTRAL",
          descripcion: "Combine libremente opciones CALL y PUT en posiciones Long o Short"
        },
        {
          label: "Bull Call Spread (Vertical)",
          value: "BULL_CALL_SPREAD",
          icon: "trending_up",
          tipo_badge: "BULLISH",
          descripcion: "Comprar Call ATM y Vender Call OTM con misma expiración"
        },
        {
          label: "Bear Put Spread (Vertical)",
          value: "BEAR_PUT_SPREAD",
          icon: "trending_down",
          tipo_badge: "BEARISH",
          descripcion: "Comprar Put ATM y Vender Put OTM con misma expiración"
        },
        {
          label: "Iron Condor",
          value: "IRON_CONDOR",
          icon: "compress",
          tipo_badge: "NEUTRAL",
          descripcion: "Estrategia no direccional de 4 patas: Bull Put Spread + Bear Call Spread"
        },
        {
          label: "Covered Call (Venta cubierta)",
          value: "COVERED_CALL",
          icon: "shield",
          tipo_badge: "BULLISH",
          descripcion: "Posición Long Stock + Venta de Call OTM para generar ingresos"
        },
        {
          label: "Bull Put Spread (Crédito)",
          value: "BULL_PUT_SPREAD",
          icon: "arrow_upward",
          tipo_badge: "BULLISH",
          descripcion: "Vender Put OTM y Comprar Put más OTM para proteger"
        },
        {
          label: "Bear Call Spread (Crédito)",
          value: "BEAR_CALL_SPREAD",
          icon: "arrow_downward",
          tipo_badge: "BEARISH",
          descripcion: "Vender Call OTM y Comprar Call más OTM para proteger"
        },
        {
          label: "Long Straddle",
          value: "LONG_STRADDLE",
          icon: "expand",
          tipo_badge: "VOLATILIDAD",
          descripcion: "Comprar Call y Put en el mismo Strike para alta volatilidad"
        },
        {
          label: "Long Strangle",
          value: "LONG_STRANGLE",
          icon: "unfold_more",
          tipo_badge: "VOLATILIDAD",
          descripcion: "Comprar Call OTM y Put OTM buscando gran movimiento"
        }
      ],

      // LISTA DE GRUPOS DE ESTRATEGIAS (Grupo 1: Estrategia 1, Grupo 2: Estrategia 2, etc.)
      estrategias: []
    }
  },
  computed: {
    rango_precio_simulado() {
      const base = this.cotizacion.imp_cierre || 100
      return {
        min: Number((base * 0.8).toFixed(2)),
        max: Number((base * 1.2).toFixed(2))
      }
    },
    todos_los_grupos_expandidos() {
      if (this.estrategias.length === 0) return false
      return this.estrategias.every(e => e.expandida)
    }
  },
  created() {
    // Si no hay instrumento, preconfiguramos un estado amigable
    this.inicializar_grupos_demo("SPY")
  },
  methods: {
    inicializar_grupos_demo(symbol) {
      if (!this.instrumento) {
        this.instrumento = {
          symbol: symbol || "SPY",
          name: "SPDR S&P 500 ETF Trust",
          asset_type: "ETF"
        }
        this.cargar_cotizacion(this.instrumento.symbol)
      }

      const basePrice = this.cotizacion.imp_cierre || 582.40

      // Grupo 1: Estrategia 1 (Bull Call Spread)
      const e1 = {
        id: 1,
        nombre: "Estrategia 1",
        tipo: "BULL_CALL_SPREAD",
        expandida: true,
        vista_cards: "expandida",
        contratos: [],
        precio_simulado: basePrice
      }

      // Grupo 2: Estrategia 2 (Iron Condor)
      const e2 = {
        id: 2,
        nombre: "Estrategia 2",
        tipo: "IRON_CONDOR",
        expandida: true,
        vista_cards: "resumida",
        contratos: [],
        precio_simulado: basePrice
      }

      this.estrategias = [e1, e2]
      this.aplicar_plantilla(e1, "BULL_CALL_SPREAD")
      this.aplicar_plantilla(e2, "IRON_CONDOR")
    },
    abrir_asistente_nuevo_instrumento() {
      this.asistenteInstrumentoInicial = null
      this.asistenteContratosIniciales = []
      this.asistenteEstrategiaId = null
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
            return
          }
        }

        // Si se abrió desde el botón global de nuevo instrumento
        if (this.estrategias.length > 0) {
          this.estrategias[0].contratos = nuevosContratos
        } else {
          this.agregar_nueva_estrategia_con_contratos("Estrategia 1", "CUSTOM", nuevosContratos)
        }
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
        precio_simulado: this.cotizacion.imp_cierre || 100
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
        precio_simulado: this.cotizacion.imp_cierre || 100
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
        precio_simulado: estrategia.precio_simulado || this.cotizacion.imp_cierre
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
    aplicar_plantilla(estrategia, tipoEstrategia) {
      if (!this.instrumento) return
      const basePrice = this.cotizacion.imp_cierre || 100
      const expDate = moment().add(30, "days").format("YYYY-MM-DD")
      const expShort = moment().add(30, "days").format("DD MMM")
      const sym = this.instrumento.symbol

      if (tipoEstrategia === "BULL_CALL_SPREAD") {
        const s1 = Math.round(basePrice)
        const s2 = Math.round(basePrice * 1.05)
        estrategia.contratos = [
          {
            cod_symbol: `${sym}${moment(expDate).format("YYMMDD")}C${String(s1 * 1000).padStart(8, "0")}`,
            tipo: "CALL",
            strike: s1,
            fch_vencimiento: expDate,
            expiracion_corta: expShort,
            bid: 3.20,
            ask: 3.40,
            last: 3.30,
            posicion: "LONG",
            cantidad: 1,
            is_itm: true,
            delta: "+0.65",
            theta: "-0.04"
          },
          {
            cod_symbol: `${sym}${moment(expDate).format("YYMMDD")}C${String(s2 * 1000).padStart(8, "0")}`,
            tipo: "CALL",
            strike: s2,
            fch_vencimiento: expDate,
            expiracion_corta: expShort,
            bid: 1.10,
            ask: 1.25,
            last: 1.18,
            posicion: "SHORT",
            cantidad: 1,
            is_itm: false,
            delta: "+0.32",
            theta: "-0.03"
          }
        ]
      } else if (tipoEstrategia === "BEAR_PUT_SPREAD") {
        const s1 = Math.round(basePrice)
        const s2 = Math.round(basePrice * 0.95)
        estrategia.contratos = [
          {
            cod_symbol: `${sym}${moment(expDate).format("YYMMDD")}P${String(s1 * 1000).padStart(8, "0")}`,
            tipo: "PUT",
            strike: s1,
            fch_vencimiento: expDate,
            expiracion_corta: expShort,
            bid: 3.10,
            ask: 3.30,
            last: 3.20,
            posicion: "LONG",
            cantidad: 1,
            is_itm: false,
            delta: "-0.48",
            theta: "-0.04"
          },
          {
            cod_symbol: `${sym}${moment(expDate).format("YYMMDD")}P${String(s2 * 1000).padStart(8, "0")}`,
            tipo: "PUT",
            strike: s2,
            fch_vencimiento: expDate,
            expiracion_corta: expShort,
            bid: 1.05,
            ask: 1.20,
            last: 1.15,
            posicion: "SHORT",
            cantidad: 1,
            is_itm: false,
            delta: "-0.24",
            theta: "-0.02"
          }
        ]
      } else if (tipoEstrategia === "IRON_CONDOR") {
        const sPutBuy = Math.round(basePrice * 0.90)
        const sPutSell = Math.round(basePrice * 0.95)
        const sCallSell = Math.round(basePrice * 1.05)
        const sCallBuy = Math.round(basePrice * 1.10)
        estrategia.contratos = [
          {
            cod_symbol: `${sym}${moment(expDate).format("YYMMDD")}P${String(sPutBuy * 1000).padStart(8, "0")}`,
            tipo: "PUT",
            strike: sPutBuy,
            fch_vencimiento: expDate,
            expiracion_corta: expShort,
            bid: 0.60,
            ask: 0.70,
            last: 0.65,
            posicion: "LONG",
            cantidad: 1,
            is_itm: false,
            delta: "-0.15",
            theta: "-0.02"
          },
          {
            cod_symbol: `${sym}${moment(expDate).format("YYMMDD")}P${String(sPutSell * 1000).padStart(8, "0")}`,
            tipo: "PUT",
            strike: sPutSell,
            fch_vencimiento: expDate,
            expiracion_corta: expShort,
            bid: 1.40,
            ask: 1.55,
            last: 1.48,
            posicion: "SHORT",
            cantidad: 1,
            is_itm: false,
            delta: "-0.30",
            theta: "-0.03"
          },
          {
            cod_symbol: `${sym}${moment(expDate).format("YYMMDD")}C${String(sCallSell * 1000).padStart(8, "0")}`,
            tipo: "CALL",
            strike: sCallSell,
            fch_vencimiento: expDate,
            expiracion_corta: expShort,
            bid: 1.35,
            ask: 1.50,
            last: 1.42,
            posicion: "SHORT",
            cantidad: 1,
            is_itm: false,
            delta: "+0.32",
            theta: "-0.03"
          },
          {
            cod_symbol: `${sym}${moment(expDate).format("YYMMDD")}C${String(sCallBuy * 1000).padStart(8, "0")}`,
            tipo: "CALL",
            strike: sCallBuy,
            fch_vencimiento: expDate,
            expiracion_corta: expShort,
            bid: 0.55,
            ask: 0.65,
            last: 0.60,
            posicion: "LONG",
            cantidad: 1,
            is_itm: false,
            delta: "+0.16",
            theta: "-0.02"
          }
        ]
      } else if (tipoEstrategia === "COVERED_CALL") {
        const s = Math.round(basePrice * 1.05)
        estrategia.contratos = [
          {
            cod_symbol: `${sym}${moment(expDate).format("YYMMDD")}C${String(s * 1000).padStart(8, "0")}`,
            tipo: "CALL",
            strike: s,
            fch_vencimiento: expDate,
            expiracion_corta: expShort,
            bid: 2.10,
            ask: 2.25,
            last: 2.18,
            posicion: "SHORT",
            cantidad: 1,
            is_itm: false,
            delta: "+0.38",
            theta: "-0.04"
          }
        ]
      } else if (tipoEstrategia === "LONG_STRADDLE") {
        const s = Math.round(basePrice)
        estrategia.contratos = [
          {
            cod_symbol: `${sym}${moment(expDate).format("YYMMDD")}C${String(s * 1000).padStart(8, "0")}`,
            tipo: "CALL",
            strike: s,
            fch_vencimiento: expDate,
            expiracion_corta: expShort,
            bid: 4.10,
            ask: 4.30,
            last: 4.20,
            posicion: "LONG",
            cantidad: 1,
            is_itm: true,
            delta: "+0.55",
            theta: "-0.05"
          },
          {
            cod_symbol: `${sym}${moment(expDate).format("YYMMDD")}P${String(s * 1000).padStart(8, "0")}`,
            tipo: "PUT",
            strike: s,
            fch_vencimiento: expDate,
            expiracion_corta: expShort,
            bid: 3.90,
            ask: 4.10,
            last: 4.00,
            posicion: "LONG",
            cantidad: 1,
            is_itm: false,
            delta: "-0.45",
            theta: "-0.05"
          }
        ]
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
        const precio = Number(c.last || c.ask || c.bid || 1.5)
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
    calcular_pnl(estrategia) {
      if (!estrategia || !Array.isArray(estrategia.contratos) || estrategia.contratos.length === 0) return 0
      const precioProj = estrategia.precio_simulado || this.cotizacion.imp_cierre || 100
      let totalPnl = 0

      estrategia.contratos.forEach(c => {
        const strike = Number(c.strike || 0)
        const premium = Number(c.last || c.ask || c.bid || 1.5)
        const cantidad = Number(c.cantidad || 1)
        const factor = c.posicion === "LONG" ? 1 : -1

        let valorIntrinseco = 0
        if (c.tipo === "CALL") {
          valorIntrinseco = Math.max(0, precioProj - strike)
        } else {
          valorIntrinseco = Math.max(0, strike - precioProj)
        }

        const payoffPorAccion = factor * (valorIntrinseco - premium)
        totalPnl += payoffPorAccion * 100 * cantidad
      })

      return Number(totalPnl.toFixed(2))
    },
    calcular_roi(estrategia) {
      const metricas = this.calcular_metricas(estrategia)
      const costo = Math.abs(metricas.debito_neto)
      if (!costo || costo === 0) return 0
      return (this.calcular_pnl(estrategia) / costo) * 100
    },
    calcular_variacion_precio_simulado(estrategia) {
      const base = this.cotizacion.imp_cierre
      if (!base) return 0
      const proj = estrategia.precio_simulado || base
      return ((proj - base) / base) * 100
    },
    calcular_prima_total(contrato) {
      const precio = Number(contrato.last || contrato.ask || contrato.bid || 0)
      const cant = Number(contrato.cantidad || 1)
      return (precio * 100 * cant).toFixed(2)
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
    obtener_badge_tipo_color(tipo) {
      const map = {
        BULL_CALL_SPREAD: "positive",
        BULL_PUT_SPREAD: "positive",
        COVERED_CALL: "positive",
        BEAR_PUT_SPREAD: "negative",
        BEAR_CALL_SPREAD: "negative",
        IRON_CONDOR: "primary",
        LONG_STRADDLE: "amber-9",
        LONG_STRANGLE: "amber-9",
        CUSTOM: "grey-8"
      }
      return map[tipo] || "primary"
    },
    obtener_badge_tipo_label(tipo) {
      const opt = this.estrategias_disponibles.find(o => o.value === tipo)
      return opt ? opt.tipo_badge : "ESTRATEGIA"
    },
    formatear_numero(val) {
      if (val === null || val === undefined || isNaN(Number(val))) return "0.00"
      return Number(val).toFixed(2)
    },
    cargar_cotizacion(symbol) {
      if (!symbol) return
      this.cargando_cotizacion = true

      Cotizacion.get_cotizacion(symbol)
        .then(data => {
          if (data) {
            const cierre = data.imp_cierre || data.last || 0
            const cierreAnt = data.imp_cierre_anterior || (cierre ? cierre * 0.99 : 0)
            const variacion = data.imp_variacion !== undefined ? data.imp_variacion : (cierre - cierreAnt)
            const pct = data.pct_variacion !== undefined ? data.pct_variacion : (cierreAnt ? (variacion / cierreAnt) * 100 : 0)

            this.cotizacion.imp_cierre = cierre
            this.cotizacion.imp_cierre_anterior = cierreAnt
            this.cotizacion.imp_variacion = variacion
            this.cotizacion.pct_variacion = pct
            this.cotizacion.imp_apertura = data.imp_apertura || cierreAnt
            this.cotizacion.imp_maximo = data.imp_maximo || Math.max(cierre, cierreAnt) * 1.01
            this.cotizacion.imp_minimo = data.imp_minimo || Math.min(cierre, cierreAnt) * 0.99

            this.estrategias.forEach(e => {
              if (!e.precio_simulado) e.precio_simulado = cierre
            })
          } else {
            this.asignar_cotizacion_estimada(symbol)
          }
        })
        .catch(err => {
          console.debug("No se pudo obtener cotización remota, usando estimación local:", err)
          this.asignar_cotizacion_estimada(symbol)
        })
        .finally(() => {
          this.consultar_variacion_semanal(symbol)
          this.cargando_cotizacion = false
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
                if (!e.precio_simulado) e.precio_simulado = d.imp_cierre
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
    asignar_cotizacion_estimada(symbol) {
      let base = 225.50
      if (symbol === "SPY") base = 582.40
      else if (symbol === "QQQ") base = 492.80
      else if (symbol === "NVDA") base = 141.20
      else if (symbol === "TSLA") base = 255.60
      else if (symbol === "MSFT") base = 428.10
      else if (symbol === "SPX") base = 5864.20

      const prev = Number((base * 0.992).toFixed(2))
      const diff = Number((base - prev).toFixed(2))
      const pct = Number(((diff / prev) * 100).toFixed(2))

      this.cotizacion = {
        imp_cierre_anterior: prev,
        imp_apertura: Number((prev * 1.003).toFixed(2)),
        imp_maximo: Number((base * 1.008).toFixed(2)),
        imp_minimo: Number((prev * 0.997).toFixed(2)),
        imp_cierre: base,
        imp_variacion: diff,
        pct_variacion: pct
      }

      this.estrategias.forEach(e => {
        if (!e.precio_simulado) e.precio_simulado = base
      })
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
  border-left: 4px solid #0d47a1;
}

.grupo-estrategia-card {
  border-left: 4px solid #1976d2;
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
}

.pata-card-resumida:hover {
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
}

.font-mono {
  font-family: monospace;
}

.border-dashed {
  border: 2px dashed #cfd8dc;
}
</style>
