<template>
    <div>        
        <q-toolbar class="text-blue-10 q-pb-none q-mb-none">
            <q-btn flat round dense icon="menu">
                <q-menu>
                    <q-list dense>
                        <q-item clickable :to="{name:'variacion-semanal-evolucion'}">
                            <q-item-section>Evolución</q-item-section>
                        </q-item>
                    </q-list>
                </q-menu>
            </q-btn>
            <span class="text-h6 q-pr-md">
                Variacion Semanal        
            </span>      
            <q-btn flat round dense icon="search" @click="win_filtro_variacion_semanal.open=true"></q-btn>      
        </q-toolbar>     
        <q-separator/>                                      
        <div class="row">
            <!--
            <TableVariacionSemanal class="col-12" :indata="data"
            v-bind:symbol="symbol"
            v-bind:symbol_nombre="symbol_nombre"
            />  
            -->
            <router-view class="col-12" 
                :indata="data"          
                :infiltros="filtros"                  
            />          
        </div>
        <WinFiltrosVaracionSemanal 
        v-model="win_filtro_variacion_semanal.open"        
        v-on:btn-aceptar-click="filtrar"
        />
    </div>
</template>
<script>
//import TableVariacionSemanal from '@/components/informes/TableVariacionSemanal.vue';
import WinFiltrosVaracionSemanal from '@/components/informes-variacion-semanal/WinFiltrosVaracionSemanal.vue';

import {postconfig} from '@/common/request.js';

export default {
    name:"PanelVariacionSemanal",
    components:{
//        TableVariacionSemanal,
        WinFiltrosVaracionSemanal,
        /*TableVariacionSemanalMaximo,
        TableVariacionSemanalMinimo*/
    },
    data: () => {
        return {
            symbol:"",
            symbol_nombre:"",
            instrument:"",
            data:[],
            win_filtro_variacion_semanal:{
                open:false
            },
            filtros:{}
        }
    },
    mounted:function(){
        //this.get_variacion_semanal()
        console.log('mounted-panel-variacion-semanal')
    },
    methods:{
        get_variacion_semanal:function(){
            this.$http.post(
                '/reportes/VariacionSemanalBuilder/build',{
                    symbol: this.symbol
                },
                postconfig()
            ).then(httpresp => {
                let appresp = httpresp.data
                this.data = []
                
                appresp.data.forEach(element => {
                    element.imp_cierre_ant = element.imp_cierre_ant.toFixed(2)
                    element.imp_maximo = element.imp_maximo.toFixed(2)
                    element.imp_minimo = element.imp_minimo.toFixed(2)
                    element.imp_cierre = element.imp_cierre.toFixed(2)
                    element.pct_variacion_cierre = element.pct_variacion_cierre.toFixed(2)
                    element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(2)
                    element.pct_variacion_maximo = element.pct_variacion_maximo.toFixed(2)
                    element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(2)
                    element.pct_variacion_minimo = element.pct_variacion_minimo.toFixed(2)
                    element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(2)
                    this.data.push(element)                    
                })
            })
        },
        filtrar:function(filtros){            
            this.symbol = filtros.symbol_value
            this.symbol_nombre = filtros.symbol_text
            this.filtros = filtros
            //this.get_variacion_semanal()
        }
    }
}
</script>