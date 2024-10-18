<template>
    <div>
        <q-card>
            <div id="chartdiv">
            </div>  
        </q-card>          
    </div>
</template>
<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import _ from "lodash";
//import MessageBox from '@/components/MessageBox.vue';
import {postconfig} from '@/common/request.js';
import {HttpResponseHandler} from "@/common/http-response-handler"
import date from "date-and-time";

export default {
    name:"ChartOHLCSeriesDiaria",
    components:{

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
            if (Object.keys(to.query).length > 0){                
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
            this.chart.padding(25, 25, 0, 15);
            this.chart.data = []
            
            //this.chart.leftAxesContainer.layout = "vertical";

            var dateAxis = this.chart.xAxes.push(new am4charts.DateAxis());            
            //dateAxis.renderer.grid.template.location = 0;
            
            
            dateAxis.baseInterval = {
                "timeUnit": "day",
                "count": 1
            }
            
            this.chart.dateFormatter.inputDateFormat = "dd/MM/yyyy"

            dateAxis.renderer.ticks.template.length = 8;
            dateAxis.renderer.ticks.template.strokeOpacity = 0.1;
            dateAxis.renderer.grid.template.disabled = true;
            dateAxis.renderer.ticks.template.disabled = false;
            dateAxis.renderer.ticks.template.strokeOpacity = 0.2;
            dateAxis.renderer.minLabelPosition = 0.01;
            dateAxis.renderer.maxLabelPosition = 0.99;
            dateAxis.keepSelection = true;
            dateAxis.minHeight = 30;
            //dateAxis.dateFormats.setKey("day","yyyy-MM-dd")
            //dateAxis.periodChangeDateFormats.setKey("day", "dd/MM/yyyy"); 

            

              console.log(dateAxis)
            var valueAxis = this.chart.yAxes.push(new am4charts.ValueAxis());
            valueAxis.tooltip.disabled = true;

            var series = this.chart.series.push(new am4charts.CandlestickSeries());
            series.dataFields.dateX = "fch_serie";
            series.dataFields.openValueY = "imp_apertura";
            series.dataFields.valueY = "imp_cierre";
            series.dataFields.lowValueY = "imp_minimo";
            series.dataFields.highValueY = "imp_maximo";
            series.simplifiedProcessing = true;
            series.tooltipText = "Open:${openValueY.value}\nLow:${lowValueY.value}\nHigh:${highValueY.value}\nClose:${valueY.value}";
            this.chart.cursor = new am4charts.XYCursor();
            /*
            series.dropFromOpenState.properties.fill = am4core.color("#8F3985");
            series.dropFromOpenState.properties.stroke = am4core.color("#8F3985");
            */

            series.riseFromOpenState.properties.fill = am4core.color("#07BEB8");
            series.riseFromOpenState.properties.stroke = am4core.color("#07BEB8");

        }
        ,
        filtrar:function(params){
            
            if (_.isEmpty(params)){
                return 
            }
            const now = new Date()
            let fch_hasta = date.format(now, "DD/MM/YYYY")
            let fch_desde = date.format(date.addYears(now, -1),"DD/MM/YYYY")

            this.$http.post(
                'SerieManager/SerieController/get_series_diarias',{
                    cod_symbol:params.cod_symbol,
                    fch_desde:fch_desde,
                    fch_hasta:fch_hasta                 
                },
                postconfig()
            ).then(httpresp => {
                console.log(httpresp)
                HttpResponseHandler.showMessageIfError(httpresp)
                
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