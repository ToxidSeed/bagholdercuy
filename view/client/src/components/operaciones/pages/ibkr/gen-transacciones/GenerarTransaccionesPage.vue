<template>
  <div>    
    <q-card flat>
      <q-card-section class="text-primary text-h5">
        Generar Transacciones
      </q-card-section>
    </q-card>    
    <q-separator />
    <q-splitter v-model="splitterModel" style="height: 85vh;">
      <template v-slot:before>
        <q-card flat>      
          <q-card-section>
            <span class="text-subtitle1 text-primary text-bold">Datos Generales</span>
          </q-card-section>
          <q-card-section class="row">
            <q-btn color="primary" label="Generar Transacciones" no-caps @click="generarTransacciones" flat icon="play_arrow" dense />
            <div class="col-9">
                <div class="q-gutter-sm q-pb-md">
                  <q-radio v-model="opcionProcesamiento" val="todos" label="Procesar Todos" />
                  <q-radio v-model="opcionProcesamiento" val="seleccion" label="Procesar Seleccion" />
                </div>
            </div>                        
          </q-card-section>
        </q-card>
        <q-separator />
        <q-card flat>
          <q-card-section>
            <div class="row">
              <span class="text-subtitle1 text-primary text-bold">Filtros</span>
              <q-space />
              <q-btn color="primary" flat round icon="expand_less" @click="limpiarFiltros" />
            </div>
            <q-btn color="primary" flat icon="filter_alt" dense  label="Filtrar" no-caps @click="filtrarResultados"/>            
            <div>
              <div>
                <q-input v-model="filtroSimbolo" label="Símbolo" />
              </div>
              <div>
                <q-input v-model="filtroFechaHora" label="Fecha y hora de operación" />              
              </div>
            </div>            
          </q-card-section>
        </q-card>
      </template>
      <template v-slot:after>
        <q-table
          flat      
          dense
          separator="vertical"        
          :data="rows"
          :columns="columns"
          row-key="id_operacion_importada"
          :selected.sync="selected"
          selection="multiple"
          :loading="loading"
          :pagination.sync="pagination"
          table-header-class="bg-grey-2"
        >
        <template v-slot:top>
          <div class="column full-width">
            <div class="row items-center">
              <q-icon name="table_rows" size="sm" class="q-mr-sm" color="purple-3"/>
              <span class="text-subtitle1">Operaciones Importadas IBKR</span>          
            </div>
            <div class="text-caption">
              ÚLTIMA ACTUALIZACIÓN: {{ fechaActualizacion }}
            </div>
          </div>
        </template>
        <!-- Columna de checkbox personalizada (primera columna) -->
        <template v-slot:header-selection="scope">
          <q-checkbox v-model="scope.selected" />
        </template>

        <template v-slot:body-selection="scope">
          <q-checkbox
          dense
            v-model="scope.selected"
            :val="scope.row"
          />
        </template>
      </q-table>
    </template>
    </q-splitter>    
  </div>
</template>

<script>
import Operacion from '@/api/operacion'

export default {
  name: 'GenerarTransaccionesPage',

  data () {
    return {
      opcionProcesamiento: 'todos',
      filtroSimbolo: '',
      filtroFechaHora: '',
      loading: false,
      splitterModel: 30,
      selected: [],
      pagination: {
        rowsPerPage: 20
      },
      columns: [
        {
          name: 'id_operacion_importada',
          label: 'ID',
          field: 'id_operacion_importada',
          align: 'left',
          sortable: true
        },
        {
          name: 'id_importacion',
          label: 'ID Importación',
          field: 'id_importacion',
          align: 'left',
          sortable: true
        },
        {
          name: 'categoria_activo',
          label: 'Categoría Activo',
          field: 'categoria_activo',
          align: 'left',
          sortable: true
        },
        {
          name: 'cod_moneda',
          label: 'Moneda',
          field: 'cod_moneda',
          align: 'left',
          sortable: true
        },
        {
          name: 'cod_symbol',
          label: 'Símbolo',
          field: 'cod_symbol',
          align: 'left',
          sortable: true
        },
        {
          name: 'fch_hora_operacion',
          label: 'Fecha/Hora Operación',
          field: 'fch_hora_operacion',
          align: 'left',
          sortable: true
        },
        {
          name: 'cantidad',
          label: 'Cantidad',
          field: 'cantidad',
          align: 'right',
          sortable: true
        },
        {
          name: 'precio_trade',
          label: 'Precio Trade',
          field: 'precio_trade',
          align: 'right',
          sortable: true
        },
        {
          name: 'precio_cierre',
          label: 'Precio Cierre',
          field: 'precio_cierre',
          align: 'right',
          sortable: true
        },
        {
          name: 'importe_bruto',
          label: 'Importe Bruto',
          field: 'importe_bruto',
          align: 'right',
          sortable: true
        },
        {
          name: 'comision',
          label: 'Comisión',
          field: 'comision',
          align: 'right',
          sortable: true
        },
        {
          name: 'base_costo',
          label: 'Base Costo',
          field: 'base_costo',
          align: 'right',
          sortable: true
        },
        {
          name: 'pl_realizado',
          label: 'P/L Realizado',
          field: 'pl_realizado',
          align: 'right',
          sortable: true
        },
        {
          name: 'pl_mtm',
          label: 'P/L MTM',
          field: 'pl_mtm',
          align: 'right',
          sortable: true
        },
        {
          name: 'codigo',
          label: 'Código',
          field: 'codigo',
          align: 'left',
          sortable: true
        },
        {
          name: 'procesado',
          label: 'Procesado',
          field: 'procesado',
          align: 'center',
          sortable: true,
          format: val => val ? 'Sí' : 'No'
        },
        {
          name: 'fch_procesado',
          label: 'Fecha Procesado',
          field: 'fch_procesado',
          align: 'left',
          sortable: true
        },
        {
          name: 'fch_registro',
          label: 'Fecha Registro',
          field: 'fch_registro',
          align: 'left',
          sortable: true
        }, 
        {
          name: 'id_transaccion',
          label: 'ID Transacción',
          field: 'id_transaccion',
          align: 'left',
          sortable: true
        }
      ],
      rows: []
    }
  },

  methods: {
    filtrarResultados () {
      // Implementación del filtrado
      console.log('Filtrar por', this.filtroSimbolo, this.filtroFechaHora)
    },

    async cargarDatos () {
      this.loading = true
      try {
        const id_importacion = this.$route.query.id_importacion
        const httpresp = await Operacion.get_ibkr_import_trades_detail(id_importacion)
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

    async generarTransacciones () {
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

  mounted () {
    this.cargarDatos()
  }
}
</script>
