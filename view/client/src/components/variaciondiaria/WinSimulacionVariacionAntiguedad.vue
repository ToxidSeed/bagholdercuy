<template>
    <q-dialog v-model="open">    
        <q-card  style="min-width:1550px;">
            <q-toolbar>
                <q-toolbar-title class="text-blue-10">Criterios para el calculo de la varicion diaria</q-toolbar-title>
            </q-toolbar>
            <q-separator/>
            <q-card style="width:600px;">                                
                <q-card-actions align="left">
                    <q-btn label="Ejecutar" color="blue-10" @click="btn_aceptar_click"></q-btn>
                    <q-btn label="Cancelar" color="red-14" @click="open=false"></q-btn>
                </q-card-actions>
                <q-separator/>   
                <q-card-section>    
                    <div><span>Accion: </span><span class="text-blue-10 text-bold">{{cod_symbol}}</span><span>{{ nom_symbol }}</span></div>
                    <div>
                        <span>Fecha final: </span><span class="text-blue-10 text-bold">{{ fch_final }}</span>
                    </div>
                    <div class="row">
                        <div class="col-7">
                            <q-input stack-label label=""
                            v-model="txt_num_dias_profundidad" color="blue-10" hint="Numeros enteros mayores a 0 separados por comas"/>
                        </div>
                        <div class="col-5">
                            <q-btn icon="add" flat color="teal-10" class="text-capitalize" @click="btn_incluir_click">Añadir</q-btn>                                
                        </div>                        
                    </div>     
                    <div>
                        <q-chip removable color="blue-10" text-color="white" v-for="item in lista_dias_profundidad" :key="item" v-on:remove="eliminar_profundidad(item)">
                            {{ item }}
                        </q-chip>
                    </div>           
                </q-card-section>                
            </q-card>        
            <q-table
            :data="data"
            title=""
            :columns="columns"        
            row-key="fch_inicial"
            dense            
            :pagination="pagination"       
            separator="vertical" 
            wrap-cells
            >
            <template v-slot:header>
                <q-tr>
                    <q-th colspan="6"></q-th>
                    <q-th></q-th>
                    <q-th colspan="3" style="border-bottom-width:1px">Variación apertura</q-th>
                    <q-th></q-th>              
                    <q-th colspan="2" style="border-bottom-width:1px">Variación cierre </q-th>
                    <q-th></q-th>
                    <q-th></q-th>
                    <q-th></q-th>
                </q-tr>
                <q-tr>
                    <q-th class="text-left" style="width:50px;"><span class="text-bold">Fch inicial</span> ( fecha final - dias profundidad )</q-th>                
                    <q-th class="text-left" style="width:50px;">Dias de profundidad</q-th>
                    <q-th class="text-right" style="width:100px;"><span class="text-bold">Imp. Apertura</span> (en fecha inicial)</q-th>
                    <q-th class="text-right" style="width:100px;">Imp. Maximo</q-th>
                    <q-th class="text-right" style="width:100px;">Imp. Minimo</q-th>
                    <q-th class="text-right" style="width:100px;"><span class="text-bold">Imp. Cierre</span> (en fecha final)</q-th>
                    <q-th style="width:5px;"></q-th>
                    <q-th class="text-right" style="width:80px;">Imp. var maximo</q-th>
                    <q-th class="text-right" style="width:80px;">Imp. var minimo</q-th>
                    <q-th class="text-right" style="width:80px;">Imp. var cierre</q-th>                    
                    <q-th style="width:5px;"></q-th>              
                    <q-th class="text-right" style="width:80px;">Imp. var maximo</q-th>
                    <q-th class="text-right" style="width:80px;">Imp. var minimo</q-th>                                 
                    <q-th style="width:5px;"></q-th>              
                    <q-th class="text-center" style="width:100px;"><div>Variacion</div><div> maximo - minimo </div></q-th>                
                    <q-th></q-th>              
                </q-tr>
            </template>
            <template v-slot:body="props"> 
                <q-tr>
                    <q-td>{{props.row.fch_inicial}}</q-td>
                    <q-td>{{props.row.num_dias_profundidad}}</q-td>
                    <q-td class="text-right">{{props.row.imp_apertura}}</q-td>
                    <q-td class="text-right">{{props.row.imp_maximo}}</q-td>
                    <q-td class="text-right">{{props.row.imp_minimo}}</q-td>
                    <q-td class="text-right">{{props.row.imp_cierre}}</q-td>
                    <q-td></q-td>
                    <q-td class="text-right">{{props.row.imp_var_aper_maximo}}</q-td>
                    <q-td class="text-right">{{props.row.imp_var_aper_minimo}}</q-td>
                    <q-td class="text-right">{{props.row.imp_var_apertura_cierre}}</q-td>
                    <q-td></q-td>
                    <q-td class="text-right">{{props.row.imp_var_cierre_maximo}}</q-td>
                    <q-td class="text-right">{{props.row.imp_var_cierre_minimo}}</q-td>
                    <q-td></q-td>
                    <q-td class="text-right" >{{props.row.imp_var_minimo_maximo}}</q-td>
                    <q-td></q-td>
                </q-tr>
            </template>
            </q-table>
        </q-card>            
    </q-dialog>
