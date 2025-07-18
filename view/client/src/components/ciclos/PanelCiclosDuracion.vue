<template>
    <div>
        <q-bar  class="bg-white">
            <div class="text-blue-10 q-pr-md">Duración</div>
            <q-separator vertical/>
            <q-btn dense flat icon="search" color="blue-10" @click="btn_buscar_click"/>
            <q-btn dense flat icon="fas fa-object-group" color="purple" @click="btn_vista_agrupada_click(!vistaAgrupada)"/>
        </q-bar>
        <q-card flat v-if="localStore.state.filtros_aplicados.cod_symbol != ''">            
            <q-card-section>
                {{localStore.state.filtros_aplicados.cod_symbol}} - {{localStore.state.filtros_aplicados.extdata.nom_symbol}}
            </q-card-section>
        </q-card>
        <q-separator/>       
        <div  class="row justify-center" v-show="vistaAgrupada==false" style="height: 500px;">                        
            <div id="ciclosNegativosChart" class="col-6" style="height: 500px;" >                
            </div>              
        </div>
        <div style="height: 300px;" v-show="vistaAgrupada==true" class="row justify-center">
            <div id="ciclosChart"></div>
        </div>
        <q-separator/>       
        <div class="row">
            <q-table
            title="Ciclos Negativos"
            title-class="text-blue-10"
            table-header-class="text-blue-10"
            :data="stats_neg"
            :columns="columns_neg"
            row-key="index"
            separator="vertical"
            dense
            class="col"
            flat
            :pagination="pagination"
            />
            <q-separator vertical/>
            <q-table
            table-header-class="text-blue-10"
            title="Ciclos Positivos"
            title-class="text-blue-10"
            :data="stats_pos"
            :columns="columns_pos"
            row-key="index"
            separator="vertical"
            dense
            class="col-6"
            flat
            :pagination="pagination"
            />
            
            
        </div>
        <q-separator/>
        <WinBuscarCiclos v-model="WinBuscarCiclosOpen" @btn-buscar-click="WinBuscarCiclos_btn_buscar_click"/>
    </div>
</template>
<script>
import * as echarts from 'echarts';
import WinBuscarCiclos from './WinBuscarCiclos.vue';
import ciclos_store ,{chartDuracionDiasCicloOption} from "./ciclos-store.js"

import { CicloService } from '../../api/ciclo';
import store from "@/store/store"
import date from 'date-and-time'

