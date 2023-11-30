<template>
    <div>
        <q-table
            :data="store.table_monitoreo.state.monitoreo_activo_data"            
            title-class="text-blue-10"
            :columns="columns"
            row-key="name"            
            dense
            hide-header            
            separator="vertical"
            :pagination="pagination"
        >            
        
            <template v-slot:top shrink>
                <q-toolbar>
                    <q-toolbar-title class="text-blue-10">Monitoreo</q-toolbar-title>
                </q-toolbar>
                <q-toolbar>
                    <SelectSymbol label="Filtrar" style="width:250px;" v-on:select-symbol="sel_symbol"></SelectSymbol>
                    <q-btn dense label="Mostrar todos" flat color="blue-10" class="text-capitalize" @click="btn_mostrar_todos_click" icon="filter_list_off"></q-btn>
                    <q-btn icon="refresh" flat color="green" dense/>
                </q-toolbar>                                
            </template>
            <template v-slot:body="props">                
                <q-tr>                    
                    <q-td colspan="3" @click="get_alertas(props.row)">
                        <div class="row">
                            <div class="text-blue-10 col-11" >
                                {{ props.row.cod_symbol }}
                            </div>
                            <div>                                
                                <q-btn icon="notifications" flat :color="props.row.id_config_alerta == undefined ? 'grey':'orange'" dense round @click="btn_alerta_click(props.row)"/>
                            </div>
                            <div class="col-12">
                                {{ props.row.nom_symbol }}
                            </div>
                        </div>                        
                        <div class="row q-gutter-md">
                            <div class="col3">
                                <div>Imp. cierre anterior</div>
                                <div class="text-right">{{ props.row.imp_cierre_anterior }}</div>
                            </div>
                            <div class="col3">
                                <div>Imp. actual</div>
                                <div class="text-right">{{ props.row.imp_actual }}</div>
                            </div>
                        </div>      
                        <q-separator/>                  
                    </q-td>
                </q-tr>                                                                    
            </template>
        </q-table>            
    </div>
</template>
<script>
import WinGestorAlertaStore from "./win-gestor-alerta-store"
import tableAlertasSymbolStore from "./table-alertas-symbol-store"
import winComentariosAlertaStore from "./win-comentarios-alerta-store"
import SelectSymbol from "@/components/SelectSymbol.vue"
import store from "./store"

export default {
    name:"TableMonitoreo",
    components:{
        SelectSymbol
    },
    data(){
        return {
            data:[],
            columns:[{
                name:'id_monitoreo',
                label:'ID',
                align:'left',
                field:'id_monitoreo'
            },{
                name:'id_symbol',
                label:'Id Symbol',
                align:'left',
                field:'id_symbol'
            },{
                name:'cod_symbol',
                label:'Cod. Symbol',
                align:'left',
                field:'cod_symbol'
            },{
                name:'Nombre',
                label:'Nom. symbol',
                align:'left',
                field:'nom_symbol'
            },{
                name:'imp_cierre_anterior',
                label:'Imp. cierre anterior',
                align:'left',
                field:'imp_cierre_anterior'
            },{
                name:'imp_actual',
                label:'Imp. actual',
                align:'left',
                field:'imp_actual'
            },{
                name:'imp_variacion',
                label:'Imp. variacion',
                align:'left',
                field:'imp_variacion'
            },{
                name:'pct_variacion',
                label:'Pct. variacion',
                align:'left',
                field:'pct_variacion'
            },{
                name:"id_config_alerta",
                label:"Id configuracion alerta",
                align:'left',
                field:"id_config_alerta"
            }],
            pagination:{
                rowsPerPage:15
            },
            WinManagerFuturaOperacion:{
                open:false
            },
            WinGestorAlertaStore:WinGestorAlertaStore,
            tableAlertasSymbolStore: tableAlertasSymbolStore,
            winComentariosAlertaStore: winComentariosAlertaStore,
            store: store
        }
    },
    mounted:function(){
        this.init()
    },
    methods:{
        init:async function(){            
            await store.table_monitoreo.get_monitoreo_activo()            
            
        },        
        sel_symbol: async function(item){
            await store.table_monitoreo.get_monitoreo_activo({
                id_symbol: item.id_symbol
            })            
        },
        btn_mostrar_todos_click:async function(){            
            await store.table_monitoreo.get_monitoreo_activo()                        
        },
        btn_refresh_click: async function(){
            await store.table_monitoreo.refresh()            
        },
        get_alertas:function(row){                        
            //
            winComentariosAlertaStore.cerrar()

            this.tableAlertasSymbolStore.set_symbol({
                id_symbol: row.id_symbol,
                cod_symbol: row.cod_symbol,
                nom_symbol: row.nom_symbol
            })

            

            this.tableAlertasSymbolStore.fetch_data({                 
                id_config_alerta: row.id_config_alerta
            })
        },  
        btn_alerta_click:function(row){
            //Sea cual sea el resultado cerrar            

            if (row.id_config_alerta !== undefined && row.id_config_alerta !== "" && row.id_config_alerta != null){
                this.WinGestorAlertaStore.editar(row.id_config_alerta)
                return
            }

            if (row.id_monitoreo != undefined && row.id_monitoreo != ""){
                this.WinGestorAlertaStore.incluir_alerta(row.id_monitoreo, row.id_symbol)
            }            
        }
    }
}
</script>

<style scoped>
.q-toolbar {
    min-height: auto;
}
</style>