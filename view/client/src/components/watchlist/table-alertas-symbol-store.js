import Alerta from "@/api/alerta"
import Cotizacion from "@/api/cotizacion"
import GestorObjeto from "@/common/gestor-objeto"

export default {
    state:{
        title:"",
        id_monitoreo:"",
        id_symbol:"",
        id_contrato_opcion:null,
        cod_symbol:"",
        nom_symbol:"",
        fch_vencimiento:null,
        dias_expiracion:null,
        tipo_opcion:null,
        imp_strike:null,
        imp_accion:0,
        cotizacion:{

        },
        data:[],
        tmp_data:[]
    },
    set_symbol: function(param){
        this.state.id_monitoreo = param.id_monitoreo || ""
        this.state.id_symbol = param.id_symbol
        this.state.id_contrato_opcion = param.id_contrato_opcion || null
        this.state.cod_symbol = param.cod_symbol
        this.state.nom_symbol = param.nom_symbol
        this.state.fch_vencimiento = param.fch_vencimiento || null
        this.state.dias_expiracion = param.dias_expiracion !== undefined ? param.dias_expiracion : null
        this.state.tipo_opcion = param.tipo_opcion || null
        this.state.imp_strike = param.imp_strike !== undefined ? param.imp_strike : null
    },
    limpiar: function(){
        this.state.title = ""
        this.state.id_monitoreo = ""
        this.state.id_symbol = ""
        this.state.id_contrato_opcion = null
        this.state.cod_symbol = ""
        this.state.nom_symbol = ""
        this.state.fch_vencimiento = null
        this.state.dias_expiracion = null
        this.state.tipo_opcion = null
        this.state.imp_strike = null
        this.state.imp_accion = 0
        this.state.cotizacion = {}
        this.state.data = []
        this.state.tmp_data = []
    },
    fetch_data: async function(params){         
        this.state.imp_accion = 0
        this.state.data = []

        let param_obj = new GestorObjeto(params)
        if (param_obj.get_elemento("id_config_alerta") == ""){
            return
        }
        
        this.state.tmp_data = await Alerta.get_alertas_x_configuracion(params) 
        this.state.data = this.state.tmp_data       

        let cotizacion = await Cotizacion.get_cotizacion(this.state.cod_symbol)                                
        this.state.imp_accion = cotizacion ? cotizacion.imp_cierre : null        

        let idx_break = -1

        if (cotizacion && cotizacion.imp_cierre !== null && cotizacion.imp_cierre !== undefined) {
            for (let element of this.state.tmp_data){                        
                if (element.imp_alerta >=  cotizacion.imp_cierre){
                    idx_break = idx_break + 1        
                    continue
                }else{                
                    break
                }            
            }
        }        

        let idx_limite_superior = idx_break - 10
        let idx_limite_inferior = idx_break + 10        
        
        this.state.data = this.state.tmp_data.filter((element, index) => {        
            if (index > idx_limite_superior && index <= idx_limite_inferior ){
                return true
            }else{
                return false
            }
        })

        for (let element of this.state.data){            
            let imp_diff_alerta = (element.imp_alerta - cotizacion.imp_cierre).toFixed(3)
            element.imp_diff_alerta = imp_diff_alerta > 0? `+${imp_diff_alerta}` : `${imp_diff_alerta}`            
        }        
    }
}

