import {SET_MODEL} from "./mutation-types"
import axios from 'axios'
import {postconfig} from "@/common/request.js"

const ABRIR_GESTOR_ALERTA = "ABRIR_GESTOR_ALERTA"
const CERRAR_GESTOR_ALERTA = "CERRAR_GESTOR_ALERTA"


export default {
    namespaced:true,
    state:{
        win_gestor_alerta:{
            abierto:false,
            accion:"",
            id_config_alerta:""
        },
        model:{            
            id_config_alerta:"",
            id_monitoreo:"",
            id_cuenta:"",
            id_symbol:"",
            ctd_variacion_accion:"",
            ctd_ciclos:"",
            imp_inicio_ciclos:"",            
        }        
    },
    actions:{        
        async get_configuracion_alerta(context, payload){                        
            if (payload.id_config_alerta == ""){
                return
            }

            const httpresp = await axios.post("/configuracionalerta/ConfiguracionAlertaController/get_configuracion_alerta",{
                id_config_alerta: payload.id_config_alerta
            },postconfig())                        

            context.commit("message",{"httpresp":httpresp, "mostrar_si_error":true},{root:true})            
            let data = httpresp.data.data            
            context.commit("SET_MODEL", data)
        }
    },
    mutations:{
        [SET_MODEL](state, payload){                        
            state.model.id_config_alerta = payload.id_config_alerta
            state.model.id_monitoreo = payload.id_monitoreo
            state.model.id_cuenta = payload.id_cuenta
            state.model.id_symbol = payload.id_symbol
            state.model.ctd_variacion_accion = payload.ctd_variacion_titulo
            state.model.ctd_ciclos = payload.ctd_ciclos
            state.model.imp_inicio_ciclos = payload.imp_inicio_ciclos            
        },
        [ABRIR_GESTOR_ALERTA](state, payload){
            if (payload.id_config_alerta !== undefined){
                state.win_gestor_alerta.id_config_alerta = payload.id_config_alerta
                state.win_gestor_alerta.accion = "editar"                
            }

            state.win_gestor_alerta.abierto = true
        },
        [CERRAR_GESTOR_ALERTA](state){
            state.win_gestor_alerta.abierto = false
        }

    }
}