<template>
    <div>
        <q-card flat>            
            <q-toolbar>            
                <q-toolbar-title class="text-subtitle1 text-blue-10 " shrink>
                    Evolución semanal
                </q-toolbar-title>                  
                <q-btn class="text-capitalize" icon="arrow_back" flat dense color="teal" @click="btn_anterior_click">Anterior</q-btn>
                <div class="text-subtitle1 text-blue-10 q-pl-md q-pr-md">{{ store.panel_evolucion_semanal.state.anyo }}/{{ store.panel_evolucion_semanal.state.semana }}</div>
                <q-btn class="text-capitalize" icon-right="arrow_forward" flat dense color="teal" @click="btn_siguiente_click">Siguiente</q-btn>
            </q-toolbar>                        
            <q-separator/>
            <q-card-section class="q-pa-xs">
                <span class="text-blue-10 text-subtitle1">{{ store.panel_evolucion_semanal.state.cod_symbol }}</span>
                <span class="text-subtitle1">: {{ store.panel_evolucion_semanal.state.nom_symbol }}</span>
            </q-card-section>            
        </q-card>
        <q-separator/>
        <div class="row q-col-gutter-xs q-pt-xs">
            <ChartEvolucionSemanal v-bind:infiltros="filtros" class="col-2"/>
            <TableEvolucionSemanal v-bind:infiltros="filtros" class="col-5"/>            
        </div>        
    </div>
</template>
<script>
import ChartEvolucionSemanal from '@/components/informes-variacion-semanal/ChartEvolucionSemanal.vue';
import TableEvolucionSemanal from '@/components/informes-variacion-semanal/TableEvolucionSemanal.vue';
import store from "./store"

/*
SOXL: 31 PUT/ CALL 32 costo 11/11 0DTE
SOXL: 31 CALL - 0.30 / PUT 32 - 0.88 0DTE
NVDA: 490 PUT 150/492.5 call 1.15
LRCX: 775 put 168 0dte
SPY 18 dec call 472 - 0.28 01-3200700 - oncosalud
*/

export default {
    name:"PanelEvolucionSemanal",
    components:{
        ChartEvolucionSemanal,
        TableEvolucionSemanal
    },
    props:{
        infiltros:{
            type:Object,
            default: () => {}
        }
    },
    data(){
        return {
            store:store 
        }
    },
    watch: {
        
    },
    mounted:function(){
        //this.filtros = this.infiltros
        this.init()
    },
    methods:{
        init:function(){
            let cod_symbol = this.$route.query.cod_symbol
            store.panel_evolucion_semanal.completar_symbol(
                cod_symbol
            )
            store.panel_evolucion_semanal.set_properties(this.$route.query)
        },
        btn_anterior_click: function(){
            let num_semana_actual = parseInt(store.panel_evolucion_semanal.state.semana)
            let num_semana_anterior = num_semana_actual == 1? 52 : num_semana_actual - 1
            let num_anyo_actual = parseInt(store.panel_evolucion_semanal.state.anyo) 
            let num_anyo_anterior = num_semana_anterior == 52? num_anyo_actual - 1 : num_anyo_actual            

            this.$router.push({
                name:"variacion-semanal-evolucion",
                query:{
                    cod_symbol: store.panel_evolucion_semanal.state.cod_symbol,
                    anyo: num_anyo_anterior,
                    semana: num_semana_anterior
                }
            })

            store.panel_evolucion_semanal.set_properties({
                anyo: num_anyo_anterior,
                semana: num_semana_anterior
            })
        },
        btn_siguiente_click: function(){
            let num_semana_actual = parseInt(store.panel_evolucion_semanal.state.semana)
            let num_semana_siguiente = num_semana_actual == 52? 1 : num_semana_actual + 1
            let num_anyo_actual = parseInt(store.panel_evolucion_semanal.state.anyo) 
            let num_anyo_siguiente = num_semana_siguiente == 1? num_anyo_actual + 1 : num_anyo_actual            

            let query = {
                    cod_symbol: store.panel_evolucion_semanal.state.cod_symbol,
                    anyo: num_anyo_siguiente,
                    semana: num_semana_siguiente
                }            

            this.$router.push({
                name:"variacion-semanal-evolucion",
                query:query
            })

            store.panel_evolucion_semanal.set_properties({
                anyo: num_anyo_siguiente,
                semana: num_semana_siguiente
            })
        }
    }
}
</script>