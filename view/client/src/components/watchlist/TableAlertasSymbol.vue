<template>
    <div>
        <q-table
            :data="tableAlertasSymbolStore.state.data"
            title="Alertas"
            title-class="text-blue-10"
            :columns="columns"
            row-key="name"            
            dense
            separator="vertical"
            :pagination="pagination"
        >        
            <template v-slot:top>
                <q-toolbar class="q-pa-none q-ma-none">
                    <q-toolbar-title class="q-pa-none q-ma-none">
                        <div v-if="titulo_default_visible == false">
                            <span class="text-blue-10">{{tableAlertasSymbolStore.state.cod_symbol}}</span>
                            {{tableAlertasSymbolStore.state.nom_symbol}}
                        </div>
                        <div class="text-blue-10" v-if="titulo_default_visible == true">
                            Alertas
                        </div>
                    </q-toolbar-title>
                </q-toolbar>
                <q-separator/>
                <q-toolbar class="q-pl-none">
                    <q-btn icon="refresh" dense color="green-10" flat></q-btn>
                </q-toolbar>
            </template>
            <template v-slot:header="props">
                <q-tr :props="props">          
                    <q-th style="width:15px;"></q-th>                              
                    <q-th class="text-center" style="width:100px;">Imp. alerta</q-th>                                                            
                    <q-th class="text-center" style="width:100px;">Imp. diff alerta</q-th>                                                            
                    <q-th></q-th>
                </q-tr>
            </template>
            <template v-slot:body="props">
                <q-tr :props="props" @click="ver_props(props)">
                    <q-menu
                    context-menu
                    touch-position                                        
                    >
                        <q-list dense>
                            <q-item clickable v-close-popup @click="agregar_comentario(props.row.id_alerta)">
                                <q-item-section>
                                    <div><q-icon name="add" color="green-10" class="q-pr-xs" ></q-icon><span>Añadir comentario</span></div>                                    
                                </q-item-section>
                            </q-item>
                            <q-item clickable v-close-popup @click="ver_comentarios(props.row.id_alerta, props.row)">
                                <q-item-section>
                                    <div><q-icon name="visibility" color="green-10" class="q-pr-xs"></q-icon><span>Ver Comentarios</span></div>                                    
                                </q-item-section>
                            </q-item>
                        </q-list>
                    </q-menu>                                                                             
                    <q-td class="bg-grey-3">{{ props.rowIndex + 1 }}</q-td>
                    <q-td class="text-right" :style="'width:100px;'+color(props.row.imp_alerta)">{{ props.row.imp_alerta }}</q-td>                                        
                    <q-td :class="text_color_diff_alerta(props.row.imp_diff_alerta)" >{{ props.row.imp_diff_alerta }}</q-td>                                                            
                    <q-td></q-td>                                                            
                </q-tr>
                <q-separator/>                
            </template>
        </q-table>
       <WinGestionComentariosAlerta/>       
       <WinComentariosAlerta/>  
    </div>
</template>
<script>

import tableAlertasSymbolStore from "./table-alertas-symbol-store"
import WinGestionComentariosAlerta from "./WinGestionComentariosAlerta.vue"
import winGestionComentariosAlertaStore from "./win-gestion-comentarios-alerta-store"
import WinComentariosAlerta from "./WinComentariosAlerta.vue"
import winComentariosAlertaStore from "./win-comentarios-alerta-store"

export default {
    name:"TableAlertasSymbol",
    components:{
        WinGestionComentariosAlerta   ,
        WinComentariosAlerta     
    },
    computed:{
        titulo_default_visible:function(){
            if (tableAlertasSymbolStore.state.cod_symbol == "" || tableAlertasSymbolStore.state.cod_symbol == undefined || tableAlertasSymbolStore.state.cod_symbol == null){
                return true
            }else{
                return false
            }
        }
    },
    data(){
        return {
            data:[],
            columns:[{
                name:'id_alerta',
                label:'ID',
                align:'left',
                field:'id_alerta'
            },{
                name:'id_config_alerta',
                label:'Id config alerta',
                align:'left',
                field:'id_config_alerta'
            },{
                name:'id_symbol',
                label:'Id symbol',
                align:'left',
                field:'id_symbol'
            },{
                name:'imp_alerta',
                label:'Imp. alerta',
                align:'left',
                field:'imp_alerta'
            },{
                name:"imp_diff_alerta",
                label:"Diff a alerta",
                alignh:"right",
                field:"imp_diff_alerta"
            }],
            pagination:{
                rowsPerPage:20
            },
            tableAlertasSymbolStore:tableAlertasSymbolStore,
            winGestionComentariosAlertaStore: winGestionComentariosAlertaStore,
            winComentariosAlertaStore: winComentariosAlertaStore
        }
    },
    mounted:function(){
        this.init()
    },
    methods:{
        init:function(){
            
        },
        ver_props:function(){
            console.log(WinComentariosAlerta)
        },
        color:function(imp_alerta){            
            if (tableAlertasSymbolStore.state.imp_accion == 0){
                return ""
            }
            
            let imp_accion = tableAlertasSymbolStore.state.imp_accion

            let pct_claridad = ((imp_accion - imp_alerta) * 100 / imp_accion)
            if(imp_accion > imp_alerta){
                let pct_claridad_inicial = 60
                pct_claridad = pct_claridad + pct_claridad_inicial
                return `background-color: hsl(0, 100%, ${pct_claridad}%);color: rgb(255,255,255)`
            }else{
                let pct_claridad_inicial = 40
                pct_claridad = Math.abs(pct_claridad) + pct_claridad_inicial                
                return `background-color: hsl(115, 80%, ${pct_claridad}%);color: rgb(255,255,255)`
            }
        },
        text_color_diff_alerta:function(imp_diff_alerta){            
            if (imp_diff_alerta >= 0){
                return "text-right text-green"
            }else{
                return "text-right text-red"
            }
        },
        agregar_comentario: function(id_alerta){
            winGestionComentariosAlertaStore.agregar(id_alerta)
            if (id_alerta !== winComentariosAlertaStore.state.id_alerta){
                winComentariosAlertaStore.cerrar()
            }
        },
        ver_comentarios: function(id_alerta, row){
            let aux = {
                imp_alerta: row.imp_alerta,
                cod_symbol: tableAlertasSymbolStore.state.cod_symbol
            }

            winComentariosAlertaStore.abrir(id_alerta, aux)
        }
    }
}
</script>

<style scoped>
.q-toolbar {
    min-height: auto;
}
</style>