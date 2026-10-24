<template>
    <q-dialog v-model="open">
        <q-card style="width: 500px; max-width: 90vw;">
            <q-toolbar>
                <q-toolbar-title class="text-blue-10">
                    Filtro de Symbols
                </q-toolbar-title>
                <q-btn flat round dense icon="close" v-close-popup />
            </q-toolbar>
            <q-separator />

            <q-card-section class="q-pt-md">
                <div class="q-gutter-y-md">
                    <q-input
                        v-model="cod_symbol"
                        label="Código de Symbol"
                        placeholder="Ej: AAPL, MSFT, TSLA"
                        outlined
                        dense
                        color="blue-10"
                        clearable
                        autofocus
                        @keyup.enter="btn_aceptar_click"
                    >
                        <template v-slot:prepend>
                            <q-icon name="search" color="blue-10" />
                        </template>
                    </q-input>

                    <q-input
                        v-model="name"
                        label="Nombre"
                        placeholder="Ej: Apple Inc, Microsoft, Tesla"
                        outlined
                        dense
                        color="blue-10"
                        clearable
                        @keyup.enter="btn_aceptar_click"
                    >
                        <template v-slot:prepend>
                            <q-icon name="badge" color="blue-10" />
                        </template>
                    </q-input>
                </div>
            </q-card-section>

            <q-separator />

            <q-card-actions align="right" class="q-px-md q-py-sm">
                <q-btn
                    label="Limpiar"
                    class="text-capitalize"
                    color="grey-7"
                    flat
                    icon="clear_all"
                    @click="limpiar"
                />
                <q-space />
                <q-btn
                    label="Cancelar"
                    class="text-capitalize"
                    color="red-14"
                    flat
                    v-close-popup
                />
                <q-btn
                    label="Filtrar"
                    class="text-capitalize"
                    color="blue-10"
                    unelevated
                    icon="filter_alt"
                    @click="btn_aceptar_click"
                />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script>
export default {
    name: "WinFiltrarSymbols",
    props: {
        value: {
            required: true
        }
    },
    watch: {
        open: function (newval) {
            this.$emit('input', newval)
        },
        value: function (newval) {
            this.open = newval
        }
    },
    data() {
        return {
            open: this.value,
            cod_symbol: "",
            name: ""
        }
    },
    methods: {
        btn_aceptar_click: function () {
            this.$emit('btn-aceptar-click', {
                cod_symbol: this.cod_symbol ? this.cod_symbol.trim() : "",
                name: this.name ? this.name.trim() : ""
            })
            this.open = false
        },
        limpiar: function () {
            this.cod_symbol = ""
            this.name = ""
        }
    }
}
</script>