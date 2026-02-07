import ComentarioAlerta from "@/api/comentario-alerta"
import GestorObjeto from '@/common/gestor-objeto'

export default {
    state:{
        abierto:false,
        comentario_alerta:{
            id_alerta:"",
            id_comentario_alerta:"",
            dsc_comentario:""
        },
        cod_symbol:""
    },
    agregar: function(id_alerta, aux){
        this.state.abierto = true
        new GestorObjeto(this.state.comentario_alerta).reset()

        //inicializamos
        this.state.comentario_alerta.id_alerta = id_alerta   

        let aux_obj = new GestorObjeto(aux)
        this.state.cod_symbol = aux_obj.get_elemento("cod_symbol")
    },
    abrir:function(id_alerta, aux){
        this.state.abierto = true
        this.state.comentario_alerta.id_alerta = id_alerta   

        let aux_obj = new GestorObjeto(aux)
        this.state.cod_symbol = aux_obj.get_elemento("cod_symbol")
    },
    registrar: async function(){
        await ComentarioAlerta.registrar(this.state.comentario_alerta)
    },
    cerrar:function(){
        this.state.abierto = false
    }
}