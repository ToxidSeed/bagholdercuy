<template>
    <q-dialog v-model="winGestionComentariosAlertaStore.state.abierto">                
        <q-card style="width:400px;">
            <q-toolbar>
                <q-toolbar-title class="text-blue-10">Gestion de comentarios de alertas</q-toolbar-title>
            </q-toolbar>
            <q-separator/>
            <q-card-section>              
                <q-input label="Comentario" color="blue-10"  type="textarea" stack-label 
                v-model="winGestionComentariosAlertaStore.state.comentario_alerta.dsc_comentario" filled>

                </q-input>                  
            </q-card-section>
            <q-separator/>
            <q-card-actions align="right">
                <q-btn label="Guardar" dense flat class="text-capitalize" color="blue-10" @click="btn_aceptar_click"></q-btn>
                <q-btn label="Cancelar" flat class="text-capitalize" color="red-14" @click="winGestionComentariosAlertaStore.cerrar()"></q-btn>
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>
<script>
import winGestionComentariosAlertaStore from "./win-gestion-comentarios-alerta-store"
import winComentariosAlertaStore from "./win-comentarios-alerta-store"

export default {
    name:"WinGestionComentariosAlerta"
    ,    
    /*
    props:{        
        value:{
            required:true
        }
    },
    watch:{
        open:function(newval){
            this.$emit('input',newval)
        },
        value:function(newval){
            this.open = newval
        }
    },
    */
    data(){
        return {            
            winGestionComentariosAlertaStore: winGestionComentariosAlertaStore,
            winComentariosAlertaStore: winComentariosAlertaStore
        }
    },
    methods:{        
        btn_aceptar_click: async function(){            
            if (winGestionComentariosAlertaStore.state.comentario_alerta.id_comentario_alerta == ""){
                await winGestionComentariosAlertaStore.registrar()
                winGestionComentariosAlertaStore.cerrar()
                
                let id_alerta = winGestionComentariosAlertaStore.state.comentario_alerta.id_alerta
                winComentariosAlertaStore.fetch_data(id_alerta)                
            }
        }
    }
}
</script>