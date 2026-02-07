<template>
    <q-dialog v-model="winComentariosAlertaStore.state.abierto" position="right" seamless >
        <q-card style="width:600px;" class="bg-white">
            <q-toolbar >
                <q-toolbar-title class="text-blue-10 text-subtitle1">
                    <span>Comentarios</span>
                    <span> / {{winComentariosAlertaStore.state.cod_symbol}}</span> 
                    <span> / {{winComentariosAlertaStore.state.imp_alerta}}</span>
                </q-toolbar-title>
                <q-space />
                <q-btn icon="close" flat dense v-close-popup></q-btn>
            </q-toolbar>
            <q-card-section class="q-pl-none q-pr-none q-pt-none q-pb-none">
                <q-table
                :data="winComentariosAlertaStore.state.data"
                :columns="columns"
                row-key="name"            
                dense                
                separator="vertical"
                :visible-columns="['rownum','dsc_comentario','']"                
                >                    
                    <template v-slot:body="props">
                        <q-tr :props="props">
                            <q-menu
                            context-menu
                            touch-position
                            >
                                <q-list dense>
                                    <q-item clickable v-close-popup @click="winComentariosAlertaStore.eliminar(props.row.id_comentario_alerta)">
                                        <q-item-section>
                                            <div><q-icon name="delete" color="red" class="q-pr-xs" size="xs"></q-icon><span>Eliminar</span></div>                                            
                                        </q-item-section>
                                    </q-item>
                                </q-list>
                            </q-menu>                       
                            <q-td key="rownum" style="width:35px;">
                                {{ props.rowIndex + 1 }}     
                            </q-td>
                            <q-td key="dsc_comentario">
                                {{ props.row.dsc_comentario }}
                            </q-td>
                            <q-td key="">
                            </q-td>
                        </q-tr>
                    </template>
                </q-table>
            </q-card-section>
        </q-card>
    </q-dialog>
</template>
<script>
import winComentariosAlertaStore from "./win-comentarios-alerta-store"

export default {
    name:"WinComentariosAlerta",
    data(){
        return {
            abierto:false,            
            columns:[{
                "field":"rownum",
                "name":"rownum",
                "label":"N.",
                "align":"right",
                "style":"width:50px;"
            },{
                "field":"id_alerta",
                "name":"id_alerta",
                "label":"Id. Alerta",
                "align":"right"
            },{
                "field":"id_comentario_alerta",
                "name":"id_comentario_alerta",
                "label":"Id. comentario alerta",
                "align":"right"
            },{
                "field":"dsc_comentario",
                "name":"dsc_comentario",
                "label":"Comentario",
                "align":"left",
                "style":"width:400px;"
            },{
                "field":"",
                "name":"",
                "label":"",
                "align":"right"
            }],
            winComentariosAlertaStore: winComentariosAlertaStore
        }
    },
    methods:{
        abrir:function(){
            console.log("xx")
            this.abierto = true
        },
        test:function(props){
            console.log(props)
        }
    }
}
</script>
<style scoped>
.q-toolbar {
    min-height: auto;
}
</style>