<template>
    <q-card flat>
        <q-card-section class="q-col-gutter-xs">
            <HelperPeriodo />
            <SelectSymbol />
        </q-card-section>
        <q-separator />
        <q-card-actions>
            <q-btn color="primary" icon="clear_all" label="Limpiar" flat no-caps />
            <q-btn color="primary" icon="check" label="Aplicar" flat no-caps />
        </q-card-actions>
    </q-card>
</template>

<script>
import HelperPeriodo from '../../../common/HelperPeriodo.vue';
import SelectSymbol from '../../../SelectSymbol.vue';
export default {
    name: 'FiltrosPosicionesPanel',
    components: {
        HelperPeriodo,
        SelectSymbol
    }
}
</script>