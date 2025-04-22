<template>
    <div>
        <q-toolbar>
            <q-btn flat round dense icon="menu" color="blue-10"></q-btn>
            <q-toolbar-title class="text-blue-10">Metricas</q-toolbar-title>
        </q-toolbar>
        <q-separator/>
        <!--
        <q-toolbar>
            <q-btn flat class=" text-blue-10" icon="grain" @click="metricas.state.win_criterios_metricas.open=true" no-caps>Criterios generales</q-btn>            
        </q-toolbar>
        -->

        <q-card flat class="q-pl-md q-pb-md">
            <div class="q-pt-xs text-blue-10 text-subtitle1 row">                
                <q-btn icon="expand_less" flat round dense/>
                <div>Criterios generales</div>                                                
            </div>            
            
            <q-toolbar class="text-green-10 col-12">
                <q-btn label="Generar" no-caps flat dense icon="build" @click="btn_generar_click" />
            </q-toolbar>       
            <q-separator/>            
            <div class="row">
                <div>
                    <div class="col-3">                
                        <SelectSymbol v-on:select-symbol="select_symbol"/>
                    </div>                
                    <div class="col-12 q-pt-xs">
                        <span class="text-subtitle1 text-blue-10">
                            {{ metricas.state.panel_metricas.cod_symbol }}
                        </span>
                        <span>
                            {{ metricas.state.panel_metricas.nom_symbol }}
                        </span>
                    </div>
                </div>
                <q-separator vertical class="q-ml-md q-mr-md"/>
                <div>
                    <div class="q-gutter-sm">
                        <q-radio v-model="cod_tipo_periodo" val="dias" label="Dias" color="blue-10"/>
                        <q-radio v-model="cod_tipo_periodo" val="semanas" label="Semanas" color="blue-10"/>
                        <q-radio v-model="cod_tipo_periodo" val="meses" label="Meses" color="blue-10"/>
                        <q-radio v-model="cod_tipo_periodo" val="anyos" label="Años" color="blue-10"/>
                    </div>
                    <q-btn icon="menu" flat color="blue-10" :label="rango_seleccionado.nombre" no-caps>
                        <q-menu>
                            <q-list dense style="min-width: 150px">
                                <q-item clickable v-close-popup class="text-body2" 
                                v-for="item in rangos_periodo" :key="item.codigo"
                                @click="sel_rango(item)"
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
                </div>
            </div>                       
        </q-card>
        
        <div>
            <q-list bordered class="rounded borders">
                <q-expansion-item
                    default-opened
                    expand-separator         
                    switch-toggle-side           
                    class="text-subtitle1"                                        
                >
                    <template v-slot:header>                        
                        <q-item-section>
                            <div class="row">
                                <div class="text-blue-10">
                                    Metricas variacion diaria
                                </div>          
                                <!--
                                <q-separator vertical spaced/>                                                      
                                <div>
                                    <span class="text-blue-10">Periodo: </span>
                                    <span class="text-subtitle1">{{ metricas.state.panel_metricas.fch_desde }}</span> - <span class="text-subtitle1">{{ metricas.state.panel_metricas.fch_hasta }}</span>                                    
                                </div>
                                -->
                            </div>
                        </q-item-section>                    
                    </template>
                    <q-separator/>                                                                              
                    <div class="row q-col-xs">                                                        
                        <TableMetricasVariacionPositiva class="col-6"/>
                        <q-separator vertical/>
                        <TableMetricasVariacionNegativa class="col"/>
                    </div>
                </q-expansion-item>                
                <q-expansion-item
                    default-opened
                    expand-separator  
                    switch-toggle-side                                       
                    class="text-subtitle1"                                        
                >
                    <template v-slot:header>
                        <q-item-section avatar class="text-blue-10">
                            Metricas variacion semanal
                        </q-item-section> 
                    </template>     
                    <q-separator/>
                    <q-card>                                    
                    <div class="row">
                        <PanelCotizacionSemana :cod_symbol="metricas.state.panel_metricas.cod_symbol"/>                            
                    </div>        
                    <q-separator/>             
                    <div class="row q-col-xs">                                                        
                        <TableMetricasSemanalVariacionPositiva class="col-6"/>
                        <q-separator vertical/>
                        <TableMetricasSemanalVariacionNegativa class="col"/>
                    </div>  
                    </q-card>             
                </q-expansion-item>                
                <q-expansion-item
                    default-opened
                    expand-separator     
                    switch-toggle-side                
                    class="text-subtitle1 text-blue-10"                                        
                >
                    <template v-slot:header>
                        <q-item-section avatar>
                            Metricas variacion Mensual
                        </q-item-section> 
                    </template>    
                    <q-separator/>                    
                    <div class="row q-col-xs">                                                        
                        <TableMetricasMensualVariacionPositiva class="col-6"/>
                        <q-separator vertical/>
                        <TableMetricasMensualVariacionNegativa class="col"/>
                    </div>
                </q-expansion-item>
            </q-list>        
        </div>        
    </div>
