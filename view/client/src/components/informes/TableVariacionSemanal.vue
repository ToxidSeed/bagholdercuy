<template>
    <q-table
        :data="data"
        :columns="columns"        
        row-key="fch_serie"
        title="Variación Cierre"
        dense
        :pagination="pagination"       
        separator="vertical" 
    >
        <template v-slot:top>
            <div v-if="filtros.symbol != ''">
                <span class="text-blue-10 text-h6 q-pr-xs">{{ filtros.symbol }}</span><span class="text-body1">{{ filtros.symbol_nombre }}</span>
            </div>
            <div v-if="filtros.symbol == ''">
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
import {postconfig} from '@/common/request.js';

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
    watch:{
        indata:function(newdata){
            console.log("indata")
            console.log(newdata)
            this.data = newdata
        },
        infiltros:function(newval){                        
            this.filtros.symbol = newval.symbol_value            
            this.filtros.symbol_nombre = newval.symbol_text
            console.log(this.filtros)
            this.filtrar()
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
            }
        }
    },
    mounted:function(){
        //this.get_variacion_semanal()
        console.log('mounted-table-variacion-semanal')
        this.init()
        
    },
    methods:{
        init:function(){
            if (this.indata.length > 0){
                this.data = this.indata
                console.log(this.data)
            }
        },
        filtrar:function(){
            this.$http.post(
                '/reportes/VariacionSemanalBuilder/build',{
                    symbol: this.filtros.symbol
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
        abrir_evolucion_semanal:function(row){       
            console.log(row)     
            this.$router.push({name:'variacion-semanal-evolucion', params:{
                infiltros:{
                    symbol:row.symbol,
                    anyo:row.anyo,
                    semana:row.semana
                }
            }})
        }
    }
}
</script>