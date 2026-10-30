<template>
  <div class="menu-principal-container q-py-sm">
    <q-list dense class="menu-list">

      <!-- Sección General -->
      <div class="menu-section-label">General</div>
      
      <q-item clickable v-ripple active-class="my-menu-link" to="/funds" class="menu-item">
        <q-item-section avatar class="menu-avatar">
          <q-icon name="account_balance" size="18px" />
        </q-item-section>
        <q-item-section>Funds</q-item-section>
      </q-item>

      <q-item clickable v-ripple active-class="my-menu-link" :to="{ name: 'currencyexchange', params: { inFirstPanelSize: 0 } }" class="menu-item">
        <q-item-section avatar class="menu-avatar">
          <q-icon name="currency_exchange" size="18px" />
        </q-item-section>
        <q-item-section>Currency exchange rates</q-item-section>
      </q-item>

      <q-item clickable v-ripple active-class="my-menu-link" to="/watchlist" class="menu-item">
        <q-item-section avatar class="menu-avatar">
          <q-icon name="visibility" size="18px" />
        </q-item-section>
        <q-item-section>Watchlist</q-item-section>
      </q-item>

      <q-separator class="q-my-sm menu-separator" />

      <!-- Holdings -->
      <q-expansion-item 
        expand-separator 
        default-opened 
        header-class="menu-header" 
        icon="account_balance_wallet"
        label="Holdings" 
        dense
      >
        <q-list dense class="submenu-list">
          <q-item clickable v-ripple active-class="my-menu-link" to="/holdings" class="menu-item">
            <q-item-section avatar class="menu-avatar">
              <q-icon name="pie_chart" size="16px" />
            </q-item-section>
            <q-item-section>Posiciones</q-item-section>
          </q-item>

          <q-item clickable v-ripple active-class="my-menu-link" to="/reprocesarposiciones" class="menu-item">
            <q-item-section avatar class="menu-avatar">
              <q-icon name="sync" size="16px" />
            </q-item-section>
            <q-item-section>Reprocesar Posiciones</q-item-section>
          </q-item>

          <q-item clickable v-ripple active-class="my-menu-link" to="/reorganizarorden" class="menu-item">
            <q-item-section avatar class="menu-avatar">
              <q-icon name="low_priority" size="16px" />
            </q-item-section>
            <q-item-section>Reorganizar</q-item-section>
          </q-item>
        </q-list>
      </q-expansion-item>

      <!-- Carga de Operaciones -->
      <q-expansion-item 
        expand-separator 
        default-opened 
        header-class="menu-header" 
        icon="cloud_upload"
        label="Carga de Operaciones" 
        dense
      >
        <q-list dense class="submenu-list">
          <q-item clickable v-ripple active-class="my-menu-link" to="/carga-operaciones/ibkr" class="menu-item">
            <q-item-section avatar class="menu-avatar">
              <q-icon name="file_upload" size="16px" />
            </q-item-section>
            <q-item-section>Interactive Brokers</q-item-section>
          </q-item>

          <q-item clickable v-ripple active-class="my-menu-link" to="/hapi-trades" class="menu-item">
            <q-item-section avatar class="menu-avatar">
              <q-icon name="bolt" size="16px" />
            </q-item-section>
            <q-item-section>HAPI</q-item-section>
          </q-item>

          <q-item clickable v-ripple active-class="my-menu-link" to="/sura-trades" class="menu-item">
            <q-item-section avatar class="menu-avatar">
              <q-icon name="apartment" size="16px" />
            </q-item-section>
            <q-item-section>SURA</q-item-section>
          </q-item>
        </q-list>
      </q-expansion-item>

      <!-- Simulación -->
      <q-expansion-item 
        expand-separator 
        default-opened 
        header-class="menu-header" 
        icon="science"
        label="Simulación" 
        dense
      >
        <q-list dense class="submenu-list">
          <q-item clickable v-ripple active-class="my-menu-link" to="/simulacion-rentabilidad" class="menu-item">
            <q-item-section avatar class="menu-avatar">
              <q-icon name="trending_up" size="16px" />
            </q-item-section>
            <q-item-section>Rentabilidad</q-item-section>
          </q-item>
        </q-list>
      </q-expansion-item>

      <!-- Informes -->
      <q-expansion-item 
        expand-separator 
        default-opened 
        header-class="menu-header" 
        icon="insights"
        label="Informes" 
        dense
      >
        <q-list dense class="submenu-list">
          <q-item clickable v-ripple active-class="my-menu-link" to="/variacionmensual" class="menu-item">
            <q-item-section avatar class="menu-avatar">
              <q-icon name="calendar_month" size="16px" />
            </q-item-section>
            <q-item-section>Analítica Mensual</q-item-section>
          </q-item>

          <q-item clickable v-ripple active-class="my-menu-link" to="/variacionsemanal" class="menu-item">
            <q-item-section avatar class="menu-avatar">
              <q-icon name="view_week" size="16px" />
            </q-item-section>
            <q-item-section>Analítica Semanal</q-item-section>
          </q-item>

          <q-item clickable v-ripple active-class="my-menu-link" to="/variaciondiaria" class="menu-item">
            <q-item-section avatar class="menu-avatar">
              <q-icon name="today" size="16px" />
            </q-item-section>
            <q-item-section>Analítica Diaria</q-item-section>
          </q-item>

          <q-item clickable v-ripple active-class="my-menu-link" to="/rentabilidadoperaciones" class="menu-item">
            <q-item-section avatar class="menu-avatar">
              <q-icon name="calculate" size="16px" />
            </q-item-section>
            <q-item-section>Rentabilidad Operaciones</q-item-section>
          </q-item>

          <q-item clickable v-ripple active-class="my-menu-link" to="/stats" class="menu-item">
            <q-item-section avatar class="menu-avatar">
              <q-icon name="bar_chart" size="16px" />
            </q-item-section>
            <q-item-section>Stats</q-item-section>
          </q-item>

          <q-item clickable v-ripple active-class="my-menu-link" to="/metricas" class="menu-item">
            <q-item-section avatar class="menu-avatar">
              <q-icon name="speed" size="16px" />
            </q-item-section>
            <q-item-section>Métricas</q-item-section>
          </q-item>

          <q-item clickable v-ripple active-class="my-menu-link" to="/ciclos" class="menu-item">
            <q-item-section avatar class="menu-avatar">
              <q-icon name="cyclone" size="16px" />
            </q-item-section>
            <q-item-section>Ciclos</q-item-section>
          </q-item>
        </q-list>
      </q-expansion-item>

      <q-separator class="q-my-sm menu-separator" />

      <!-- Configuración -->
      <q-expansion-item 
        expand-separator 
        default-opened 
        header-class="menu-header" 
        icon="settings"
        label="Configuración" 
        dense
      >
        <q-list dense class="submenu-list">
          <q-item clickable v-ripple active-class="my-menu-link" to="/dataloader" class="menu-item">
            <q-item-section avatar class="menu-avatar"><q-icon name="cloud_sync" size="16px" /></q-item-section>
            <q-item-section>Data Loader</q-item-section>
          </q-item>
          <q-item clickable v-ripple active-class="my-menu-link" to="/series" class="menu-item">
            <q-item-section avatar class="menu-avatar"><q-icon name="timeline" size="16px" /></q-item-section>
            <q-item-section>Series</q-item-section>
          </q-item>
          <q-item clickable v-ripple active-class="my-menu-link" to="/currency" class="menu-item">
            <q-item-section avatar class="menu-avatar"><q-icon name="paid" size="16px" /></q-item-section>
            <q-item-section>Currency</q-item-section>
          </q-item>
          <q-item clickable v-ripple active-class="my-menu-link" to="/symbols" class="menu-item">
            <q-item-section avatar class="menu-avatar"><q-icon name="tag" size="16px" /></q-item-section>
            <q-item-section>Symbols</q-item-section>
          </q-item>
          <q-item clickable v-ripple active-class="my-menu-link" :to="{ name: 'opciones' }" class="menu-item">
            <q-item-section avatar class="menu-avatar"><q-icon name="tune" size="16px" /></q-item-section>
            <q-item-section>Opciones</q-item-section>
          </q-item>
          <q-item clickable v-ripple active-class="my-menu-link" :to="{ name: 'calendario-semanal-loader' }" class="menu-item">
            <q-item-section avatar class="menu-avatar"><q-icon name="event_repeat" size="16px" /></q-item-section>
            <q-item-section>Calendario Semanal</q-item-section>
          </q-item>
          <q-item clickable v-ripple active-class="my-menu-link" :to="{ name: 'calendario-diario-loader' }" class="menu-item">
            <q-item-section avatar class="menu-avatar"><q-icon name="calendar_today" size="16px" /></q-item-section>
            <q-item-section>Calendario Diario</q-item-section>
          </q-item>
          <q-item clickable v-ripple active-class="my-menu-link" :to="{ name: 'broker' }" class="menu-item">
            <q-item-section avatar class="menu-avatar"><q-icon name="storefront" size="16px" /></q-item-section>
            <q-item-section>Broker</q-item-section>
          </q-item>
          <q-item clickable v-ripple active-class="my-menu-link" :to="{ name: 'cuenta' }" class="menu-item">
            <q-item-section avatar class="menu-avatar"><q-icon name="manage_accounts" size="16px" /></q-item-section>
            <q-item-section>Cuenta</q-item-section>
          </q-item>
          <q-item clickable v-ripple active-class="my-menu-link" :to="{ name: 'usuario' }" class="menu-item">
            <q-item-section avatar class="menu-avatar"><q-icon name="person" size="16px" /></q-item-section>
            <q-item-section>Usuario</q-item-section>
          </q-item>
          <q-item clickable v-ripple active-class="my-menu-link" :to="{ name: 'stocksplit' }" class="menu-item">
            <q-item-section avatar class="menu-avatar"><q-icon name="call_split" size="16px" /></q-item-section>
            <q-item-section>Stock Split</q-item-section>
          </q-item>
          <q-item clickable v-ripple active-class="my-menu-link" :to="{ name: 'ibkr' }" class="menu-item">
            <q-item-section avatar class="menu-avatar"><q-icon name="integration_instructions" size="16px" /></q-item-section>
            <q-item-section>Interactive Brokers</q-item-section>
          </q-item>
        </q-list>
      </q-expansion-item>

    </q-list>
  </div>
