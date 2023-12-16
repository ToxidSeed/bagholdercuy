<template>
    <q-table
        :data="store.table_variacion_semanal.state.data"
        :columns="columns"        
        row-key="fch_serie"
        title="Variación Cierre"
        dense
        :pagination="pagination"       
        separator="vertical" 
    >
        <template v-slot:top>
            <div v-if="titulo_personalizado_visible">
                <span class="text-blue-10 text-h6 q-pr-xs">{{ store.table_variacion_semanal.state.filtros.cod_symbol }}</span>
                <span class="text-body1">{{ store.table_variacion_semanal.state.nom_symbol }}</span>
            </div>
            <div v-if="titulo_personalizado_visible == false">
                <span class="text-body1 text-orange-10">Seleccionar instrumento financiero</span>
            </div>            
        </template>
        <template v-slot:header>
            <q-tr>
                <q-th colspan="8"></q-th>
                <q-th colspan="3">Variación Cierre Ant</q-th>
                <q-th></q-th>
                <q-th colspan="3">Porcentaje (%)</q-th>
                <q-th></q-th>
            </q-tr>
            <q-tr>
                <q-th class="text-left" style="width:50px;">Año</q-th>
                <q-th class="text-left" style="width:50px;">Fecha</q-th>
                <q-th class="text-left" style="width:50px;">Semana</q-th>
                <q-th class="text-right" style="width:50px;">Imp. Cierre anterior</q-th>                                
                <q-th class="text-right" style="width:50px;">Imp. Apertura</q-th>                                
                <q-th class="text-right" style="width:50px;">Imp. Maximo</q-th>
                <q-th class="text-right" style="width:50px;">Imp. Minimo</q-th>
                <q-th class="text-right" style="width:50px;">Imp. Cierre</q-th>                
                <q-th class="text-right" style="width:50px;">Var. Cierre</q-th>
                <q-th class="text-right" style="width:50px;">Var. Máximo</q-th>
                <q-th class="text-right" style="width:50px;">Var. Mínimo</q-th>
                <q-th style="width:2px;"></q-th>
                <q-th class="text-right" style="width:50px;">Pct. Cierre</q-th>
                <q-th class="text-right" style="width:50px;">Pct. Máximo</q-th>
                <q-th class="text-right" style="width:50px;">Pct. Mínimo</q-th>
                <q-th class="text-left"></q-th>
            </q-tr>
        </template>
        <template v-slot:body="props">            
            <q-tr :props="props" @dblclick="abrir_evolucion_semanal(props.row)">
                <q-td key="anyo"  class="text-left">
                    {{props.row.anyo}}
                </q-td>
                <q-td key="fecha"  class="text-left">
                    {{props.row.fecha}}
                </q-td>
                <q-td key="semana" class="text-left">
                    {{props.row.semana}}
                </q-td>
                <q-td key="imp_cierre_ant" class="text-right">
                    {{props.row.imp_cierre_ant}}
                </q-td>          
                <q-td key="imp_apertura" class="text-right">
                    {{props.row.imp_apertura}}
                </q-td>                
                <q-td key="imp_maximo" class="text-right">
                    {{props.row.imp_maximo}}
                </q-td>                
                <q-td key="imp_minimo" class="text-right">
                    {{props.row.imp_minimo}}
                </q-td>                                
                <q-td key="imp_cierre" class="text-right">
                    {{props.row.imp_cierre}}
                </q-td>                                
                <q-td key="imp_variacion_cierre"  v-bind:class="{'bg-red':props.row.imp_variacion_cierre < 0,'bg-green':props.row.imp_variacion_cierre >= 0,'text-right':true,'text-white':true}">
                    {{props.row.imp_variacion_cierre}}
                </q-td>
                <q-td key="imp_variacion_maximo"  v-bind:class="{'bg-orange':props.row.imp_variacion_maximo >= 0 && props.row.imp_variacion_maximo < 1,'bg-green':props.row.imp_variacion_maximo >= 1, 'bg-red':props.row.imp_variacion_maximo < 0,'text-right':true,'text-white':true}">
                    {{props.row.imp_variacion_maximo}}
                </q-td>
                <q-td key="imp_variacion_minimo"  v-bind:class="{'bg-orange':props.row.imp_variacion_minimo > -1,'bg-red':props.row.imp_variacion_minimo <= -1,'text-right':true,'text-white':true}">
                    {{props.row.imp_variacion_minimo}}
                </q-td>
                <q-td></q-td>
                <q-td key="pct_variacion_cierre"  v-bind:class="{'bg-red':props.row.pct_variacion_cierre < 0,'bg-green':props.row.pct_variacion_cierre >= 0,'text-right':true,'text-white':true}">
                    {{props.row.pct_variacion_cierre}}
                </q-td>
                <q-td key="pct_variacion_maximo"  v-bind:class="{'bg-green':props.row.pct_variacion_maximo >= 0,'bg-red':props.row.pct_variacion_maximo < 0,'text-right':true,'text-white':true}">
                    {{props.row.pct_variacion_maximo}}
                </q-td>
                <q-td key="pct_variacion_minimo"  v-bind:class="{'bg-green':props.row.pct_variacion_minimo >= 0,'bg-red':props.row.pct_variacion_minimo < 0,'text-right':true,'text-white':true}">
                    {{props.row.pct_variacion_minimo}}
                </q-td>
                <q-td>                    
                </q-td>
            </q-tr>
        </template>
    </q-table>
</template>
<script>
//import date from 'date-and-time'
//import {CLIENT_DATE_FORMAT, ISO_DATE_FORMAT} from '@/common/constants.js'
//import {headers} from '@/common/common.js'
//import {postconfig} from '@/common/request.js';
import store from './store'

export default {
    name:"TableVariacionSemanal",
    props:{
        indata:{
            type:Array,
            default: () => []
        },
        infiltros:{
            type:Object,
            default: () => {}
        },
        symbol:{
            type:String,
            default:""
        },
        symbol_nombre: {
            type:String,
            default:""
        }
    },
    computed:{
        titulo_personalizado_visible:function(){            
            if (store.table_variacion_semanal.state.filtros.cod_symbol !== ""){
                return true
            }else{
                return false
            }
        }
    },
    watch:{        
        $route:function(newroute){     
            console.log("$route")       
            store.table_variacion_semanal.get_datos_variacion(newroute.query)
        }
    },
    data: () => {
        return {            
            pagination:{
                rowsPerPage:24
            },
            data:[],            
            columns:[],
            filtros:{
                symbol:"",
                symbol_nombre:""
            },
            store: store
        }
    },
    mounted:function(){
        //this.get_variacion_semanal()        
        this.init()
        
    },
    methods:{
        init:function(){                                    
            let filtros = this.$route.query     
            
            store.table_variacion_semanal.reset()
            store.table_variacion_semanal.set_filtros(
                this.$route.query
            )

            store.table_variacion_semanal.get_datos_variacion(filtros)
        },
        abrir_evolucion_semanal:function(row){       
            //console.log(row)     
            /*this.$router.push({name:'variacion-semanal-evolucion', params:{
                infiltros:{
                    symbol:row.symbol,
                    anyo:row.anyo,
                    semana:row.semana
                }
            }})*/
            this.$router.push({name:'variacion-semanal-evolucion', query:{
                cod_symbol:row.symbol,
                anyo: row.anyo,
                semana: row.semana
            }})
        }
    }
}
</script>