<template>
    <div>
    <q-table
        :data="data"
        :columns="columns"        
        row-key="fch_mes"
        dense
        :pagination="pagination"       
        separator="vertical" 
    >        
        <template v-slot:top>
            <div v-if="symbol_value != ''">
                <span class="text-blue-10 text-h6 q-pr-xs">{{ symbol_value }}</span><span class="text-body1">{{ symbol_nombre }}</span>
            </div>
            <div v-if="symbol_value == ''">
                <span class="text-body1 text-orange-10">Seleccionar instrumento financiero</span>
            </div>            
        </template>
        <template v-slot:header>
            <q-tr>
                <q-th colspan="7"></q-th>
                <q-th colspan="3">Variación</q-th>
                <q-th></q-th>              
                <q-th colspan="3">Porcentaje</q-th>
                <q-th></q-th>
            </q-tr>
            <q-tr>
                <q-th class="text-left" style="width:50px;">Año</q-th>                
                <q-th class="text-left" style="width:50px;">Fecha</q-th>
                <q-th class="text-right" style="width:50px;">Imp. Cierre anterior</q-th>
                <q-th class="text-right" style="width:50px;">Imp. Apertura</q-th>
                <q-th class="text-right" style="width:50px;">Imp. Maximo</q-th>
                <q-th class="text-right" style="width:50px;">Imp. Minimo</q-th>
                <q-th class="text-right" style="width:50px;">Imp. Cierre</q-th>
                <q-th class="text-right" style="width:50px;">Var. Cierre</q-th>
                <q-th class="text-right" style="width:50px;">Var. Maximo</q-th>
                <q-th class="text-right" style="width:50px;">Var. Minimo</q-th>  
                <q-th style="width:5px;"></q-th>              
                <q-th class="text-right" style="width:50px;">Pct. Cierre</q-th>
                <q-th class="text-right" style="width:50px;">Pct. Maximo</q-th>
                <q-th class="text-right" style="width:50px;">Pct. Minimo</q-th>                
                <q-th class="text-left"></q-th>
            </q-tr>
        </template>      
        <template v-slot:body="props">                        
            <q-tr :props="props" :class="props.row.num_dia_semana==1?'text-green text-bold':'text-black'">
                <q-menu
                    touch-position
                    context-menu
                    >
                    <q-list dense style="min-width: 100px" >
                        <q-item class="bg-blue-10 text-white text-body1" clickable v-close-popup @click="abrir_criterios_calculos_variacion_diaria(props.row)">
                            <q-item-section ><div class="q-pl-sm">Calcular variacion desde antiguedad</div></q-item-section>                                    
                        </q-item>                        
                    </q-list>
                </q-menu>                    
                <q-td key="anyo"  class="text-left">
                    {{props.row.anyo}}
                </q-td>                
                <q-td key="fch_serie" class="text-right">
                    {{props.row.fch_serie}}
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
                <q-td key="imp_variacion_cierre" v-bind:class="{'bg-green':props.row.imp_variacion_cierre >= 0,'bg-red':props.row.imp_variacion_cierre < 0,'text-right':true, 'text-white':true}">                    
                    {{props.row.imp_variacion_cierre}}
                </q-td>
                <q-td key="imp_variacion_maximo" :class="{'bg-green':props.row.imp_variacion_maximo >= 0,'bg-red':props.row.imp_variacion_maximo < 0,'text-right':true,'text-white':true}">
                    {{props.row.imp_variacion_maximo}}
                </q-td>
                <q-td key="imp_variacion_minimo" :class="{'bg-red':props.row.imp_variacion_minimo <= -1,'bg-orange':props.row.imp_variacion_minimo > -1,'text-white':true,'text-right':true}">
                    {{props.row.imp_variacion_minimo}}
                </q-td>
                <q-td></q-td>
                <q-td key="pct_variacion_cierre" :class="{'text-right':true}">                    
                    {{props.row.pct_variacion_cierre}}
                </q-td>            
                <q-td key="pct_variacion_maximo" :class="{'text-right':true}">                    
                    {{props.row.pct_variacion_maximo}}
                </q-td>                
                <q-td key="pct_variacion_minimo" :class="{'text-right':true}">                    
                    {{props.row.pct_variacion_minimo}}
                </q-td>                
                <q-td>                    
                </q-td>
            </q-tr>
            <q-inner-loading :showing="loading">
                <q-spinner-gears size="50px" color="blue-10" />
            </q-inner-loading>
        </template>        
    </q-table>    
    <WinSimulacionVariacionAntiguedad v-model="WinSimulacionVariacionAntiguedad.open"
    :cod_symbol="WinSimulacionVariacionAntiguedad.cod_symbol"
    :fch_final="WinSimulacionVariacionAntiguedad.fch_final"
    v-on:btn-aceptar-click="simular"
    />    
    </div>
</template>
<script>
import WinSimulacionVariacionAntiguedad from "@/components/variaciondiaria/WinSimulacionVariacionAntiguedad.vue"
import {postconfig} from '@/common/request.js'
export default {
    name:"TableVariacionDiaria",
    components:{
        WinSimulacionVariacionAntiguedad
    },
    props:{
        indata:{
            default: () => []
        },
        symbol_value:{
            type:String,
            default:""
        },
        symbol_nombre:{
            type:String,
            default:""
        },
        loading:{
            type:Boolean,
            default:true
        }
    },
    watch:{
        indata:function(newdata){
            this.data = newdata
        }
    },
    data: () => {
        return {
            filter:{
                symbol:"SOXL"
            },
            pagination:{
                rowsPerPage:24
            },
            data:[],            
            columns:[
                
            ],
            WinSimulacionVariacionAntiguedad:{
                open:false,
                cod_symbol:"",
                nom_symbol:"",
                fch_final:""
            }
        }
    },
    mounted:function(){
        this.init()
    },
    methods:{
        init:function(){
            if (this.indata.length > 0){
                this.data = this.indata                
            }
        },
        abrir_criterios_calculos_variacion_diaria:function(row){
            console.log(row)
            this.WinSimulacionVariacionAntiguedad.open = true
            this.WinSimulacionVariacionAntiguedad.cod_symbol = row.symbol
            this.WinSimulacionVariacionAntiguedad.fch_final = row.fch_serie            
        },
        simular:function(filtros){
            this.$http.post(
                "/SerieManager/SimulacionVariacionManager/simular",
                {
                    cod_symbol: filtros.cod_symbol,
                    fch_final: filtros.fch_final,
                    lista_dias_profundidad: JSON.stringify(filtros.lista_dias_profundidad)
                },postconfig()
            ).then(httpresp => {
                console.log(httpresp)
            })
        }
    }
}
</script>