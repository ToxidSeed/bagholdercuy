import Vue from 'vue'

import VueRouter from 'vue-router'
import PanelSimulationDataEntry from './components/PanelSimulationDataEntry.vue';
import PanelTradeList from './components/PanelTradeList.vue';
import PanelTrade from './components/PanelTrade.vue';
import PanelStats from './components/PanelStats.vue';
import DataLoader from './components/DataLoader.vue';
import PanelHoldings from './components/PanelHoldings.vue';
import PanelFunds from './components/Funds/PanelFunds.vue'
import MainPanelCurrencyExchange from './components/CurrencyExchange/MainPanelCurrencyExchange.vue';
import MainPanelCurrency from './components/MainPanelCurrency.vue';
import MainPanelSymbol from './components/Symbol/MainPanelSymbol.vue';
import PanelHistorialOperaciones from '@/components/Holdings/PanelHistorialOperaciones.vue';
import MainPanelHistorialOrdenes from '@/components/Ordenes/MainPanelHistorialOrdenes.vue'

Vue.use(VueRouter);

const routes =  [
    {
      path:'/', component:PanelSimulationDataEntry,     
    },{
      path:'/funds', component:PanelFunds
    },{
      path:'/currencyexchange', component:MainPanelCurrencyExchange
    },{
      path:'/tradelist', component:PanelTradeList
    },{
      path:'/trade', component:PanelTrade
    },{
      path:'/trade/:symbol/:asset_type/:trade_type', component:PanelTrade, props:true
    },{
      path:'/stats', component:PanelStats
    },{
      path:'/dataloader', component:DataLoader
    },{
      path:'/holdings', component:PanelHoldings
    },{
      path:'/historial_operaciones', component:PanelHistorialOperaciones
    },{
      path:'/currency', component:MainPanelCurrency
    },{
      path:"/symbols", component:MainPanelSymbol
    },{
      path:"/historial_ordenes", component:MainPanelHistorialOrdenes
    }
]

const router = new VueRouter({
  routes
})


export default router;