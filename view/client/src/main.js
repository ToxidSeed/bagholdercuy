import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import './quasar'

import router from '@/routes.js';
Vue.config.productionTip = false
Vue.prototype.$http = axios
Vue.prototype.$backend_url = "http://127.0.0.1:5000/bagholdercuy/"

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
