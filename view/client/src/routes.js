import Vue from 'vue'

import VueRouter from 'vue-router'
import PanelSimulationDataEntry from './components/PanelSimulationDataEntry.vue';
import PanelTradeList from './components/PanelTradeList.vue';
import PanelTrade from './components/PanelTrade.vue';
import PanelStats from './components/PanelStats.vue';
import DataLoader from './components/DataLoader.vue';
import PanelHoldings from './components/PanelHoldings.vue';

Vue.use(VueRouter);

const routes =  [
    {
      path:'/', component:PanelSimulationDataEntry,     
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
    }
]

const router = new VueRouter({
  routes
})


export default router;