import Vue from 'vue'
import { BASE_PATH } from './common/constants'
import axios from 'axios'

import VueRouter from 'vue-router'
//import PanelSimulationDataEntry from './components/PanelSimulationDataEntry.vue';
import PanelTradeList from './components/PanelTradeList.vue';
import PanelTrade from './components/PanelTrade.vue';
import PanelStats from './components/PanelStats.vue';
import DataLoader from './components/DataLoader.vue';
import MainPanelHoldings from './components/Holdings/MainPanelHoldings.vue';
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
import PanelVariacionDiaria from '@/components/informes/PanelVariacionDiaria.vue';

//Rentabilidad operaciones
import PanelRentabilidadOperaciones from '@/components/informes/PanelRentabilidadOperaciones.vue';
//import TableRentabilidadOperacionesDiaria from '@/components/informes/TableRentabilidadOperacionesDiaria.vue';
import PanelRentabilidadOperacionesDiaria from '@/components/informes/PanelRentabilidadOperacionesDiaria.vue';
import MainRentabilidadOperacionesMensual from '@/components/operaciones/rentabilidadoperaciones/MainRentabilidadOperacionesMensual.vue';
import MainRentabilidadOperacionesSemanal from '@/components/operaciones/rentabilidadsemanal/MainRentabilidadOperacionesSemanal.vue';
import MainRentabilidadOperacionesAnual from '@/components/operaciones/rentabilidadanual/MainRentabilidadOperacionesAnual.vue';

import PanelMantOpciones from '@/components/MantOpciones/PanelMantOpciones.vue'
import DataLoaderOptions from '@/components/DataLoaderOptions.vue'
import PanelOpcionCargaFichero from '@/components/MantOpciones/PanelOpcionCargaFichero.vue'

import MainMantSerie from '@/components/serie/MainMantSerie.vue'
import PanelDeposit from '@/components/Funds/PanelDeposit.vue'
import PanelWithdraw from '@/components/Funds/PanelWithdraw.vue'
import PanelRecalcularFondos from '@/components/Funds/PanelRecalcularFondos.vue'
import PanelCurrencyConversion from '@/components/Funds/PanelCurrencyConversion.vue'
import PanelLogin from '@/components/PanelLogin.vue'
import PanelReorganizarFondos from '@/components/Funds/PanelReorganizarFondos.vue'
import PanelCurrencyExchangeRate from '@/components/CurrencyExchange/PanelCurrencyExchangeRate.vue';
import PanelCurrencyExchangeRateLoader from '@/components/CurrencyExchange/PanelCurrencyExchangeRateLoader.vue'

import TableVariacionSemanal from '@/components/informes/TableVariacionSemanal.vue';
import PanelEvolucionSemanal from '@/components/informes/PanelEvolucionSemanal.vue'

//Configuracion
import PanelCalendarioSemanalLoader from '@/components/Configuracion/PanelCalendarioSemanalLoader.vue'
import PanelCalendarioDiarioLoader from '@//components/Configuracion/PanelCalendarioDiarioLoader.vue'

//
import PanelBroker from '@/components/broker/PanelBroker.vue'
import MainBroker from '@/components/broker/MainBroker.vue'
//Cuenta
import PanelCuenta from '@/components/cuenta/PanelCuenta.vue'
import MainCuenta from '@/components/cuenta/MainCuenta.vue'

