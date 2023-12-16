<template>
    <div>
        <q-card>
            <div id="chartdiv">
            </div>  
        </q-card>  
        <MessageBox :config="msgbox"/>
    </div>
</template>
<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import MessageBox from '@/components/MessageBox.vue';
import {postconfig} from '@/common/request.js';

export default {
    name:"ChartEvolucionSemanal",
    components:{
        MessageBox
    },
    props:{
        infiltros:{
            type:Object,
            default: () => {}
        }        
    },
    data(){
        return {
            filtros:{},
            data:[],
            msgbox:{},
            chart:null,
            dateAxis:null
        }
    },
    watch:{        
        $route: function(to){
            console.log(to)
            if (Object.keys(to.query).length > 0){
                console.log("enter aqui")
                this.filtrar(to.query)
            }
        }
    },
    mounted:function(){        
        this.init()
    },
    methods:{
        init: function(){
            this.construir()
            this.filtrar(this.$route.query)
        },
        construir:function(){
            this.chart = am4core.create("chartdiv", am4charts.XYChart)
            this.chart.padding(5, 15, 0, 15);
            this.chart.data = []
            
            //this.chart.leftAxesContainer.layout = "vertical";

            var dateAxis = this.chart.xAxes.push(new am4charts.DateAxis());            
            //dateAxis.renderer.grid.template.location = 0;
            dateAxis.baseInterval = {
                "timeUnit": "day",
                "count": 1
            }
            dateAxis.renderer.ticks.template.length = 8;
            dateAxis.renderer.ticks.template.strokeOpacity = 0.1;
            //dateAxis.renderer.grid.template.disabled = true;
            //dateAxis.renderer.ticks.template.disabled = false;
            dateAxis.renderer.ticks.template.strokeOpacity = 0.2;
            dateAxis.renderer.minLabelPosition = 0.01;
            dateAxis.renderer.maxLabelPosition = 0.99;
            dateAxis.keepSelection = true;
            dateAxis.minHeight = 30;
            dateAxis.dateFormats.setKey("day","dd/MM/yyyy")
            dateAxis.periodChangeDateFormats.setKey("day", "dd/MM/yyyy"); 

            

            //  console.log(dateAxis)
            var valueAxis = this.chart.yAxes.push(new am4charts.ValueAxis());
            console.log(valueAxis)
            var series = this.chart.series.push(new am4charts.CandlestickSeries());
            series.dataFields.dateX = "fch_serie";
            series.dataFields.openValueY = "imp_apertura";
            series.dataFields.valueY = "imp_cierre";
            series.dataFields.lowValueY = "imp_minimo";
            series.dataFields.highValueY = "imp_maximo";

            /*
            series.dropFromOpenState.properties.fill = am4core.color("#8F3985");
            series.dropFromOpenState.properties.stroke = am4core.color("#8F3985");
            */

            series.riseFromOpenState.properties.fill = am4core.color("#07BEB8");
            series.riseFromOpenState.properties.stroke = am4core.color("#07BEB8");

        },
        filtrar:function(params){
            console.log("filtrar params")
            this.$http.post(
                'reportes/VariacionSemanalEvolucion/build',{
                    symbol:params.cod_symbol,
                    anyo:params.anyo,
                    semana:params.semana                    
                },
                postconfig()
            ).then(httpresp => {
                this.msgbox = {
                    httpresp:httpresp,
                    onerror:true
                }
                //this.data = httpresp.data.data         
                this.chart.data = httpresp.data.data         
            })
        }
    }
}
</script>
<style>
#chartdiv {  
  height: 400px;
  max-width: 100%;
}
</style>