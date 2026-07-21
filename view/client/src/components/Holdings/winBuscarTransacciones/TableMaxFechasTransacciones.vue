<template>
    <div>
        <q-table :data="data" :columns="columns" :filter="filter" row-key="cod_symbol" flat dense
            @row-dblclick="on_row_dblclick" :pagination="pagination">
            <template v-slot:top-right>
                <q-input dense debounce="300" v-model="filter" placeholder="Buscar">
                    <template v-slot:append>
                        <q-icon name="search" />
                    </template>
                </q-input>
            </template>
        </q-table>
    </div>
</template>

<script>
import { get_postconfig } from '@/common/request.js'
import { TRANSACCION } from '@/api/endpoints.js'

export default {
    name: 'TableMaxFechasTransacciones',
    data() {
        return {
            filter: '',
            data: [],
            pagination: {
                rowsPerPage: 20
            },
            columns: [
                { name: 'cod_symbol', field: 'cod_symbol', label: 'Symbol', align: 'left', sortable: true },
                { name: 'max_fch_hr_transaccion', field: 'max_fch_hr_transaccion', label: 'Max Fecha', align: 'left', sortable: true },
                { name: 'fifo_seq_informado', label: 'FIFO Seq Informado', field: row => row.min_orden_fifo === 0 ? 'NO' : 'SI', align: 'left', sortable: true },
                { name: 'ctd_transacciones', field: 'ctd_transacciones', label: 'Ctd Transacciones', align: 'left', sortable: true }
            ]
        }
    },
    mounted() {
        this.loadData()
    },
    methods: {
        async loadData() {
            try {
                let postconfig;
                if (typeof get_postconfig === 'function') {
                    postconfig = get_postconfig();
                } else {
                    postconfig = {};
                }

                let httpresp = await this.$http.post(TRANSACCION.GET_MAX_FECHAS_AGROUPADAS_X_SYMBOL, {
                    id_cuenta: localStorage.getItem("id_cuenta"),
                }, postconfig)
                let appdata = httpresp.data
                if (appdata.success) {
                    this.data = appdata.data
                }
            } catch (e) {
                console.error(e)
            }
        },
        on_row_dblclick(evt, row) {
            this.$emit('symbol-selected', row)
        }
    }
}
</script>
