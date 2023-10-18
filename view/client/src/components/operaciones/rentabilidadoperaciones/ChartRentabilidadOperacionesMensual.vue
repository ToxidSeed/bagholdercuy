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
    name:"ChartRentabilidadOperacionesMensual",
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
            categoryX.dataFields.category = "desc_mes_transaccion"
            
            //necesario definir ValueAxis
            var valueAxis = this.chart.yAxes.push(new am4charts.ValueAxis());
            console.log(valueAxis)
            
            //series
            var series = this.chart.series.push(new am4charts.ColumnSeries());
            series.dataFields.categoryX = "desc_mes_transaccion";
            series.dataFields.valueY = "imp_rentabilidad";                             
            series.name = "Rentabilidad";

            //
            series.columns.template.fillOpacity = .8;
            series.columns.template.adapter.add("fill", function(fill, target){
                console.log(fill)
                //console.log(target)
                //console.log(target.dataItem)
                console.log(target.dataItem.values.valueY)
                if (target.dataItem.values.valueY.value < 0){
                    return "red"
                }else{
                    return "green"                    
                }
            })

            //
            this.get_rentabilidad_mensual()
        },
        get_rentabilidad_mensual:function(){
            this.$http.post(
                "/operacion/OperacionManager/get_rentabilidad_mensual",{
                    id_cuenta: localStorage.getItem("id_cuenta")
                },postconfig()
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