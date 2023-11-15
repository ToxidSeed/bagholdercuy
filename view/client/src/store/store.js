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
            open:false,
            data:[]
        }        
    },
    mutations:{
        message:function(state, payload){                                    
            //
            let mostrar_si_error = false            
            let httpresp = null
            //
            if ("mostrar_si_error" in payload)
                mostrar_si_error = payload.mostrar_si_error

            if ("httpresp" in payload){
                httpresp = payload.httpresp
            }

            //
            if (mostrar_si_error == false){                
                state.messagebox.data.push(payload.httpresp)
                state.messagebox.open = true                            
            }                        
            //
            if (mostrar_si_error == true){
                let appdata = httpresp.data
                if (appdata.success == false){
                    state.messagebox.data.push(payload.httpresp)
                    state.messagebox.open = true                            
                }
            }
        },
        cerrar_messagebox:function(state){            
            state.messagebox.open = false
            state.messagebox.data = []
        }
    }    
});
    