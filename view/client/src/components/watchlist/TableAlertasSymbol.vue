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
            flat
        >        
            <template v-slot:top>
                <q-toolbar class="q-pa-none q-ma-none">
                    <q-toolbar-title class="q-pa-none q-ma-none">
                        <div v-if="titulo_default_visible == false" class="row items-center q-gutter-x-sm">
                            <span class="text-blue-10 text-weight-bold">{{tableAlertasSymbolStore.state.cod_symbol}}</span>
                            <span class="text-grey-9">{{tableAlertasSymbolStore.state.nom_symbol}}</span>
                            <q-badge
                                v-if="has_expiracion_alerta"
                                :color="badge_expiracion_alerta_color"
                                class="q-px-xs text-weight-bold"
                            >
                                <q-icon name="timer" size="12px" class="q-mr-xs" />
                                {{ format_dias_expiracion_alerta }}
                                <q-tooltip v-if="tableAlertasSymbolStore.state.fch_vencimiento">
                                    Vencimiento: {{ format_fecha_vencimiento_alerta }}
                                </q-tooltip>
                            </q-badge>
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
        <q-separator/> 
        
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
        },
        has_expiracion_alerta: function() {
            return this.get_dias_expiracion_alerta !== null
        },
        get_dias_expiracion_alerta: function() {
            const dias = tableAlertasSymbolStore.state.dias_expiracion
            if (dias !== null && dias !== undefined) {
                return Number(dias)
            }
            const fch = tableAlertasSymbolStore.state.fch_vencimiento
            if (fch) {
                const clean = String(fch).split(/[-T ]/)[0]
                const parts = clean.split('-')
                if (parts.length === 3) {
                    const year = parseInt(parts[0], 10)
                    const month = parseInt(parts[1], 10) - 1
                    const day = parseInt(parts[2], 10)
                    const expDate = new Date(year, month, day)
                    const now = new Date()
                    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
                    const diffTime = expDate.getTime() - today.getTime()
                    return Math.round(diffTime / (1000 * 60 * 60 * 24))
                }
            }
            return null
        },
        format_dias_expiracion_alerta: function() {
            const dias = this.get_dias_expiracion_alerta
            if (dias === null) return ''
            if (dias === 0) return 'Expira hoy'
            if (dias === 1) return '1 día'
            if (dias > 1) return `${dias} días`
            if (dias === -1) return 'Expiró ayer'
            return `Expiró hace ${Math.abs(dias)} días`
        },
        badge_expiracion_alerta_color: function() {
            const dias = this.get_dias_expiracion_alerta
            if (dias === null) return 'grey-6'
            if (dias < 0) return 'grey-7'
            if (dias <= 2) return 'negative'
            if (dias <= 7) return 'amber-9'
            if (dias <= 30) return 'primary'
            return 'teal-8'
        },
        format_fecha_vencimiento_alerta: function() {
            const fch = tableAlertasSymbolStore.state.fch_vencimiento
            if (!fch) return ''
            const clean = String(fch).split(/[-T ]/)[0]
            const parts = clean.split('-')
            if (parts.length === 3) {
                return `${parts[2]}/${parts[1]}/${parts[0]}`
            }
            return clean
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

            let pct_claridad = ((imp_accion - imp_alerta) * 100 / imp_accion)/2.5
            if(imp_accion > imp_alerta){
                let pct_claridad_inicial = 35
                pct_claridad = pct_claridad + pct_claridad_inicial
                console.log(pct_claridad)            
                return `background-color: hsl(0, 100%, ${pct_claridad}%);color: rgb(255,255,255)`
            }else{
                let pct_claridad_inicial = 35
                pct_claridad = Math.abs(pct_claridad) + pct_claridad_inicial    
                console.log(pct_claridad)            
                return `background-color: hsl(115, 70%, ${pct_claridad}%);color: rgb(255,255,255)`
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