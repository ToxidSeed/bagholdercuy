<template>
  <div>
    <q-bar class="bg-white">
      <div class="text-blue-10 q-pr-md">Variación</div>
      <q-separator vertical />
      <q-btn dense flat icon="search" color="blue-10" @click="btn_buscar_click" />
    </q-bar>
    <q-card flat>
      <q-card-section>
        <!--
        <div class="row col justify-center" id="chartVariacionAbsoluta">
          No Data
        </div>
        <q-separator vertical />
        <div class="row col justify-center" id="chartVariacionPorcentaje">
          No Data
        </div>
        -->
        <div v-if="confirmedParams.cod_symbol">
          <span class="text-indigo">{{confirmedParams.cod_symbol}}</span>
           - {{confirmedParams.nom_symbol}} 
           | {{ confirmedParams.fch_desde}} - {{ confirmedParams.fch_hasta }}
           | Dia: 
        </div>
        <div class="row">
          <div class="col-6">
            <div id="chartVariacion" class="panel-variacion"></div>
          </div>
          <q-separator vertical />
          <div class="col">
            <div id="chartVariacionPct" class="panel-variacion-pct"></div>
          </div>

        </div>
      </q-card-section>
    </q-card>
    <WinBuscarCiclos v-model="winBuscarCiclosOpen" @btn-buscar-click="winBuscarCiclos_btnBuscarClick" />
  </div>
</template>
<script>
import WinBuscarCiclos from "./WinBuscarCiclos.vue";
import { CicloService } from "@/api/ciclo.js";
import date from "date-and-time"
import _ from "lodash"
import * as echarts from 'echarts';

export default {
  name: "PanelCiclosVariacion",
  components: {
    WinBuscarCiclos,
  },
  data() {
    return {
      winBuscarCiclosOpen: false,
      chartOptions: {
        title: {
          text: 'Variación de Cierre'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['var_neg', 'var_pos']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'value'
          }
        ],
        yAxis: [],
        series: []
      },
      chartOptionsPct: null,
      confirmedParams:{
        cod_symbol:'',
        nom_symbol:'',
        fch_desde:'',
        fch_hasta:''
      }
    }
  },
  methods: {
    btn_buscar_click: function () {
      this.winBuscarCiclosOpen = true;
    },
    winBuscarCiclos_btnBuscarClick(evt_data) {
      const params = {
        cod_symbol: evt_data.cod_symbol,
        fch_desde: date.transform(evt_data.fch_desde, 'DD/MM/YYYY', 'YYYY-MM-DD'),
        fch_hasta: date.transform(evt_data.fch_hasta, 'DD/MM/YYYY', 'YYYY-MM-DD')
      }
      //            
      this.confirmedParams.cod_symbol = evt_data.cod_symbol
      this.confirmedParams.nom_symbol = evt_data.nom_symbol
      this.confirmedParams.fch_desde = evt_data.fch_desde
      this.confirmedParams.fch_hasta = evt_data.fch_hasta

      const resp = CicloService.get_variacion_ciclos_diarios(params)
      resp.then(httpresp => {
        console.log(httpresp)
        const httpdata = httpresp.data
        const data = httpdata.data
        const ciclosNeg = data.df_ciclos_negativos.map(item => item.num_ciclo)
        const ciclosPos = data.df_ciclos_positivos.map(item => item.num_ciclo)
        const categoryData = _.sortBy([...ciclosNeg, ...ciclosPos])
        console.log(categoryData)
        this.refreshChartVariacion(data)
        this.refreshChartVariacionPct(data)
      })
    },
 
    refreshChartVariacion: function (data) {
      const options = {
        title: {
          text: 'Variación de Cierre'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['var_neg', 'var_pos']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'value'
          }
        ],
        yAxis: [
          {
            type: 'category',
            axisTick: {
              show: false
            },
            data: []
          }
        ],
        series: [
          {
            name: 'var_neg',
            type: 'bar',
            stack: 'Total',
            label: {
              show: true,
              position: 'left'
            },
            emphasis: {
              focus: 'series'
            },
            itemStyle: {
              color: '#f44336'
            },
            data: data.df_ciclos_negativos.map(item => item.imp_var_ciclo)
          },
          {
            name: 'var_pos',
            type: 'bar',
            stack: 'Total',
            label: {
              show: true,
              position: 'right'
            },
            emphasis: {
              focus: 'series'
            },
            itemStyle: {
              color: '#388e3c'
            },
            data: data.df_ciclos_positivos.map(item => item.imp_var_ciclo)
          }
        ]
      }
      this.myChart.clear()
      this.myChart.setOption(options)
    },
    refreshChartVariacionPct: function (data) {
      const options = {
        title: {
          text: 'Variación de Cierre %'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['pct_neg', 'pct_pos']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'value'
          }
        ],
        yAxis: [
          {
            type: 'category',
            axisTick: {
              show: false
            },
            data: []
          }
        ],
        series: [
          {
            name: 'pct_neg',
            type: 'bar',
            stack: 'Total',
            label: {
              show: true,
              position: 'left'
            },
            emphasis: {
              focus: 'series'
            },
            itemStyle: {
              color: '#f44336'
            },
            data: data.df_ciclos_negativos.map(item => item.pct_var_ciclo)
          },
          {
            name: 'pct_pos',
            type: 'bar',
            stack: 'Total',
            label: {
              show: true,
              position: 'right'
            },
            emphasis: {
              focus: 'series'
            },
            itemStyle: {
              color: '#388e3c'
            },
            data: data.df_ciclos_positivos.map(item => item.pct_var_ciclo)
          }
        ]
      }
      console.log(options)
      this.myChartPct.clear()
      this.myChartPct.setOption(options)
    }
  },
  mounted: function () {
    this.chartDom = document.getElementById('chartVariacion');
    this.myChart = echarts.init(this.chartDom);
    this.chartDomPct = document.getElementById('chartVariacionPct');
    this.myChartPct = echarts.init(this.chartDomPct);

    const options = {
      graphic: {
        type: 'text',
        left: 'center',
        top: 'middle',
        style: {
          text: 'No data available',
          fontSize: 20,
          fill: '#999',
        },
      }
    }

    const optionsPct = {
      graphic: {
        type: 'text',
        left: 'center',
        top: 'middle',
        style: {
          text: 'No data available',
          fontSize: 20,
          fill: '#999',
        },
      }
    }

    this.myChart.setOption(options)
    this.myChartPct.setOption(optionsPct)
  }
};
</script>
<style lang="scss" scoped>
.panel-variacion {  
  height: 800px;
}

.panel-variacion-pct {    
  height: 800px;
}
</style>