export default {
    name:"PanelCiclosDuracion",
    components:{
        WinBuscarCiclos
    },
    data(){
        return {
            localStore: ciclos_store,
            WinBuscarCiclosOpen: false,
            chartDuracionDiasCicloOption: chartDuracionDiasCicloOption,
            chartDomCiclosPositivos: null,
            chartCiclosPositivos:null,
            chartDomCiclosNegativos:null,
            chartCiclosNegativos:null,
            chartDomCiclos:null, 
            chartCiclos:null,
            option:{},
            pagination:{
                rowsPerPage:15
            },
            columns_pos:[
                {
                name: 'index',                
                label: 'Metrica',
                align: 'left',
                field: "index"
                },
                {
                name: 'num_series',                
                label: 'N. series',
                align: 'left',
                field: "num_series"
                }
            ],
            columns_neg:[
                {
                name: 'index',                
                label: 'Metrica',
                align: 'left',
                field: "index"
                },
                {
                name: 'num_series',                
                label: 'N. series',
                align: 'left',
                field: "num_series"
                }
            ],            
            data_pos: [],
            data_neg: [],
            stats_pos: [],
            stats_neg: [],
            ciclos:[],
            vistaAgrupada: false
        }
    },
    watch:{
        data_pos:function(newval){
            console.log(newval)
            this.setOptionPos(newval)
        },
        data_neg:function(newval){
            console.log(newval)
            this.setOptionNeg(newval)
        },
        ciclos:function(newval){
            this.setOptions(newval)
        }
    },
    mounted:function(){
        //console.log("mounted echarts")
        //this.chartDomCiclosPositivos = document.getElementById('ciclosPositivosChart');
        //this.chartCiclosPositivos = echarts.init(this.chartDomCiclosPositivos);

        this.chartDomCiclosNegativos = document.getElementById('ciclosNegativosChart')
        this.chartCiclosNegativos = echarts.init(this.chartDomCiclosNegativos);                

        this.chartDomCiclos = document.getElementById('ciclosChart');              
        this.chartCiclos = echarts.init(this.chartDomCiclos, null, {height:300, width:1500});
        
    },
    methods:{
        btn_buscar_click:function(){            
            this.WinBuscarCiclosOpen = true
        },
        WinBuscarCiclos_btn_buscar_click: function(evtData){
            
            evtData.fch_desde = date.transform(evtData.fch_desde,"DD/MM/YYYY",'YYYY-MM-DD')
            evtData.fch_hasta = date.transform(evtData.fch_hasta,"DD/MM/YYYY",'YYYY-MM-DD')
            CicloService.get_ciclos_diarios(evtData).then(httpresp => {
                store.dispatch("incluir_httpresp_si_apperror", httpresp)
                const httpdata = httpresp.data
                if (httpdata.success == true){
                    this.WinBuscarCiclosOpen = false
                    const appdata = httpdata.data                    
                    chartDuracionDiasCicloOption.series[0].data = appdata.ciclos_neg.map(item => item.num_series*-1)
                    chartDuracionDiasCicloOption.series[1].data = appdata.ciclos_pos.map(item => item.num_series)
                    console.log(chartDuracionDiasCicloOption)
                    this.chartCiclosNegativos.clear()
                    this.chartCiclosNegativos.setOption(chartDuracionDiasCicloOption)
                    //console.log(appdata)

                    this.stats_neg = appdata.stats_neg
                    this.stats_pos = appdata.stats_pos
                    /*                                        
                    this.stats_neg = appdata.stats_neg
                    this.stats_pos = appdata.stats_pos
                    this.data_pos = appdata.ciclos_pos
                    this.data_neg = appdata.ciclos_neg
                    this.ciclos = appdata.ciclos
                    */
                }       
            })
            
           console.log(evtData)
        },
        setOptionPos:function(ciclos_pos){
            let xAxisData = []
            let series = []

            for (const elem of ciclos_pos){
                xAxisData.push(elem.num_ciclo)
                series.push({
                        value: elem.num_series,
                        itemStyle: {
                            color: '#91cc75'
                        }
                })
            }
            let option = {
                xAxis: {
                    type:'category',
                    data:xAxisData
                },
                yAxis: {
                    type: 'value'
                },
                series:{
                    data: series,
                    type: 'bar'
                }
            }
            this.chartCiclosPositivos.setOption(option);
        },
        setOptionNeg:function(ciclos_neg){
            console.log(ciclos_neg)
            let xAxisDataNegativos = []
            let seriesData = []

            for (const elem_neg of ciclos_neg){
                xAxisDataNegativos.push(elem_neg.num_ciclo)
                seriesData.push({
                    value: elem_neg.num_series,
                    itemStyle: {
                        color: '#ee6666'
                    }
                })
            }

            let option_ciclos_negativos = {
                xAxis: {
                    type:'category',
                    data:xAxisDataNegativos
                },
                yAxis: {
                    type: 'value'
                },
                series:{
                    data: seriesData,
                    type: 'bar'
                }
            }
            console.log(option_ciclos_negativos)
            this.chartCiclosNegativos.setOption(option_ciclos_negativos);
        },
        setOptions:function(ciclos){                        
            let xAxisData = []
            let seriesData = []
            for (const elem of ciclos){
                xAxisData.push(elem.num_ciclo)
                seriesData.push({
                    value: elem.num_series,
                    itemStyle: {
                        color: (elem.flg_ciclo_positivo == false? '#ee6666' : '#91cc75')
                    }
                })
            }
            let options = {
                xAxis: {
                    type:'category',
                    data:xAxisData
                },
                yAxis: {
                    type: 'value'
                },
                series:{
                    data: seriesData,
                    type: 'bar'
                }
            }    
            console.log(options)        
            this.chartCiclos.setOption(options)            
        },
        btn_vista_agrupada_click:function(flg_vista_agrupada){            
            this.vistaAgrupada = flg_vista_agrupada
            if (flg_vista_agrupada == true){                
                
                this.setOptions(this.ciclos)
            }else{
                this.setOptionPos(this.data_pos)
                this.setOptionNeg(this.data_neg)
            }
        }        
    }
}
</script>