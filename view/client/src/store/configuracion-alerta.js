import {SET_CONFIGURACION_ALERTA} from "./mutation-types"
import axios from 'axios'
import {postconfig} from "@/common/request.js"

const ABRIR_GESTOR_ALERTA = "ABRIR_GESTOR_ALERTA"
const CERRAR_GESTOR_ALERTA = "CERRAR_GESTOR_ALERTA"


export default {
    namespaced:true,
    state:{
        win_gestor_alerta:{
            abierto:false
        },
        configuracion_alerta:{            
            id_config_alerta:"",
            id_monitoreo:"",
            id_cuenta:"",
            id_symbol:"",
            ctd_variacion_accion:"",
            ctd_ciclos:"",
            imp_inicio_ciclos:""            
        }        
    },
    actions:{
        async editar_configuracion_alerta(context, payload){                        
            context.commit("ABRIR_GESTOR_ALERTA")
            let id_monitoreo = payload.id_monitoreo
            await context.dispatch("get_configuracion_alerta",{id_monitoreo:id_monitoreo})
            
        },
        async get_configuracion_alerta(context, payload){                        
            const httpresp = await axios.post("/configuracionalerta/ConfiguracionAlertaController/get_configuracion_alerta",{
                id_monitoreo: payload.id_monitoreo
            },postconfig())                        

            context.commit("message",{"httpresp":httpresp, "mostrar_si_error":true},{root:true})            
            let data = httpresp.data.data            
            context.commit("SET_CONFIGURACION_ALERTA", data)
        }
    },
    mutations:{
        [SET_CONFIGURACION_ALERTA](state, payload){                        
            state.configuracion_alerta.id_config_alerta = payload.id_config_alerta
            state.configuracion_alerta.id_monitoreo = payload.id_monitoreo
            state.configuracion_alerta.id_cuenta = payload.id_cuenta
            state.configuracion_alerta.id_symbol = payload.id_symbol
            state.configuracion_alerta.ctd_variacion_accion = payload.ctd_variacion_titulo
            state.configuracion_alerta.ctd_ciclos = payload.ctd_ciclos
            state.configuracion_alerta.imp_inicio_ciclos = payload.imp_inicio_ciclos            
        },
        [ABRIR_GESTOR_ALERTA](state){
            state.win_gestor_alerta.abierto = true
        },
        [CERRAR_GESTOR_ALERTA](state){
            state.win_gestor_alerta.abierto = false
        }

    }
}