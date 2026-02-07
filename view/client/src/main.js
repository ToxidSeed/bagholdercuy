import Vue from 'vue'

import App from './App.vue'
import axios from 'axios'
import './quasar'
//import { BASE_PATH } from './common/constants'
import store from './store/store.js'
import router from '@/routes.js';

async function initApp() {
  Vue.config.productionTip = false
  Vue.prototype.$http = axios
  Vue.prototype.$http.defaults.baseURL = process.env.VUE_APP_SERVICE_BASE_URL


  //await store.dispatch('serverConstants/getList')


  new Vue({
    router,
    store,
    render: h => h(App),
  }).$mount('#app')
}

initApp()

