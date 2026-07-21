<template>
    <q-select ref="selsymbol" :label="label" stack-label v-model="symbol" color="blue-10" dense outlined
        :use-input="useInput" clearable input-debounce="1000" @filter="filterFn" @input="sel_symbol"
        @clear="clear_symbol" :options="symbol_list" :readonly="readonly" class="text-overline">
        <template v-slot:selected>
            <div class="q-pt-xs" v-if="symbol && symbol.value"><span class="text-blue-10 text-bold">{{ symbol.value
            }}</span> - {{ symbol.label }}</div>
        </template>
        <template v-slot:option="scope">
            <q-item v-bind="scope.itemProps" v-on="scope.itemEvents">
                <q-item-section>
                    <span class="text-blue-10 text-bold">{{ scope.opt.value }}</span><span>{{ scope.opt.label }}</span>
                </q-item-section>
            </q-item>
        </template>
    </q-select>

</template>
<script>
import { headers } from '@/common/common.js'

export default {
    name: "SelectSymbol",
    props: {
        in_symbol: {
            type: Object,
            default: () => ({})
        },
        readonly: {
            type: Boolean,
            default: false
        },
        label: {
            type: String,
            default: "Buscar Symbol"
        }
    },
    data: () => {
        return {
            symbol: null,
            symbol_list: [],
            useInput: true
        }
    },
    mounted: function () {
        if (Object.keys(this.in_symbol).length > 0) {
            console.log(this.in_symbol)
            this.symbol = this.in_symbol
        }
    },
    methods: {
        clear_symbol: function () {
            this.$emit('clear-symbol')
        },
        sel_symbol: function (selected) {
            if (selected == null) {
                this.useInput = true
                return
            }

            this.useInput = false
            this.symbol = selected
            this.$emit('select-symbol', selected)
            // Hacer que pierda el foco después del ciclo actual para evitar comportamiento extraño de renderizado
            this.$nextTick(() => {
                if (this.$refs.selsymbol) this.$refs.selsymbol.blur()
            })
        },
        filterFn: function (val, update) {
            console.log(val)
            if (val === '') {
                console.log(val)
                update(() => {
                    this.symbol_list = []
                })
                return
                /*
                
                this.symbol = ""
                */
            } else {
                this.$http.post(
                    'SymbolManager/SymbolFinder/buscar_por_texto', {
                    texto: val
                }, {
                    headers: headers()
                }).then(httpresponse => {
                    var appresponse = httpresponse.data
                    //console.log(appresponse.data)
                    /*this.symbol_list = appresponse.data*/
                    var options = []
                    for (let element of appresponse.data) {
                        options.push({
                            "id_symbol": element["id"],
                            "value": element["symbol"],
                            "label": element["name"]
                        })
                    }

                    update(() => {
                        this.symbol_list = options
                    })
                })
            }

        }
    }
}
</script>