</template>

<script>
import PanelCotizacionSemana from "@/components/common/PanelCotizacionSemana.vue"
import SelectSymbol from "@/components/SelectSymbol.vue"
import TableMetricasVariacionPositiva from './TableMetricasVariacionPositiva.vue';
import TableMetricasVariacionNegativa from './TableMetricasVariacionNegativa.vue';
import TableMetricasSemanalVariacionNegativa from './TableMetricasSemanalVariacionNegativa.vue'
import TableMetricasSemanalVariacionPositiva from './TableMetricasSemanalVariacionPositiva.vue'
import TableMetricasMensualVariacionPositiva from './TableMetricasMensualVariacionPositiva.vue'
import TableMetricasMensualVariacionNegativa from './TableMetricasMensualVariacionNegativa.vue'
import metricas from "./metricas-store"
import store from "@/store/store"
import metrica_api from "@/api/metrica"
import {HttpResponseHandler} from "@/common/http-response-handler"
import date from 'date-and-time';
import _ from 'lodash';


export default {
    name:"PanelMetricas",
    components:{
    PanelCotizacionSemana,
    TableMetricasVariacionPositiva,
    TableMetricasVariacionNegativa,
    TableMetricasSemanalVariacionPositiva,
    TableMetricasSemanalVariacionNegativa,
    TableMetricasMensualVariacionPositiva,
    TableMetricasMensualVariacionNegativa,
    SelectSymbol
    },
    data(){
        return {
            metricas:metricas,
            cod_tipo_periodo:"dias",            
            rangos_tipo_periodo:{
                "dias":[
                    {
                        "codigo":"RANGOS_FECHAS",
                        "nombre":"Rangos de fechas"
                    },{
                        "codigo":"ULTIMOS_100_DIAS",
                        "nombre":"Ultimos 100 dias"
                    },{
                        "codigo":"ULTIMOS_365_DIAS",
                        "nombre":"Ultimos 365 dias"
                    },{
                        "codigo":"ANYO_EN_CURSO",
                        "nombre":"Año en curso"
                    }
                ]
            },
            rango_seleccionado:{
                "codigo":"",
                "nombre":"Seleccionar rango"
            },
            fch_desde:"",
            fch_hasta:""
        }
    },
    computed:{        
        rangos_periodo:function(){
            if (this.cod_tipo_periodo == ""){
                return [];
            }
            let rangos = this.rangos_tipo_periodo[this.cod_tipo_periodo]
            return rangos
        }
    },
    mounted:function(){        
        /*console.log(metricas)
        metricas.get_metricas({
            "cod_symbol": "NVDA",
            "fch_desde":"2023-11-01",
            "fch_hasta":"2023-11-30"
        })*/
    },
    methods:{
        calc_fechas_rango: function(rango_item){            
            if(rango_item.codigo == "ULTIMOS_100_DIAS"){
                const now = new Date();
                const fch_100_dias = date.addDays(now, -100)
                this.fch_hasta = date.format(now, "DD/MM/YYYY")
                this.fch_desde = date.format(fch_100_dias, "DD/MM/YYYY")                    
            }
        },
        sel_rango: function(rango){
            console.log(rango)
            if (this.cod_tipo_periodo == ""){
                return;
            }                                    
            this.rango_seleccionado = rango
            this.calc_fechas_rango(this.rango_seleccionado)
        },
        select_symbol: function(item){
            metricas.state.panel_metricas.cod_symbol = item.value
            metricas.state.panel_metricas.nom_symbol = item.label
        },
        abrir_criterios_metricas_diarias: function(){
            let state = metricas.state.panel_metricas
            if (state.cod_symbol == ""){
                store.dispatch("incluir_msg","Debe indicar los criterios generales")
                return;
            }
            metricas.state.win_criterios_metricas_diaria.cod_symbol = metricas.state.panel_metricas.cod_symbol
            metricas.state.win_criterios_metricas_diaria.open=true
        },
        abrir_criterios_metricas_semanal: function(){
            let state = metricas.state.panel_metricas
            if (state.cod_symbol == ""){
                store.dispatch("incluir_msg","Debe indicar los criterios generales")
                return;
            }            

            metricas.state.win_criterios_metricas_semanal.cod_symbol = metricas.state.panel_metricas.cod_symbol
            metricas.state.win_criterios_metricas_semanal.open=true
            console.log(metricas)
        },
        btn_generar_click: async function(){                                    
            this.get_metricas_diarias_de_cierres_positivos()
            this.get_metricas_diarias_de_cierres_negativos()
            this.get_metricas_semanales_de_cierres_positivos()            
            this.get_metricas_semanales_de_cierres_negativos()
            
            /*
            this.get_metricas_mensuales_de_cierres_positivos()
            this.get_metricas_mensuales_de_cierres_negativos()
            */
        },
        get_metricas_diarias_de_cierres_positivos: function(){
            let metrica_api_instance = new metrica_api()  
            let params = {
                cod_symbol: metricas.state.panel_metricas.cod_symbol,
                cod_tipo_periodo: this.cod_tipo_periodo
            }
            if (_.toUpper(this.cod_tipo_periodo) == "DIAS"){
                params.fch_desde = date.transform(this.fch_desde,"DD/MM/YYYY","YYYY-MM-DD")
                params.fch_hasta = date.transform(this.fch_hasta,"DD/MM/YYYY","YYYY-MM-DD")
            }

            let response_mdcp = metrica_api_instance.get_metricas_diarias_de_cierres_positivos(params)
            response_mdcp.then(httpresp => {
                HttpResponseHandler.showMessageIfError(httpresp)
                let httpdata = httpresp.data
                let appdata = httpdata.data
                let extradata = httpdata.extradata
                for (let element of appdata){                    
                    element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(3)                    
                    element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(3)
                    element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(3)
                    element.imp_var_max_min = element.imp_var_max_min.toFixed(3)
                    element.imp_var_max_cierre = element.imp_var_max_cierre.toFixed(3)
                    //element.imp_variacion_maximo_minimo = element.imp_variacion_maximo_minimo.toFixed(3)
                }
                metricas.state.table_metricas_var_positiva.data = appdata
                metricas.state.table_metricas_var_positiva.count = extradata.count
                metricas.state.table_metricas_var_positiva.total = extradata.total
                console.log(metricas.state.table_metricas_var_positiva)
            })
        },
        get_metricas_diarias_de_cierres_negativos: function(){            
            let metrica_api_instance = new metrica_api()

            let params = {
                cod_symbol: metricas.state.panel_metricas.cod_symbol,
                cod_tipo_periodo:this.cod_tipo_periodo
            }
            
            if (_.toUpper(this.cod_tipo_periodo) == "DIAS"){
                params.fch_desde = date.transform(this.fch_desde,"DD/MM/YYYY","YYYY-MM-DD")
                params.fch_hasta = date.transform(this.fch_hasta,"DD/MM/YYYY","YYYY-MM-DD")
            }

            let response_mdcn = metrica_api_instance.get_metricas_diarias_de_cierres_negativos(params)
            response_mdcn.then(httpresp => {
                HttpResponseHandler.showMessageIfError(httpresp)
                let httpdata = httpresp.data
                let appdata = httpdata.data
                let extradata = httpdata.extradata

                for (let element of appdata){
                    element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(3)                    
                    element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(3)
                    element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(3)
                    element.imp_var_min_max = element.imp_var_min_max.toFixed(3)
                    element.imp_var_min_cierre = element.imp_var_min_cierre.toFixed(3)
                }
                metricas.state.table_metricas_var_negativa.data = appdata
                metricas.state.table_metricas_var_negativa.count = extradata.count
                metricas.state.table_metricas_var_negativa.total = extradata.total
            })
        },
        get_metricas_semanales_de_cierres_positivos: function(){
            let params = {
                cod_symbol: metricas.state.panel_metricas.cod_symbol,
                cod_tipo_periodo:this.cod_tipo_periodo
            }

            if (_.toUpper(this.cod_tipo_periodo) == "DIAS"){
                params.fch_desde = date.transform(this.fch_desde,"DD/MM/YYYY","YYYY-MM-DD")
                params.fch_hasta = date.transform(this.fch_hasta,"DD/MM/YYYY","YYYY-MM-DD")
            }

            let metrica_api_instance = new metrica_api()
            let response_mscp = metrica_api_instance.get_metricas_semanales_de_cierres_positivos(params)
            response_mscp.then(httpresp => {
                HttpResponseHandler.showMessageIfError(httpresp)
                let httpdata = httpresp.data
                let appdata = httpdata.data
                let extradata = httpdata.extradata

                for (let element of appdata){
                    element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(3)                    
                    element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(3)
                    element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(3)
                    element.imp_var_max_min = element.imp_var_max_min.toFixed(3)
                    element.imp_var_max_cierre = element.imp_var_max_cierre.toFixed(3)
                }
                metricas.state.table_metricas_semanal_var_positiva.data = appdata
                metricas.state.table_metricas_semanal_var_positiva.count = extradata.count
                metricas.state.table_metricas_semanal_var_positiva.total = extradata.total                
            })
        },
        get_metricas_semanales_de_cierres_negativos: function(){
            let params = {
                cod_symbol: metricas.state.panel_metricas.cod_symbol,
                cod_tipo_periodo:this.cod_tipo_periodo
            }

            if (_.toUpper(this.cod_tipo_periodo) == "DIAS"){
                params.fch_desde = date.transform(this.fch_desde,"DD/MM/YYYY","YYYY-MM-DD")
                params.fch_hasta = date.transform(this.fch_hasta,"DD/MM/YYYY","YYYY-MM-DD")
            }

            let metrica_api_instance = new metrica_api()
            let response_mscp = metrica_api_instance.get_metricas_semanales_de_cierres_negativos(params)
            response_mscp.then(httpresp => {
                HttpResponseHandler.showMessageIfError(httpresp)
                let httpdata = httpresp.data
                let appdata = httpdata.data
                let extradata = httpdata.extradata

                for (let element of appdata){
                    element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(3)                    
                    element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(3)
                    element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(3)
                    element.imp_var_min_max = element.imp_var_min_max.toFixed(3)
                    element.imp_var_min_cierre = element.imp_var_min_cierre.toFixed(3)
                }
                metricas.state.table_metricas_semanal_var_negativa.data = appdata
                metricas.state.table_metricas_semanal_var_negativa.count = extradata.count
                metricas.state.table_metricas_semanal_var_negativa.total = extradata.total
            })
        },
        get_metricas_mensuales_de_cierres_positivos: function(){
            let metrica_api_instance = new metrica_api()
            let response = metrica_api_instance.get_metricas_mensuales_de_cierres_positivos({
                cod_symbol: metricas.state.panel_metricas.cod_symbol,
                cod_tipo_periodo:this.cod_tipo_periodo
            })
            response.then(httpresp => {
                HttpResponseHandler.showMessageIfError(httpresp)
                let httpdata = httpresp.data
                let appdata = httpdata.data
                let extradata = httpdata.extradata

                for (let element of appdata){
                    element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(3)                    
                    element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(3)
                    element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(3)
                    element.imp_var_max_min = element.imp_var_max_min.toFixed(3)
                    element.imp_var_max_cierre = element.imp_var_max_cierre.toFixed(3)
                }
                metricas.state.table_metricas_mensual_var_positiva.data = appdata
                metricas.state.table_metricas_mensual_var_positiva.count = extradata.count
                metricas.state.table_metricas_mensual_var_positiva.total = extradata.total
            })
        },
        get_metricas_mensuales_de_cierres_negativos: function(){
            let metrica_api_instance = new metrica_api()
            let response = metrica_api_instance.get_metricas_mensuales_de_cierres_negativos({
                cod_symbol: metricas.state.panel_metricas.cod_symbol,
                cod_tipo_periodo:this.cod_tipo_periodo
            })
            response.then(httpresp => {
                HttpResponseHandler.showMessageIfError(httpresp)
                let httpdata = httpresp.data
                let appdata = httpdata.data
                let extradata = httpdata.extradata

                for (let element of appdata){
                    element.imp_variacion_cierre = element.imp_variacion_cierre.toFixed(3)                    
                    element.imp_variacion_maximo = element.imp_variacion_maximo.toFixed(3)
                    element.imp_variacion_minimo = element.imp_variacion_minimo.toFixed(3)
                    element.imp_var_min_max = element.imp_var_min_max.toFixed(3)
                    element.imp_var_min_cierre = element.imp_var_min_cierre.toFixed(3)
                }
                metricas.state.table_metricas_mensual_var_negativa.data = appdata
                metricas.state.table_metricas_mensual_var_negativa.count = extradata.count
                metricas.state.table_metricas_mensual_var_negativa.total = extradata.total
            })
        }
    }
}
</script>