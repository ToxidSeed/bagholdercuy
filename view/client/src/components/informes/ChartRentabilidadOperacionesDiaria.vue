<template>
    <div>
        <q-card>
            <div id="chartdiv">
            </div>
        </q-card>
        <!--
        <MessageBox :config="msgbox"/>
        -->
    </div>
</template>
<script>
import {postconfig} from '@/common/request.js';
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
//import MessageBox from '@/components/MessageBox.vue';
//import {postconfig} from '@/common/request.js';

export default {
    name:"ChartRentabilidadOperacionesDiaria",
    components:{
        //MessageBox
    },
    data(){
        return {
            data:[            
            ],
            chart:null,
            dateAxis:null
        }
    },
    mounted:function(){
        this.construir()
    },
    methods:{
        construir:function(){
            this.chart = am4core.create("chartdiv", am4charts.XYChart)
            this.chart.padding(15, 15, 15, 15);            

            var categoryX = this.chart.xAxes.push(new am4charts.CategoryAxis());
            categoryX.dataFields.category = "fch_transaccion"
            
            //necesario definir ValueAxis
            var valueAxis = this.chart.yAxes.push(new am4charts.ValueAxis());
            console.log(valueAxis)
            
            //series
            var series = this.chart.series.push(new am4charts.ColumnSeries());
            series.dataFields.categoryX = "fch_transaccion";
            series.dataFields.valueY = "imp_rentabilidad";                             
            series.name = "Rentabilidad";
            series.columns.template.fillOpacity = .8;

            //
            this.get_rentabilidad_ult30dias()
        },
        get_rentabilidad_ult30dias:function(){
            this.$http.post(
                "/operacion/OperacionManager/get_rentabilidad_ult30dias",{},postconfig()
            ).then(httpresp => {
                this.msgbox = {
                    httpresp: httpresp,
                    onerror:true
                }

                let records = httpresp.data.data
                this.data = []
                for (let element of records){           
                    element.imp_rentabilidad = element.imp_rentabilidad.toFixed(2)         
                    this.data.push(element)
                }          
                this.chart.data = this.data 
            })
        }
    }
}
</script>