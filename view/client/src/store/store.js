import Vue from 'vue'
import Vuex from 'vuex'
import alerta from "./alerta"
import configuracion_alerta from "./configuracion-alerta"
Vue.use(Vuex);

export default new Vuex.Store({
    modules:{
        alerta,
        configuracion_alerta
    },
    state:{
        messagebox:{
            open: false,            
            httpresponses: [],
            msgs: []
        }        
    },
    actions:{
        incluir_httpresp_si_apperror: function(context, payload){
            let appdata = payload.data
            if (appdata.success == false){
                context.commit("abrir_messagebox")
                context.commit("httpresp", payload)
            }
        },
        incluir_httpresp: function(context, payload){            
            let httpresp = payload            
            context.commit("abrir_messagebox")
            context.commit("httpresp", httpresp)
        },
        incluir_msg: function(context, payload){
            context.commit("abrir_messagebox")
            context.commit("message", payload)
        }
    },
    mutations:{
        message:function(state, payload){                                    
            state.messagebox.msgs.push(payload)
        },
        httpresp: function(state, payload){                        
            state.messagebox.httpresponses.push(payload)
        },
        abrir_messagebox:function(state){
            state.messagebox.open = true
        },
        cerrar_messagebox:function(state){            
            state.messagebox.open = false
            state.messagebox.httpresponses = []
            state.messagebox.msgs = []
        }
    }    
});
    