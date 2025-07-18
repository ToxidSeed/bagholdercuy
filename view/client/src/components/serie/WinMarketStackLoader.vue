<template>
    <div>        
        <q-dialog v-model="open">
            <q-card style="width:450px;">
                <q-toolbar>
                    <q-toolbar-title class="text-h6 text-blue-10">
                    Carga de Series desde MarketStack
                    </q-toolbar-title>
                </q-toolbar>
                <q-separator/>                
                <q-card-section>
                    <SelectSymbol  v-on:select-symbol="select_symbol"/>
                    <div class="col-12 q-pt-xs">
                        <span class="text-subtitle1 text-blue-10">
                            {{ cod_symbol }}
                        </span>
                        <span>
                            {{ nom_symbol }}
                        </span>
                    </div>
                    <div>
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
                    </div>
                    <div class="row q-gutter-xs">
                        <q-input label="Fecha Desde" stack-label color="blue-10" dense placeholder="dd/mm/yyyy"  mask="##/##/####" v-model="fch_desde"/>
                        <q-input label="Fecha Hasta" stack-label color="blue-10" dense placeholder="dd/mm/yyyy" mask="##/##/####" v-model="fch_hasta"/>
                    </div>
                    <q-select color="blue-10" v-model="modo_carga" :options="lista_modos_carga" label="Modo de Escritura" stack-label/>                                                
                </q-card-section>            
                <q-inner-loading :showing="loading">
                    <q-spinner-gears size="50px" color="primary" />
                </q-inner-loading>
                <q-card-actions align="right">
                    <q-btn flat @click="procesar" no-caps color="blue-10" icon="play_arrow">Procesar</q-btn>
                    <q-btn flat v-close-popup no-caps icon="close" color="red-10">Cerrar</q-btn>
                </q-card-actions>
            </q-card>  
        </q-dialog>      
    </div>
</template>
<script>
import SelectSymbol from "@/components/SelectSymbol.vue"
import Serie from '@/api/serie'
import date from 'date-and-time'
import store from "@/store/store"

export default {
    name:"WinMarketStackLoader",
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
            open: this.value,
            fichero:null,
            cod_symbol:"",
            nom_symbol:"",
            modo_carga:"Agregar",
            fch_desde:"",
            fch_hasta:"",
            loading: false,
            lista_modos_carga:["Agregar","Reemplazar"],
            rangos_fechas: [
                {
                    "codigo":"RANGOS_FECHAS",
                    "nombre":"Rangos de Fechas"
                },{
                    "codigo":"ULTIMOS_7_DIAS",
                    "nombre":"Ultimos 7 dias"
                },{
                    "codigo":"ULTIMOS_30_DIAS",
                    "nombre":"Últimos 30 dias"
                },{
                    "codigo":"ULTIMOS_100_DIAS",
                    "nombre":"Últimos 100 dias"
                },{
                    "codigo":"ANYO_EN_CURSO",
                    "nombre":"Año en curso"
                }
            ],
            rango_seleccionado:{"codigo":"ULTIMOS_7_DIAS","nombre":"Ultimos 7 dias"}
        }
    },
    mounted:function(){
        this.sel_rango(this.rango_seleccionado.codigo)
    },
    methods:{        
        sel_rango:function(rango_codigo){
            
            for(const elem of this.rangos_fechas){
                if(elem.codigo == rango_codigo){
                    this.rango_seleccionado = elem
                }
            }

            let fch_desde=null, fch_hasta=null

            switch (rango_codigo) {
                case 'ULTIMOS_7_DIAS':
                    [fch_desde, fch_hasta] = this.calc_ultimos_n_dias(7)
                    break;
                case 'ULTIMOS_30_DIAS':
                    [fch_desde, fch_hasta] = this.calc_ultimos_n_dias(30)
                    break;
                case 'ULTIMOS_100_DIAS':
                    [fch_desde, fch_hasta] = this.calc_ultimos_n_dias(100)
                    break;
                default:
                    break;
            }
            console.log(fch_desde)
            console.log(fch_hasta)
            this.fch_desde = fch_desde
            this.fch_hasta = fch_hasta
        },
        calc_ultimos_n_dias:function(n_dias){
            const now = new Date()
            const fch_desde = date.format(date.addDays(now, n_dias * -1), "DD/MM/YYYY")
            const fch_hasta = date.format(now, "DD/MM/YYYY")
            return [fch_desde, fch_hasta]
        },
        select_symbol:function(symbol){
            this.cod_symbol = symbol.value
            this.nom_symbol = symbol.label
        },
        procesar:function(){
            const params = {
                cod_symbol: this.cod_symbol,
                fch_desde: date.transform(this.fch_desde, "DD/MM/YYYY","YYYY-MM-DD")  ,
                fch_hasta: date.transform(this.fch_hasta, "DD/MM/YYYY","YYYY-MM-DD"),
                modo_carga: this.modo_carga
            }            

            const api_serie = new Serie()
            api_serie.load_marketstack_series(params).then(resp => {
                store.dispatch("incluir_httpresp", resp)
            })
        }
    }
}
</script>