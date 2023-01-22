<template>
    <div>
        <q-card flat>
            <q-toolbar class="text-blue-10 q-pb-none q-mb-none">
                <q-btn flat round dense icon="menu">
                    <q-menu>

                    </q-menu>
                </q-btn>
                <span class="text-h6 q-pr-md">
                    Variacion Semanal        
                </span>      
                <q-btn flat round dense icon="search"></q-btn>      
            </q-toolbar>            
            <q-card-section>
                <span class="text-body1">Instrumento:</span>
                <div>{{instrument}}</div>
            </q-card-section>
        </q-card>        
        <div class="row">
            <TableVariacionSemanalCierre class="col-4" :indata="data"/>
            <TableVariacionSemanalMaximo class="col-4" :indata="data"/>
            <TableVariacionSemanalMinimo class="col-4" :indata="data"/>
        </div>
    </div>
</template>
<script>
import TableVariacionSemanalCierre from '@/components/informes/TableVariacionSemanalCierre.vue';
import TableVariacionSemanalMaximo from '@/components/informes/TableVariacionSemanalMaximo.vue';
import TableVariacionSemanalMinimo from '@/components/informes/TableVariacionSemanalMinimo.vue';
import {postconfig} from '@/common/request.js';

export default {
    name:"PanelVariacionSemanal",
    components:{
        TableVariacionSemanalCierre,
        TableVariacionSemanalMaximo,
        TableVariacionSemanalMinimo
    },
    data: () => {
        return {
            symbol:"SOXL",
            instrument:"",
            data:[]
        }
    },
    mounted:function(){
        this.get_variacion_semanal()
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
        }
    }
}
</script>