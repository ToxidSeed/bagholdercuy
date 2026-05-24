<template>
    <q-page class="q-pt-md">
        <q-bar class="bg-white">
            <div class="text-h6 text-primary">Reprocesar Posiciones</div><q-space />
        </q-bar>
        <q-bar class="bg-white">
            <q-btn color="primary" label="REPROCESAR" no-caps icon="autorenew" @click="onReprocesar" />
        </q-bar>
        <q-separator />
        <q-card flat>
            <q-card-section>
                <div class="q-gutter-sm">
                    <q-radio v-model="tipo_proceso" val="todos" label="Procesar todos" />
                    <q-radio v-model="tipo_proceso" val="seleccionados" label="Procesar Seleccionados" />
                </div>
            </q-card-section>
        </q-card>
        <q-separator />
        <TablePosiciones :data="posiciones" />
    </q-page>
</template>

<script>
import TablePosiciones from './reprocesar-posiciones/TablePosiciones.vue'

export default {
    name: 'ReprocesarPosicionesPage',
    components: {
        TablePosiciones
    },
    data() {
        return {
            tipo_proceso: 'todos',
            posiciones: []
        }
    },
    methods: {
        onReprocesar() {
            this.$q.notify({
                message: 'Reprocesando...',
                color: 'info',
                icon: 'info'
            })
            // Evento o llamado a API
            this.$emit('reprocesar')
        }
    }
}
</script>

<style scoped></style>
