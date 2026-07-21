<template>
  <div>
    <q-card flat>
      <q-card-section class="text-primary text-h5">
        Generar Transacciones
      </q-card-section>
    </q-card>
    <q-bar class="bg-white">
      <q-btn color="primary" label="Generar Transacciones" @click="generarTransacciones" icon="play_arrow" />
    </q-bar>
    <q-separator />
    <PanelGenerarTransacciones :opcionProcesamiento.sync="opcionProcesamiento" :selected.sync="selected"
      @generar="generarTransacciones" />
    <q-separator />
    <TableOperacionesImportadas :rows="rows" :loading="loading" :fechaActualizacion="fechaActualizacion"
      :selected.sync="selected" :pagination.sync="pagination" />
  </div>
</template>

<script>
import Operacion from '@/api/operacion'
import TableOperacionesImportadas from './generar/TableOperacionesImportadas.vue'
import PanelGenerarTransacciones from './generar/PanelGenerarTransacciones.vue'

export default {
  name: 'GenerarTransaccionesPage',

  components: {
    TableOperacionesImportadas,
    PanelGenerarTransacciones
  },

  data() {
    return {
      fechaActualizacion: '',
      opcionProcesamiento: 'todos',
      filtroSimbolo: '',
      filtroFechaHora: '',
      loading: false,
      splitterModel: 30,
      selected: [],
      pagination: {
        rowsPerPage: 20
      },
      rows: []
    }
  },

  methods: {
    limpiarFiltros() {
      this.filtroSimbolo = ''
      this.filtroFechaHora = ''
      this.filtrarResultados()
    },

    filtrarResultados() {
      // Implementación del filtrado
      //console.log('Filtrar por', this.filtroSimbolo, this.filtroFechaHora)
      const params = {
        id_importacion: this.$route.query.id_importacion,
        cod_symbol: this.filtroSimbolo
      }
      this.cargarDatos(params)
    },

    async cargarDatos(params) {

      this.loading = true
      try {
        const id_importacion = params.id_importacion
        const cod_symbol = params.cod_symbol
        const httpresp = await Operacion.get_ibkr_import_trades_detail(id_importacion, cod_symbol)
        const appresp = httpresp.data
        if (appresp.success) {
          this.rows = appresp.data
        } else {
          this.$q.notify({ type: 'negative', message: appresp.msg || 'Error al cargar las operaciones' })
        }
      } catch (error) {
        this.$q.notify({ type: 'negative', message: 'Error al cargar las operaciones importadas' })
        console.error(error)
      } finally {
        this.loading = false
      }
    },

    async generarTransacciones() {
      this.loading = true
      try {
        const id_importacion = this.$route.query.id_importacion
        let operacionesSeleccionadas = []
        for (const row of this.selected) {
          operacionesSeleccionadas.push(row.id_operacion_importada)
        }

        if (this.opcionProcesamiento == 'todos') {
          operacionesSeleccionadas = []
        }

        const id_cuenta = localStorage.getItem("id_cuenta")

        const httpresp = await Operacion.generar_transacciones(operacionesSeleccionadas, id_importacion, id_cuenta)
        const appresp = httpresp.data
        if (appresp.success) {
          this.$q.notify({ type: 'positive', message: appresp.msg || 'Transacciones generadas exitosamente' })
        } else {
          this.$q.notify({ type: 'negative', message: appresp.msg || 'Error al generar las transacciones' })
        }
      } catch (error) {
        this.$q.notify({ type: 'negative', message: 'Error al generar las transacciones' })
        console.error(error)
      } finally {
        this.loading = false
      }
    }
  },

  mounted() {
    const params = {
      id_importacion: this.$route.query.id_importacion,
      cod_symbol: this.filtroSimbolo
    }
    this.cargarDatos(params)
  }
}
</script>
