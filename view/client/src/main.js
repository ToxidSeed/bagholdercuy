import Vue from 'vue'

import App from './App.vue'
import axios from 'axios'
import './quasar'
import { BASE_PATH } from './common/constants'
import store from './store/store.js'

import router from '@/routes.js';
Vue.config.productionTip = false
Vue.prototype.$http = axios
Vue.prototype.$http.defaults.baseURL = BASE_PATH



new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