</template>

<script>
export default {
  name: "MenuPrincipal",
  data: () => {
    return {}
  }
}
</script>

<style lang="scss">
.menu-principal-container {
  font-size: 13px;
  color: #374151;

  .menu-section-label {
    padding: 6px 16px 4px;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #9ca3af;
  }

  .menu-separator {
    background-color: #f3f4f6;
    margin-left: 12px;
    margin-right: 12px;
  }

  /* Ítems generales */
  .menu-item {
    border-radius: 8px;
    margin: 2px 10px;
    padding: 6px 12px;
    min-height: 36px;
    transition: all 0.18s ease-in-out;
    color: #4b5563;

    &:hover {
      background-color: #f3f4f6;
      color: #111827;
    }
  }

  /* Encabezados de grupo/acordeón */
  .menu-header {
    border-radius: 8px;
    margin: 2px 10px;
    padding: 6px 12px;
    min-height: 38px;
    font-weight: 600;
    color: #1f2937;
    transition: background-color 0.18s ease;

    &:hover {
      background-color: #f8fafc;
    }

    .q-item__section--avatar {
      min-width: 30px;
      padding-right: 8px;
      color: #0d47a1;
    }
  }

  .submenu-list {
    padding-left: 6px;
  }

  .menu-avatar {
    min-width: 28px;
    padding-right: 8px;
    color: #6b7280;
  }

  /* Estado ACTIVO */
  .my-menu-link {
    background: rgba(13, 71, 161, 0.08) !important;
    color: #0d47a1 !important;
    font-weight: 600 !important;
    position: relative;

    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 6px;
      bottom: 6px;
      width: 3.5px;
      border-radius: 4px;
      background-color: #0d47a1;
    }

    .menu-avatar,
    .q-icon {
      color: #0d47a1 !important;
    }
  }
}
</style>