<template>
    <q-dialog :value="value" @input="$emit('input', $event)">
        <q-card style="min-width: 700px">
            <q-card-section class="row items-center justify-between">
                <div class="text-subtitle1 text-weight-bold text-primary">Buscar Transacciones</div>
                <q-btn icon="close" color="red" flat round dense v-close-popup />
            </q-card-section>
            <q-separator />
            <q-card-section>
                <!--mete la tabla aqui-->
                <TableMaxFechasTransacciones @symbol-selected="symbol_selected" />
            </q-card-section>
        </q-card>
    </q-dialog>
</template>
<script>
import TableMaxFechasTransacciones from './TableMaxFechasTransacciones.vue'

export default {
    name: 'winBuscarTransacciones',
    components: {
        TableMaxFechasTransacciones
    },
    props: {
        value: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            open: false
        }
    },
    methods: {
        symbol_selected(row) {
            this.$emit('symbol-selected', row);
            this.$emit('input', false);
        }
    },
}
</script>