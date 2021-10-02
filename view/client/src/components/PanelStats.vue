<template>
    <div>
        <div class="q-ma-md text-h6">Stats</div>    
        <div class="hello" ref="chartdiv">
        </div>    
    </div>
</template>
<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

am4core.useTheme(am4themes_animated);

export default {
    name:"PanelStats",
    data:() =>{
        return {
            chart_close_change:null
        }
    },
    mounted:function(){
        this.chart_close_change = am4core.create(this.$refs.chartdiv, am4charts.XYChart);
        this.chart_close_change.data = []

        let categoryAxis = this.chart_close_change.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.renderer.labels.template.rotation = 90;
        categoryAxis.renderer.labels.template.verticalCenter = "middle";
        categoryAxis.renderer.labels.template.horizontalCenter = "left";

        categoryAxis.dataFields.category = "price_date";
        categoryAxis.renderer.grid.template.location = 0;
        categoryAxis.renderer.minGridDistance = 30;

        categoryAxis.renderer.labels.template.adapter.add("dy", function(dy, target) {
        if (target.dataItem && target.dataItem.index & 2 == 2) {
            return dy + 25;
        }
        return dy;
        });

        //let valueAxis = this.chart_close_change.yAxes.push(new am4charts.ValueAxis());
        this.chart_close_change.yAxes.push(new am4charts.ValueAxis());
        //console.log(valueAxis)

        // Create series
        let series = this.chart_close_change.series.push(new am4charts.ColumnSeries());
        series.dataFields.valueY = "close_pct";
        series.dataFields.categoryX = "price_date";
        series.name = "Change Close";
        series.columns.template.tooltipText = "{categoryX}: [bold]{valueY}[/]";
        series.columns.template.fillOpacity = .8;

        //load the data
        this.get_weekly_change();
    },
    methods:{
        get_weekly_change:function(){
            this.$http.post(
            this.$backend_url+'StatsManager/Change/close',{
                sim_params:this.sim_params
            }).then(httpresponse => {
                var response = httpresponse.data
                this.chart_close_change.data = response.data
            })
        }
    }

}
</script>
<style scoped>
.hello {
  width: 100%;
  height: 500px;
}
</style>