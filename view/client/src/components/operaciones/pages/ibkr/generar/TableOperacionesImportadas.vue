<template>
    <q-table flat dense separator="vertical" :data="rows" :columns="columns" row-key="id_operacion_importada"
        :selected.sync="localSelected" selection="multiple" :loading="loading" :pagination.sync="localPagination"
        table-header-class="bg-grey-2" :filter="filter">
        <template v-slot:top>
            <!--
            <div class="column full-width">
                <div class="row items-center">
                    <q-icon name="table_rows" size="sm" class="q-mr-sm" color="purple-3" />
                    <span class="text-subtitle1">Operaciones Importadas IBKR</span>
                </div>
                <div class="text-caption">
                    ÚLTIMA ACTUALIZACIÓN: {{ fechaActualizacion }}
                </div>
            </div>
            -->
            <div class="row full-width justify-center">
                <div class="col-6">
                    <q-input outlined dense debounce="300" v-model="filter" placeholder="Buscar">
                        <template v-slot:append>
                            <q-icon name="search" />
                        </template>
                    </q-input>
                </div>
            </div>
        </template>
        <!-- Columna de checkbox personalizada (primera columna) -->
        <template v-slot:header-selection="scope">
            <q-checkbox dense v-model="scope.selected" />
        </template>

        <template v-slot:body-selection="scope">
            <q-checkbox dense v-model="scope.selected" :val="scope.row" />
        </template>
    </q-table>
</template>

<script>
export default {
    name: 'TableOperacionesImportadas',
    props: {
        rows: {
            type: Array,
            default: () => []
        },
        loading: {
            type: Boolean,
            default: false
        },
        fechaActualizacion: {
            type: String,
            default: ''
        },
        selected: {
            type: Array,
            default: () => []
        },
        pagination: {
            type: Object,
            default: () => ({})
        }
    },
    computed: {
        localSelected: {
            get() {
                return this.selected
            },
            set(val) {
                this.$emit('update:selected', val)
            }
        },
        localPagination: {
            get() {
                return this.pagination
            },
            set(val) {
                this.$emit('update:pagination', val)
            }
        }
    },
    data() {
        return {
            filter: '',
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
            ]
        }
    }
}
</script>
