<template>
    <div>
        <q-dialog v-model="open">
            <q-card style="width:400px;">
                <q-toolbar>
                    <q-toolbar-title class="text-blue-10">Buscar ciclos</q-toolbar-title>
                </q-toolbar>
                <q-card-section class="q-pt-none">
                    <SelectSymbol v-on:select-symbol="select_symbol"/>
                    <div>
                        <div class="q-pt-xs text-blue-10 text-h6">{{cod_symbol}}</div>
                        <div class="q-pt-xs text-body1">{{nom_symbol}}</div>
                    </div>
                    <q-btn icon="list" flat color="blue-10" :label="rango_seleccionado.nombre" no-caps>
                        <q-menu>
                            <q-list dense style="min-width: 150px">
                                <q-item clickable v-close-popup class="text-body2" 
                                v-for="item in rangos_fechas" :key="item.codigo"
                                @click="sel_rango(item.codigo)"
                                >
                                    <q-item-section>
                                        {{item.nombre}}
                                    </q-item-section>
                                </q-item>                                
                            </q-list>
                        </q-menu>
                    </q-btn>
                    <div class="row q-gutter-xs">
                        <q-input label="Fecha Desde" stack-label color="blue-10" dense placeholder="dd/mm/yyyy"  mask="##/##/####" v-model="fch_desde"/>
                        <q-input label="Fecha Hasta" stack-label color="blue-10" dense placeholder="dd/mm/yyyy" mask="##/##/####" v-model="fch_hasta"/>
                    </div>
                </q-card-section>
                <q-card-section align="right" class="q-gutter-xs">
                    <q-btn label="Buscar"  icon="search" size="sm" color="blue-10" @click="btn_buscar_click"></q-btn>
                    <q-btn label="Cancelar"  color="red-10" size="sm"  flat @click="open=false"></q-btn>
                </q-card-section>
            </q-card>
        </q-dialog>        
    </div>
</template>
<script>
import SelectSymbol from "@/components/SelectSymbol"
import date from "date-and-time"
//import { CicloService } from '../../api/ciclo';

export default {
    name:"WinBuscarCiclos",
    props:{
        value:{
            required:true
        }
    },
    components:{
        SelectSymbol
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
            rangos_fechas: [
                {
                    "codigo":"RANGOS_FECHAS",
                    "nombre":"Rangos de Fechas"
                },{
                    "codigo":"ULTIMOS_15_DIAS",
                    "nombre":"Últimos 15 días"
                },{
                    "codigo":"ULTIMOS_30_DIAS",
                    "nombre":"Últimos 30 días"
                },{
                    "codigo":"ULTIMOS_100_DIAS",
                    "nombre":"Ultimos 100 dias"
                },{
                    "codigo":"ULTIMOS_365_DIAS",
                    "nombre":"Últimos 365 dias"
                },{
                    "codigo":"ANYO_EN_CURSO",
                    "nombre":"Año en curso"
                }
            ],
            rango_seleccionado:{},
            cod_symbol:"",
            nom_symbol:"",
            fch_desde:"",
            fch_hasta:""
        }
    },
    mounted:function(){
        this.init()
    },
    methods:{
        init:function(){
            this.sel_rango("RANGOS_FECHAS")
        },  
        calc_fechas_rango: function(rango_item){            
            if(rango_item.codigo == "ULTIMOS_100_DIAS"){
                const now = new Date();
                const fch_100_dias = date.addDays(now, -100)
                this.fch_hasta = date.format(now, "DD/MM/YYYY")
                this.fch_desde = date.format(fch_100_dias, "DD/MM/YYYY")                    
            }else if(rango_item.codigo == "ULTIMOS_15_DIAS"){
                const now = new Date();
                const fch_15_dias = date.addDays(now, -15)
                this.fch_hasta = date.format(now, "DD/MM/YYYY")
                this.fch_desde = date.format(fch_15_dias, "DD/MM/YYYY")                    
            }else if(rango_item.codigo == "ULTIMOS_30_DIAS"){
                const now = new Date();
                const fch_dias = date.addDays(now, -30)
                this.fch_hasta = date.format(now, "DD/MM/YYYY")
                this.fch_desde = date.format(fch_dias, "DD/MM/YYYY")                    
            }
        },
        sel_rango:function(rango_codigo){
            for(const elem of this.rangos_fechas){
                if (elem.codigo == rango_codigo){
                    this.rango_seleccionado = elem
                    this.calc_fechas_rango(elem)
                    return
                }
            }
        },
        select_symbol: function(item){
            this.cod_symbol = item.value
            this.nom_symbol = item.label
        },
        btn_buscar_click:function(){
            /*
            this.localstore.buscar_ciclos(
                this.localstore.state.win_buscar_ciclos.cod_symbol, 
                this.localstore.state.win_buscar_ciclos.fch_desde,
                this.localstore.state.win_buscar_ciclos.fch_hasta
            )
            */
           this.$emit('btn-buscar-click', {
            "cod_symbol":this.cod_symbol,
            "nom_symbol": this.nom_symbol,
            "fch_desde": this.fch_desde,
            "fch_hasta": this.fch_hasta
           })
        }
    }
}
</script>