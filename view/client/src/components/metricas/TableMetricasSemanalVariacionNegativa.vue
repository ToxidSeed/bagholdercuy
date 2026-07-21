<template>
    <div>
        <q-table :data="metricas.state.table_metricas_semanal_var_negativa.data" :columns="columns" row-key="name" dense
            separator="vertical" :pagination="pagination" flat>
            <template v-slot:top>
                <div class="row q-gutter-md">
                    <div class="text-red-10 text-subtitle1">Cierres negativos</div>
                    <q-separator vertical />
                    <div>
                        {{ metricas.state.table_metricas_semanal_var_negativa.count }}/{{
                            metricas.state.table_metricas_semanal_var_negativa.total }}
                    </div>
                </div>
            </template>
            <template v-slot:body="props">
                <q-tr :props="props" :class="getRowClass(props.row)">
                    <q-td v-for="col in props.cols" :key="col.name" :props="props">
                        {{ col.value }}
                    </q-td>
                </q-tr>
            </template>
        </q-table>
    </div>
</template>
<script>
import metricas from './metricas-store';

export default {
    name: "TableMetricasVariacionPositiva",
    data() {
        return {
            data: [],
            columns: [{
                name: "index",
                field: "index",
                style: "width:50px",
                label: ""
            }, {
                name: "imp_variacion_cierre",
                field: "imp_variacion_cierre",
                label: "Imp. var cierre",
                style: "width:50px",
            }, {
                name: "imp_variacion_maximo",
                field: "imp_variacion_maximo",
                label: "Imp. var max",
                style: "width:50px",
            }, {
                name: "imp_variacion_minimo",
                field: "imp_variacion_minimo",
                label: "Imp. var min",
                style: "width:50px",
            }, {
                name: "imp_var_min_max",
                field: "imp_var_min_max",
                label: "Imp. var min-max",
                style: "width:50px",
            }, {
                name: "imp_var_min_cierre",
                field: "imp_var_min_cierre",
                label: "Imp. var min-cierre",
                style: "width:50px",
            }, {
                name: "",
                field: "",
                label: ""
            }],
            metricas: metricas,
            pagination: {
                rowsPerPage: 16
            }
        }
    },
    methods: {
        getRowClass(row) {
            // Cambia la condición según tu lógica
            console.log("getRowClass", row)
            if (row.index === 'min') {
                return 'bg-red text-white'  // clase de Quasar
            }
            return ''
        }
    }
}
</script>