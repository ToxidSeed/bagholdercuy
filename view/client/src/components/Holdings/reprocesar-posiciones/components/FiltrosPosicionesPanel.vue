<template>
    <q-card flat>
        <q-card-section class="q-col-gutter-xs">
            <HelperPeriodo />
            <SelectSymbol />
        </q-card-section>
        <q-separator />
        <q-card-actions>
            <q-btn color="primary" icon="clear_all" label="Limpiar" flat no-caps />
            <q-btn color="primary" icon="check" label="Aplicar" flat no-caps @click="aplicarFiltros" />
        </q-card-actions>
    </q-card>
</template>

<script>
import HelperPeriodo from '../../../common/HelperPeriodo.vue';
import SelectSymbol from '../../../SelectSymbol.vue';
import { actions } from '../reprocesarPosicionesStage.js';
export default {
    name: 'FiltrosPosicionesPanel',
    components: {
        HelperPeriodo,
        SelectSymbol
    },
    methods: {
        aplicarFiltros() {
            actions.obtenerDatosTablePosiciones({
                id_cuenta: localStorage.getItem("id_cuenta")
            })
        }
    }
}
</script>