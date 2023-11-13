import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex);

export default new Vuex.Store({
    state:{
        messages:{
            open:false,
            data:[]
        }
    },
    mutations:{
        set_message:function(state, httpresp){
            state.messages.data.push(httpresp)
        }
    }    
});
