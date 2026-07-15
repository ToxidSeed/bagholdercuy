<template>
    <q-dialog v-model="open">
        <q-card style="min-width: 35vw;">
            <q-toolbar class="text-blue-10">
                <q-toolbar-title>
                    Filtros
                </q-toolbar-title>
                <q-btn flat round dense icon="close" color="red" @click="btn_cerrar_click" />
            </q-toolbar>
            
            <q-card-section>
                <div class="q-gutter-xs">
                    <SelectSymbol v-on:select-symbol="select_symbol_handler" />
                    <div class="q-gutter-xs">
                        <div class="text-caption text-primary">Perimetro principal</div>
                        <div>
                            <HelperPeriodo ref="helperPeriodo" />
                        </div>
                    </div>
                </div>
            </q-card-section>
            
            <q-card-actions align="right">
                <q-btn label="Aceptar" color="blue-10" @click="btn_aceptar_click" dense no-caps/>
                <q-btn label="Cerrar" color="red-10" @click="btn_cerrar_click"  dense no-caps/>
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>
<script>
import SelectSymbol from "@/components/SelectSymbol.vue";
import HelperPeriodo from "@/components/common/HelperPeriodo.vue";

export default {
    name: "WinFiltrosVariacionDiaria",
    components: {
        SelectSymbol,
        HelperPeriodo
    },
    props: {
        value: {
            required: true
        }
    },
    data() {
        return {
            open: this.value,
            symbol_value: "",
            symbol_text: "",
            fch_desde: null,
            fch_hasta: null,
            per_secu_fch_desde: null,
            per_secu_fch_hasta: null,
            perimetro_secundario_options: [
                {
                    value: "FCH_MINIMO_IMP_CIERRE",
                    label: "Fecha de Imp. Minimo de Cierre"
                }, {
                    value: "FCH_MAXIMO_IMP_CIERRE",
                    label: "Fecha de Imp. Maximo de Cierre"
                }, {
                    value: "FCH_MINIMO",
                    label: "Fecha de Imp. Minimo"
                }, {
                    value: "FCH_MAXIMO",
                    label: "Fecha de Imp. Maximo"
                }, {
                    value: "FCH_MINIMO_APERTURA",
                    label: "Fecha de Imp. Minimo Apertura"
                }, {
                    value: "FCH_MAXIMO_APERTURA",
                    label: "Fecha de Imp. Maximo Apertura"
                }, {
                    value: "FCH_MINIMO_CIERRE_ANT",
                    label: "Fecha de Imp. Minimo Cierre Anterior"
                }, {
                    value: "FCH_MAXIMO_CIERRE_ANT",
                    label: "Fecha de Imp. Maximo Cierre Anterior"
                }
            ],
            campo_selectionado: null,
            operador_comparacion: null,
            valor_actual: null
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
    methods: {
        select_symbol_handler: function (selected) {
            this.symbol_value = selected.value
            this.symbol_text = selected.label
        },
        btn_aceptar_click: function () {
            console.log("btn_aceptar_click", this.$refs.helperPeriodo.fchDesde, this.$refs.helperPeriodo.fchHasta)
            this.$emit('btn-aceptar-click', {
                symbol_value: this.symbol_value,
                symbol_text: this.symbol_text,
                fch_desde: this.$refs.helperPeriodo.fchDesde,
                fch_hasta: this.$refs.helperPeriodo.fchHasta
            })
        },
        btn_cerrar_click: function () {
            this.$emit('btn-cerrar-click')
            this.open = false
        },
        btn_agregar_condicion: function () {
            /*
            let element = {
                campo: this.campo_selectionado,
                operador: this.operador_comparacion,
                valor: this.valor_actual
            }
            */
            let campo = null
            let oper_comparacion = null

            let row = {
                campo: campo,
                oper_comparacion: oper_comparacion,
                valor: null
            }

            this.condiciones.push(row)
        }
    }
}
</script>