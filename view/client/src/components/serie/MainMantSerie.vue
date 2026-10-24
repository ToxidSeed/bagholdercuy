<template>
    <div>
        <q-toolbar class="text-blue-10">
            <q-toolbar-title>
                Series
            </q-toolbar-title>
            <q-btn flat round dense icon="refresh" color="blue-10" @click="store.get_resumen_serie()">
                <q-tooltip>Actualizar listado de series</q-tooltip>
            </q-btn>
        </q-toolbar>
        <q-separator />
        <q-card flat>
            <q-bar class="bg-white q-py-sm">
                <q-btn stack-label flat icon="add_circle_outline" dense label="SINCRONIZAR SÍMBOLO" color="blue-10"
                    @click="store.abrir_w_sincronizar('')">
                </q-btn>
            </q-bar>
        </q-card>
        <q-separator />
        <q-card flat>
            <div class="col">
                <div class="row">
                    <div class="col">
                        <TableResumenSerie />
                    </div>
                </div>
            </div>
        </q-card>
    </div>
</template>
<script>
import store from './store'
import TableResumenSerie from '@/components/serie/TableResumenSerie.vue'

export default {
    name: "MainMantSerie",
    components: {
        TableResumenSerie
    },
    data: () => {
        return {
            store: store
        }
    }
}
</script>