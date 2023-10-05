<template>
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
            <q-tr :props="props">
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
        </template>
    </q-table>
</template>
<script>

export default {
    name:"TableVariacionMensual",
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
                
            ]
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
        }
    }
}
</script>