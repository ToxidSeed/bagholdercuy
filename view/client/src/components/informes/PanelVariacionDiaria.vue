<template>
    <div>
        <q-card flat>
            <q-toolbar class="text-blue-10 q-pb-none p-mb-none">
                <q-btn class="q-ml-xs" color="blue-10" dense icon="menu" flat>
                    <q-menu>
                        <q-list dense>
                            <q-item v-for="item in routes" :key="item.name" :to="get_target(item)">
                                <q-item-section class="text-subtitle1  text-blue-10">
                                    {{ item.label }}
                                </q-item-section>
                            </q-item>
                        </q-list>
                    </q-menu>
                </q-btn>
                <span class="text-h6 q-pr-md">
                    Variacion Diaria
                </span>
                <q-btn flat round dense icon="search" @click="win_filtros_variacion_diaria.open = true"></q-btn>
            </q-toolbar>
        </q-card>
        <router-view :symbolName="symbol_text" :symbolValue="symbol_value" :fchDesde="fch_desde"
            :fchHasta="fch_hasta"></router-view>
        <WinFiltrosVariacionDiaria v-model="win_filtros_variacion_diaria.open" v-on:btn-aceptar-click="filtrar" />
        <MessageBox v-bind:config="msgbox" />
    </div>
</template>
<script>
import WinFiltrosVariacionDiaria from '@/components/informes/WinFiltrosVariacionDiaria.vue';
import MessageBox from '../dialogs/MessageBox.vue';
import _ from "lodash"
import date from 'date-and-time'

export default {
    name: "PanelVariacionDiaria",
    components: {
        WinFiltrosVariacionDiaria,
        MessageBox
    },
    watch: {
        /*
        $route:function(newval){            
            if ( Object.keys(newval.query).length > 0){
                this.symbol_value = newval.query.cod_symbol
                this.get_variacion_diaria()
            }
        }
        */
    },
    mounted: function () {
        if (this.$route.query.cod_symbol) {
            this.symbol_value = this.$route.query.cod_symbol
        }
    },
    data() {
        return {
            symbol_value: "",
            symbol_text: "",
            data: [],
            win_filtros_variacion_diaria: {
                open: false
            },
            msgbox: {},
            loading: false,
            routes: [
                {
                    name: 'variacion-diaria-series-evolucion',
                    label: 'Candle Stick series diarias'
                }, {
                    path: '/variaciondiaria',
                    label: 'Variacion Diaria'
                }
            ],
            fch_desde: "",
            fch_hasta: ""
        }
    },
    methods: {
        get_target(route) {
            if (_.has(route, "name")) {
                return { name: route.name }
            }
            if (_.has(route, "path")) {
                return { path: route.path }
            }
            return {}
        },
        get_label(route) {
            return route.label
        },
        filtrar: function (filtros) {
            this.symbol_value = filtros.symbol_value
            this.symbol_text = filtros.symbol_text
            //this.fch_desde = filtros.fchDesde
            //this.fch_hasta = filtros.fchHasta

            const fch_desde = filtros?.fch_desde ? date.transform(filtros.fch_desde, 'DD/MM/YYYY', 'YYYY-MM-DD') : ""
            const fch_hasta = filtros?.fch_hasta ? date.transform(filtros.fch_hasta, 'DD/MM/YYYY', 'YYYY-MM-DD') : ""

            const query = {
                cod_symbol: filtros.symbol_value,
                fch_desde: fch_desde,
                fch_hasta: fch_hasta
            }
            console.log("variacion-diaria", query)
            this.$router.push({ path: this.$route.path, query: query }).catch(err => {
                if (err.name !== 'NavigationDuplicated') {
                    throw err;
                }
            })
        }
    }
}
</script>