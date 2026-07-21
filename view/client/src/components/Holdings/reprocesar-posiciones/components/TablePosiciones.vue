<template>
    <div>
        <q-table :data="data" :columns="columns" row-key="symbol" :filter="filter" separator="vertical" dense flat
            selection="multiple" :selected.sync="selected">
            <template v-slot:top>
                <!--
                <div class="row full-width items-center justify-center">
                    <q-input class="col-4" outlined dense debounce="300" v-model="filter" stack-label
                        label="Filtrar Resultados">
                        <template v-slot:append>
                            <q-icon name="searchfind" />
                        </template>
</q-input>
</div>
-->
                <div class="row">
                    <div class="col-11 text-subtitle1 text-primary">Transacciones</div>
                    <div>
                        <q-btn label="Filtros" icon="filter_list_off" color="primary" flat no-caps>
                            <q-popup-proxy>
                                <FiltrosPosicionesPanel style="width:700px;" />
                            </q-popup-proxy>
                        </q-btn>
                    </div>
                </div>
            </template>
        </q-table>
    </div>
</template>

<script>
import FiltrosPosicionesPanel from './FiltrosPosicionesPanel.vue'
export default {
    name: "TablePosiciones",
    props: {
        data: {
            type: Array,
            default: () => []
        }
    },
    components: {
        FiltrosPosicionesPanel
    },
    data() {
        return {
            selected: [],
            filter: '',
            columns: [
                {
                    name: 'symbol',
                    align: 'left',
                    label: 'Symbol',
                    field: 'symbol',
                    sortable: true,
                    style: 'width: 60px;'
                },
                {
                    name: 'num_transacciones',
                    align: 'center',
                    label: 'Num. Transacciones',
                    field: 'num_transacciones',
                    sortable: true,
                    style: 'width: 60px;'
                },
                {
                    name: 'fch_inicio',
                    align: 'center',
                    label: 'Fch. Transaccion Inicio',
                    field: 'fch_inicio',
                    sortable: true,
                    style: 'width: 60px;'
                },
                {
                    name: 'fch_fin',
                    align: 'center',
                    label: 'Fch. Transaccion Fin',
                    field: 'fch_fin',
                    sortable: true,
                    style: 'width: 60px;'
                }, {
                    name: '',
                    label: ''
                }
            ]
        }
    }
}
</script>
