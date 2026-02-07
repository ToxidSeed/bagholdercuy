export const chartDuracionDiasCicloOption = {  
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "shadow",
    },
  },
  legend: {
    data: ["ciclos_neg", "ciclos_pos"],
  },
  grid: {
    left: "3%",
    right: "4%",
    bottom: "3%",
    containLabel: true,
  },
  xAxis: [
    {
      type: "value",
    },
  ],
  yAxis: [
    {
      type: "category",
      axisTick: {
        show: false,
      },
      data: [],
    },
  ],
  series: [
    {
      name: "ciclos_neg",
      type: "bar",
      stack: "Total",
      label: {
        show: true,
        position: "left",
      },
      emphasis: {
        focus: "series",
      },
      itemStyle: {
        color: "#f44336",
      },
      data: []
    },
    {
      name: "ciclos_pos",
      type: "bar",
      stack: "Total",
      label: {
        show: true,
        position: "right",
      },
      emphasis: {
        focus: "series",
      },
      itemStyle: {
        color: "#388e3c",
      },
      data: []
    }
  ]
};

export default {
  state: {
    win_buscar_ciclos: {
      open: false,
      cod_symbol: "",
      nom_symbol: "",
      fch_desde: "",
      fch_hasta: "",
    },
    filtros_aplicados: {
      cod_symbol: "",
      fch_desde: "",
      fch_hasta: "",
      extdata: {
        nom_symbol: "",
      },
    },
    data_stats_pos: [],
    data_stats_neg: [],
    ciclos_pos: [],
    ciclos_neg: [],
    ciclos: [],
    vista_agrupada: false,
  },
};