</template>
<script>
import {postconfig} from '@/common/request.js'
export default {
    name:"WinSimulacionVariacionAntiguedad",
    props:{        
        value:{
            required:true
        },
        fch_final:{
            type:String,
            default:""
        },
        cod_symbol:{
            type:String,
            default:""
        },
        nom_symbol:{
            type:String,
            default:""
        }
    },
    watch:{
        open:function(newval){
            this.$emit('input',newval)
        },
        value:function(newval){
            this.open = newval
        }
    },
    data(){
        return {
            open:this.value,
            txt_num_dias_profundidad:"",            
            lista_dias_profundidad:[7,14,30,75,180,200],
            data:[],
            columns:[{
                label:"Fch. Inicial",
                align:"right",
                field:"fch_inicial",
                name:"fch_inicial",
                style:"width:100px;"      
            },{
                label:"N. dias profundidad",
                align:"right",
                field:"num_dias_profundidad",
                name:"num_dias_profundidad",
                style:"width:100px;"      
            },{
                label:"Imp. Apertura",
                align:"right",
                field:"imp_apertura",
                name:"imp_apertura",
                style:"width:100px;"      
            },{
                label:"Imp. Cierre (fecha final)",
                align:"right",
                field:"imp_cierre",
                name:"imp_cierre",
                style:"width:100px;"      
            },{
                label:"Imp. Maximo",
                align:"right",
                field:"imp_maximo",
                name:"imp_maximo",
                style:"width:100px;"      
            },{
                label:"Imp. Minimo",
                align:"right",
                field:"imp_minimo",
                name:"imp_minimo",
                style:"width:100px;"      
            },{
                label:"Imp. var apertura - cierre",
                align:"right",
                field:"imp_var_apertura_cierre",
                name:"imp_var_apertura_cierre",
                style:"width:100px;"      
            },{
                label:"Imp. var minimo - maximo",
                align:"right",
                field:"imp_var_minimo_maximo",
                name:"imp_var_minimo_maximo",
                style:"width:100px;"      
            },{
                label:"Imp. var apertura - maximo",
                align:"right",
                field:"imp_var_aper_maximo",
                name:"imp_var_aper_maximo",
                style:"width:100px;"      
            },{
                label:"Imp. var apertura - minimo",
                align:"right",
                field:"imp_var_aper_minimo",
                name:"imp_var_aper_minimo",
                style:"width:100px;"      
            },{
                label:"Imp. var cierre - maximo",
                align:"right",
                field:"imp_var_cierre_maximo",
                name:"imp_var_cierre_maximo",
                style:"width:100px;"      
            },{
                label:"Imp. var cierre - minimo",
                align:"right",
                field:"imp_var_cierre_minimo",
                name:"imp_var_cierre_minimo",
                style:"width:100px;"      
            },{
                label:"",
                field:"",
                name:""
            }],
            pagination:{
                rowsPerPage:24
            }
        }
    },
    methods:{        
        btn_incluir_click:function(){
            let lista = this.txt_num_dias_profundidad.split(",")
            lista = lista.map((elem) => parseInt(elem))
            this.lista_dias_profundidad = this.lista_dias_profundidad.concat(lista)
            this.lista_dias_profundidad = this.lista_dias_profundidad.sort((a,b) => {
                return a-b
            })
            
            //eliminado duplicados
            this.lista_dias_profundidad = this.lista_dias_profundidad.filter((elem, idx) => {
                let elem_anterior = this.lista_dias_profundidad[idx-1]
                if (elem == elem_anterior){
                    return false
                }else{
                    return true
                }
            })

        },
        btn_aceptar_click:function(){            
            /*this.$emit("btn-aceptar-click",{
                cod_symbol: this.cod_symbol,
                fch_final: this.fch_final,
                lista_dias_profundidad: this.lista_dias_profundidad
            })
            this.open = false*/
            this.simular({
                cod_symbol: this.cod_symbol,
                fch_final: this.fch_final,
                lista_dias_profundidad: this.lista_dias_profundidad
            })
        },
        eliminar_profundidad:function(param){            
            this.lista_dias_profundidad  = this.lista_dias_profundidad.filter(item => {                
                return item != param
            })            
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
                let appdata = httpresp.data
                for (let element of appdata.data){
                    element.imp_apertura = element.imp_apertura.toFixed(2)                    
                    element.imp_cierre = element.imp_cierre.toFixed(2)
                    element.imp_maximo = element.imp_maximo.toFixed(2)
                    element.imp_minimo = element.imp_minimo.toFixed(2)
                    element.imp_var_apertura_cierre = element.imp_var_apertura_cierre.toFixed(2)
                    element.imp_var_minimo_maximo = element.imp_var_minimo_maximo.toFixed(2)
                    element.imp_var_aper_maximo = element.imp_var_aper_maximo.toFixed(2)
                    element.imp_var_cierre_maximo = element.imp_var_cierre_maximo.toFixed(2)
                    element.imp_var_aper_minimo = element.imp_var_aper_minimo.toFixed(2)
                    element.imp_var_cierre_minimo = element.imp_var_cierre_minimo.toFixed(2)
                }
                this.data = appdata.data                
            })
        }
    }
}
</script>