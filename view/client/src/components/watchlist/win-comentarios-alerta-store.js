import ComentarioAlerta from "@/api/comentario-alerta"

export default {
    state:{
        abierto:false,
        id_alerta:"",
        cod_symbol:"",
        imp_alerta:"",
        data:[]
    },
    abrir:async function(id_alerta, data){
        this.state.abierto = true
        this.state.id_alerta = id_alerta

        Object.assign(this.state, data)
        
        await this.fetch_data(id_alerta)
    },
    fetch_data: async function(id_alerta){
        this.state.data = await ComentarioAlerta.get_comentarios_x_alerta({id_alerta:id_alerta})                
    },
    eliminar: async function(id_comentario_alerta){
        await ComentarioAlerta.eliminar(id_comentario_alerta)
        await this.fetch_data(this.state.id_alerta)
    },
    cerrar:function(){
        this.state.abierto = false
        this.state.id_alerta = ""
        this.state.data = []
    }
}