//Usuario
import PanelUsuario from '@/components/usuario/PanelUsuario.vue'
import MainUsuario from '@/components/usuario/MainUsuario.vue'

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
            path:'/currencyexchange', 
            component:MainPanelCurrencyExchange,
            name:"currencyexchange",
            props:true,
            children:[
              {
                path:"nuevo",
                name:"currencyexchange-nuevo",
                component:PanelCurrencyExchangeRate,
                meta: {size:30},
                props:{inFirstPanelSize:50}
              },{
                path:"loader",
                name:"currencyexchange-loader",
                component:PanelCurrencyExchangeRateLoader
              }
            ]
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
            path:'/holdings', 
            name:'holdings',
            component:MainPanelHoldings,
            children:[{
              path:'trade',
              name:'holdings-trade',
              component:PanelTrade
            }

            ]
          },{
            path:'/historial_operaciones', component:PanelHistorialOperaciones
          },{
            path:'/currency', component:MainPanelCurrency
          },{
            path:'/currency/:action=:moneda_id', component:MainPanelCurrency, props:true
          },{
            path:'/calendariosemanalloader', component:PanelCalendarioSemanalLoader, props:true,
            name:"calendario-semanal-loader"
          },{
            path:'/calendariodiarioloader', component: PanelCalendarioDiarioLoader, props: true,
            name:'calendario-diario-loader'            
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
                component:PanelMantOpciones,
                props:true
              },{
                path:"mant/edit/:id",
                name:"opciones-edit",
                component:PanelMantOpciones
              },{
                path:"loader",
                name:"opciones-loader",
                component:DataLoaderOptions
              },{
                path:"loader/fichero",
                name:"opciones-loader-fichero",
                component:PanelOpcionCargaFichero
              }
            ]
          },{
            path:"/reorganizarorden",component:PanelReorganizar
          },{
            path:"/variacionmensual",component:PanelVariacionMensual
          },{
            path:"/variacionsemanal",component:PanelVariacionSemanal,
            children:[
              {
                path:"",
                name:"variacion-semanal-series",
                props:true,
                component: TableVariacionSemanal
              },{
                path:"evolucion",
                name:"variacion-semanal-evolucion",
                props:true,
                component: PanelEvolucionSemanal
              }
            ]
          },{
            path:"/variaciondiaria",component:PanelVariacionDiaria
          },{
            path:"/rentabilidadoperaciones", component:PanelRentabilidadOperaciones,
            name:"rentabilidad-operaciones",
            children:[
              {
                path:"",
                name:"rentabilidad-operaciones-diaria",
                props:true,
                component: PanelRentabilidadOperacionesDiaria
              },
              {
                path:"/rentabilidadoperaciones/mensual",
                name:"rentabilidad-operaciones-mensual",
                props:true,
                component: MainRentabilidadOperacionesMensual
              },
              {
                path:"/rentabilidadoperaciones/anual",
                name:"rentabilidad-operaciones-anual",
                props:true,
                component: MainRentabilidadOperacionesAnual
              },
              {
                path:"/rentabilidadoperaciones/semanal",
                name:"rentabilidad-operaciones-semanal",
                props:true,
                component: MainRentabilidadOperacionesSemanal
              }
            ]
          },{
            path:"/series",
            component:MainMantSerie
          },{
            path:"/broker",
            name:"broker",
            component:MainBroker,
            props:true,
            children:[
              {
                path:"new",
                name:"broker-new",
                component:PanelBroker
              },
              {
                path:"ver/:id_broker",
                name:"broker-ver",
                props:true,
                component:PanelBroker
              },
              {
                path:"editar/:id_broker",
                name:"broker-editar",
                props:true,
                component:PanelBroker
              }
            ]
          },{
            path:"/cuenta",
            name:"cuenta",
            component: MainCuenta,
            props:true,
            children:[
              {
                path:"nuevo",
                name:"cuenta-nuevo",
                component:PanelCuenta
              },
              {
                path:"ver",
                name:"cuenta-ver/:id_cuenta",
                props:true,
                component:PanelCuenta
              },
              {
                path:"editar",
                name:"cuenta-editar/:id_cuenta",
                props:true,
                component:PanelCuenta
              }
            ]
          },
          {
            path:"/usuario",
            name:"usuario",
            component:MainUsuario,
            props:true,
            children:[
              {
                path:"nuevo",
                name:"usuario-nuevo",
                props:true,
                component: PanelUsuario                
              },
              {
                path:"ver/:id_usuario",
                name:"usuario-ver",
                props:true,
                component: PanelUsuario                
              },
              {
                path:"configurar/:id_usuario",
                name:"usuario-config",
                props:true,
                component: PanelUsuario
              }
            ]
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

router.beforeEach(async(to, from, next) => {
  let token = localStorage.getItem('token')
  //console.log(token)
  let token_valido = await validar_token(token)  

  if (token_valido != true){      
    if (to.name != 'login'){
      next({ name: 'login' })      
    }    
    next()        
  }
  
  if (to.name == 'login'){    
    next({name:'main'})      
  }
  next()
})

async function validar_token(token){
  if (token == null || token == undefined){
    return false
  }

  const http = axios.create({
    baseUrl:BASE_PATH    
  })

  const response = await http.post('/auth/LoginController/validar_token',{
    token:token
  })

  let data = response.data 

  if (data.expired == true){    
    localStorage.removeItem('token')
    return false
  }

  return true
}

export default router;