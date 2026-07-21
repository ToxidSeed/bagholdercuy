<template>
    <div>
        <q-card flat>
            <q-card-section class="text-primary text-h5">
                Importación de Operaciones
            </q-card-section>
        </q-card>
        <q-bar flat class="bg-white">
            <q-btn flat color="primary" icon="upload" @click="btn_cargar_click">Cargar</q-btn>
        </q-bar>
        <TableIbkrOperaciones />
        <WinCargarIbkrOperaciones v-model="openCargarOperaciones" />
    </div>
</template>
<script>
import TableIbkrOperaciones from './importar/TableIbkrOperaciones.vue';
import WinCargarIbkrOperaciones from './importar/WinCargarIbkrOperaciones.vue';

export default {
    name: "IbkrImportarOperacionesPage",
    components: {
        TableIbkrOperaciones,
        WinCargarIbkrOperaciones
    },
    data: () => {
        return {
            openCargarOperaciones: false
        }
    },
    methods: {
        btn_cargar_click: function () {
            this.openCargarOperaciones = true
        }
    }
}
</script>