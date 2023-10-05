<template>
    <div>
        <q-card flat>
            <q-toolbar class="text-blue-10 q-pb-none p-mb-none">
                <span class="text-h6 q-pr-md">
                    Variacion Mensual        
                </span>      
                <q-btn flat round dense icon="search" @click="win_filtro_variacion_mensual.open=true"></q-btn>                          
            </q-toolbar>
        </q-card>
        <TableVariacionMensual
        v-bind:indata="data"
        v-bind:symbol="symbol"
        v-bind:symbol_value="symbol_value"
        v-bind:symbol_nombre="symbol_text"
        />
        <WinFiltrosVariacionMensual 
        v-model="win_filtro_variacion_mensual.open"
        v-on:btn-aceptar-click="filtrar"
        />
    </div>
</template>
<script>
import TableVariacionMensual from '@/components/informes/TableVariacionMensual.vue'
import WinFiltrosVariacionMensual from '@/components/informes/WinFiltrosVariacionMensual.vue';
import {postconfig} from '@/common/request.js';
export default {
    name:"PanelVariacionMensual",
    components:{
        TableVariacionMensual,
        WinFiltrosVariacionMensual
    },
    data: () => {
        return {
            symbol_value:"",
            symbol_text:"",
            data:[],
            win_filtro_variacion_mensual:{
                open:false
            }
        }
    },
    methods:{
        get_variacion_mensual:function(){
            this.$http.post(
                '/reportes/VariacionMensualBuilder/build',{
                    symbol:this.symbol_value
                },
                postconfig()
            ).then(httpresp => {
                let appresp = httpresp.data
                this.data = []

                appresp.data.forEach(element => {
                    console.log(element)
                    element.imp_cierre_ant = element.imp_cierre_ant.toFixed(2)
                    element.imp_apertura = element.imp_apertura.toFixed(2)
                    element.imp_maximo = element.imp_maximo.toFixed(2)
                    element.imp_minimo = element.imp_minimo.toFixed(2)
                    element.imp_cierre = element.imp_cierre.toFixed(2)
                    element.pct_variacion_cierre = element.pct_variacion_cierre.toFixed(2)
                    element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(2)
                    element.pct_variacion_apertura = element.pct_variacion_apertura.toFixed(2)
                    element.imp_variacion_apertura = element.imp_variacion_apertura.toFixed(2)
                    element.pct_variacion_maximo = element.pct_variacion_maximo.toFixed(2)
                    element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(2)
                    element.pct_variacion_minimo = element.pct_variacion_minimo.toFixed(2)
                    element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(2)
                    this.data.push(element)
                })
                
            })
        },
        filtrar:function(filtros){
            this.symbol_value = filtros.symbol_value
            this.symbol_text = filtros.symbol_text
            this.get_variacion_mensual()
        }
    }
}
</script>