import Vue from 'vue'

import VueRouter from 'vue-router'
//import PanelSimulationDataEntry from './components/PanelSimulationDataEntry.vue';
import PanelTradeList from './components/PanelTradeList.vue';
import PanelTrade from './components/PanelTrade.vue';
import PanelStats from './components/PanelStats.vue';
import DataLoader from './components/DataLoader.vue';
import PanelHoldings from './components/PanelHoldings.vue';
import MainPanelFunds from './components/Funds/MainPanelFunds.vue'
import MainPanelCurrencyExchange from './components/CurrencyExchange/MainPanelCurrencyExchange.vue';
import MainPanelCurrency from './components/MainPanelCurrency.vue';
import MainPanelSymbol from './components/Symbol/MainPanelSymbol.vue';
import PanelHistorialOperaciones from '@/components/Holdings/PanelHistorialOperaciones.vue';
import MainPanelHistorialOrdenes from '@/components/Ordenes/MainPanelHistorialOrdenes.vue';
import MainMantOpciones from '@/components/MantOpciones/MainMantOpciones.vue';
import PanelReorganizar from '@/components/Holdings/PanelReorganizar.vue';
import PanelVariacionMensual from '@/components/informes/PanelVariacionMensual.vue';
import PanelVariacionSemanal from '@/components/informes/PanelVariacionSemanal.vue';
import PanelMantOpciones from '@/components/MantOpciones/PanelMantOpciones.vue'
import DataLoaderOptions from '@/components/DataLoaderOptions.vue'
import MainMantSerie from '@/components/serie/MainMantSerie.vue'
import PanelDeposit from '@/components/Funds/PanelDeposit.vue'
import PanelWithdraw from '@/components/Funds/PanelWithdraw.vue'
import PanelRecalcularFondos from '@/components/Funds/PanelRecalcularFondos.vue'
import PanelCurrencyConversion from '@/components/Funds/PanelCurrencyConversion.vue'
import PanelLogin from '@/components/PanelLogin.vue'
import PanelReorganizarFondos from '@/components/Funds/PanelReorganizarFondos.vue'
import Main from '@/Main.vue'

Vue.use(VueRouter);

const routes =  [
    {
      path:'/', component:Main,     
      name:"main",
      children:[
          {
            path:'/funds', component:MainPanelFunds,
            name:"funds",
            children:[
              {
                path:"deposito",
                name:"funds-deposito",
                component:PanelDeposit
              },        
              {
                path:"retiro",
                name:"funds-retiro",
                component:PanelWithdraw
              },
              {
                path:"conversion",
                name:"funds-conversion",
                component:PanelCurrencyConversion
              },
              {
                path:"recalcularfondos",
                name:"funds-recalcular",
                component:PanelRecalcularFondos
              },{
                path:"reorganizarfondos",
                name:"funds-reorganizar",
                component:PanelReorganizarFondos
              }
            ]
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
            path:'/currency/:action=:moneda_id', component:MainPanelCurrency, props:true
          },{
            path:'/currency/:action', component:MainPanelCurrency, props:true
          },{
            path:"/symbols", component:MainPanelSymbol
          },{
            path:"/historial_ordenes", component:MainPanelHistorialOrdenes
          },{
            path:"/opciones", component:MainMantOpciones,
            name:"opciones",
            props:true,
            children:[
              {
                path:"mant/new",
                name:"opciones-new",
                component:PanelMantOpciones
              },{
                path:"mant/edit/:id",
                name:"opciones-edit",
                component:PanelMantOpciones
              },{
                path:"loader",
                name:"opciones-loader",
                component:DataLoaderOptions
              }
            ]
          },{
            path:"/reorganizarorden",component:PanelReorganizar
          },{
            path:"/variacionmensual",component:PanelVariacionMensual
          },{
            path:"/variacionsemanal",component:PanelVariacionSemanal
          },{
            path:"/series",
            component:MainMantSerie
          }
      ]         
    },{
      path:"/login",
      name:"login",
      component:PanelLogin
    }
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  let logeado = localStorage.getItem('logeado')  
  
  if (
    // make sure the user is authenticated
    !logeado &&
    // ❗️ Avoid an infinite redirect
    to.name !== 'login'
  ) {    
    // redirect the user to the login page
    next({ name: 'login' })
  }else{
    next()
  }
})

export default router;