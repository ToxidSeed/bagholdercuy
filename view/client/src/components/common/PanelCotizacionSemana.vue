<template>
    <div>        
        <q-card class="text-center q-ma-xs" flat>
            <div class="q-pa-xs">
                <div class="row">
                    <div>
                        <div class="text-caption float-left">ant</div>
                        <div class="q-pt-md q-pl-md q-pr-md text-h5">{{panel_cotizacion_semana_store.imp_cierre_ant}}</div>
                    </div>
                    <q-separator vertical/>
                    <div>
                        <div class="text-caption float-left">ape</div>
                        <div class="q-pt-md q-pl-md q-pr-md text-h5">{{panel_cotizacion_semana_store.imp_apertura}}</div>                                        
                    </div>
                    <q-separator vertical/>
                    <div>
                        <div class="text-caption float-left">max</div>
                        <div class="q-pt-md q-pl-md q-pr-md text-h5">{{panel_cotizacion_semana_store.imp_maximo}}</div>                                        
                    </div>                   
                    <q-separator vertical/>
                    <div>
                        <div class="text-caption float-left">min</div>
                        <div class="q-pt-md q-pl-md q-pr-md text-h5">{{panel_cotizacion_semana_store.imp_minimo}}</div>                                        
                    </div>      
                    <q-separator vertical/>
                    <div>
                        <div class="text-caption float-left">act</div>
                        <div class="q-pt-md q-pl-md q-pr-md text-h5">{{panel_cotizacion_semana_store.imp_cierre_act}}</div>                                        
                    </div>                   
                    <q-separator vertical/>
                    <div>
                        <div class="text-caption float-left">var</div>
                        <div class="q-pt-md q-pl-md q-pr-md text-h5 text-bold"
                        :class="{'text-red':flg_var_positivo==false,'text-green':flg_var_positivo}"
                        >{{panel_cotizacion_semana_store.imp_variacion}}</div>                                        
                    </div>                         
                    <q-separator vertical/>
                    <div>
                        <div class="text-caption float-left">pct %</div>
                        <div class="q-pt-md q-pl-md q-pr-md text-h5 text-bold">
                            <div v-bind:class="{'text-red':flg_var_positivo==false,'text-green':flg_var_positivo}">{{panel_cotizacion_semana_store.pct_variacion}}</div>
                        </div>                                        
                    </div>
                    <q-separator vertical/>                
                    <div class="column justify-center">
                        <div class="col-8">
                            <q-btn icon="refresh" round flat  size="md" color="green"/>
                        </div>
                    </div>                                                     
                </div>                                             
            </div>                                                                             
        </q-card>     
    </div>
</template>
<script>
import panel_cotizacion_semana_store from "./panel-cotizacion-semana-store"
import store from "@/store/store"
import VariacionSemanal from "@/api/variacion-semanal"
import _ from "lodash";
//import date from "date-and-time"
import moment from "moment"

export default {
    name:"PanelCotizacionSemana",
    props:{
        cod_symbol:{
            type:String,
            required:true,
            default:""
        }
    },
    data() {
        return {
            panel_cotizacion_semana_store:panel_cotizacion_semana_store
        }
    },
    watch:{
        cod_symbol:function(newval){
            this.get_variacion_semana_actual(newval)
        }
    },
    computed:{
        flg_var_positivo:function(){                        
            if (this.panel_cotizacion_semana_store.imp_variacion >= 0){
                return true
            }else{
                return false
            }
        }
    },
    mounted:function(){
        this.get_variacion_semana_actual(this.cod_symbol)
    },
    methods:{
        get_variacion_semana_actual:function(cod_symbol){
            if(cod_symbol == ""){
                return;
            }

            let variacionSemanal = new VariacionSemanal()
            
            //const now = new Date();
            let anyo = moment().year()
            let semana = moment().week()            
            
            let cod_semana = `${anyo}${_.padStart(semana,2,"0")}`


            let params = {
                cod_symbol: cod_symbol,
                cod_semana: cod_semana
            }            

            let request = variacionSemanal.get_variacion_semana_actual(params)
            request.then(response => {                
                console.log(response)                
                store.dispatch("incluir_httpresp_si_apperror", response)
                let httpdata = response.data                
                let apppdata = httpdata.data                
                //update store
                panel_cotizacion_semana_store.fill_variacion_semana_actual(apppdata)
            })            
        }
    }
}
</script>