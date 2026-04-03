<template>
    <q-dialog :value="value" @input="$emit('input', $event)">
        <q-card>
            <q-card-section>
                <div class="text-h6">Buscar Transacciones</div>
            </q-card-section>
            <q-separator />
            <q-card-section>
            </q-card-section>
        </q-card>
    </q-dialog>
</template>
<script>
export default {
    name: 'winBuscarTransacciones',
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
        symbol_selected(contract) {
            this.$emit('symbol-select', contract);
            this.$emit('input', false);
        }
    },
}
</script>