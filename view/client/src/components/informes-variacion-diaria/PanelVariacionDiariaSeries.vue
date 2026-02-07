<template>
    <div>
        <q-card flat>            
            <TableVariacionDiaria :indata="data"
            :symbol_value="symbol_value"
            :symbol_nombre="symbol_text"        
            >        
            </TableVariacionDiaria>
            <q-inner-loading :showing="loading">
                <q-spinner-gears size="50px" color="blue-10" />
            </q-inner-loading>
        </q-card>
    </div>
</template>
<script>
import TableVariacionDiaria from '@/components/informes/TableVariacionDiaria.vue'
import {postconfig} from '@/common/request.js';

export default {
    name:"PanelVariacionDiariaSeries",
    components:{
        TableVariacionDiaria
    }
    ,
    mounted:function(){
        this.init()
    },
    watch:{
        $route:function(newval){            
            if ( Object.keys(newval.query).length > 0){
                this.symbol_value = newval.query.cod_symbol
                this.get_variacion_diaria()
            }
        }
    },
    data(){
        return {
            symbol_value:"",
            symbol_text:"",
            data:[],
            loading:false
        }        
    },
    methods:{
        init:function(){
            if (Object.keys(this.$route.query).length > 0){
                this.symbol_value = this.$route.query.cod_symbol
                this.get_variacion_diaria()
            }                        
        },
        get_variacion_diaria:function(){     
            this.loading = true       
            this.$http.post(
                '/reportes/VariacionDiariaBuilder/build',{
                    symbol:this.symbol_value
                },
                postconfig()
            ).then(httpresp => {
                this.msgbox = {
                    httpresp:httpresp,
                    onerror:true
                }

                let appresp = httpresp.data
                this.data = []

                appresp.data.forEach(element => {                    
                    element.imp_cierre_ant = element.imp_cierre_ant.toFixed(2)
                    element.num_dia_semana = new Date(element.fch_serie).getDay()+1
                    element.imp_apertura = element.imp_apertura.toFixed(2)
                    element.imp_maximo = element.imp_maximo.toFixed(2)
                    element.imp_minimo = element.imp_minimo.toFixed(2)
                    element.imp_cierre = element.imp_cierre.toFixed(2)
                    element.imp_variacion_apertura = element.imp_variacion_apertura.toFixed(2)                    
                    element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(2)
                    element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(2)
                    element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(2)                    
                    element.pct_variacion_apertura = element.pct_variacion_apertura.toFixed(2)                    
                    element.pct_variacion_cierre = element.pct_variacion_cierre.toFixed(2)
                    element.pct_variacion_maximo = element.pct_variacion_maximo.toFixed(2)
                    element.pct_variacion_minimo = element.pct_variacion_minimo.toFixed(2)                    
                    this.data.push(element)
                })                
            }).finally( () => {
                this.loading = false
            })
            
        }
    }
}
</script>