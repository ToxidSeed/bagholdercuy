<template>
    <div class="q-pa-sm">
        <div class="row q-col-gutter-xs">
            <div>
                <q-card flat bordered>
                    <q-card-section>
                        <div class="q-gutter-sm">
                            <q-radio v-model="opcionProcesamiento" val="todos" label="Procesar Todos" />
                            <q-radio v-model="opcionProcesamiento" val="seleccion" label="Procesar Seleccion" />
                        </div>
                    </q-card-section>
                </q-card>
            </div>
        </div>
    </div>
</template>
<script>


export default {
    name: 'PanelGenerarTransacciones',
    props: {},
    data() {
        return {
            opcionProcesamiento: 'todos',
            symbol: '',
            selected: []
        }
    },
    components: {

    },
    methods: {
        generarTransacciones() {
            this.$emit('generar')
        }
    },
    watch: {
        opcionProcesamiento(val) {
            this.$emit('update:opcionProcesamiento', val)
        }
    }
}
</script>