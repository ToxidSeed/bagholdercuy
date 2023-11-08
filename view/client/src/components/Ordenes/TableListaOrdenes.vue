<template>
    <div>    
        <q-toolbar>
            <q-toolbar-title class="text-blue-10">
                Historial de Ordenes
            </q-toolbar-title>
        </q-toolbar>
        <q-table
            title="Historial de Ordenes"
            :data="data"
            :columns="columns"
            selection="multiple"
            :selected.sync="selected"
            row-key="order_id"
            :pagination="pagination"
            separator="vertical"
            dense
        >
            <template v-slot:top>
                <div class="q-gutter-xs">
                    <q-btn color="blue-10"  label="Nuevo" />
                    <q-btn flat dense color="red" icon="delete" label="Eliminar" class="text-capitalize" @click="del_ordenes" />                    
                    <q-btn flat dense color="blue-10" icon="all_out" label="Reprocesar Todo" class="text-capitalize" @click="rep_todo" />
                </div>
            </template>
            <template v-slot:header="props">
                <q-tr :props="props">
                    <q-th style="width:15px"><q-checkbox dense v-model="all_selected"/></q-th>                                    
                    <q-th class="text-left"
                    style="width:30px"
                    >Fch. Orden</q-th>                    
                    <q-th class="text-left" 
                    style="width:30px"
                    >N. Orden</q-th>    
                    <q-th class="text-left"
                    style="width:30px"
                    >Tipo</q-th>
                    <q-th class="text-left"
                    style="width:30px"
                    >Symbol</q-th>
                    <q-th class="text-left"
                    style="width:30px"
                    >Codigo de Opcion</q-th>
                    <q-th class="text-left"
                    style="width:30px"
                    >T. Activo</q-th>                    
                    <q-th class="text-right"
                    style="width:30px"
                    >Cantidad</q-th>  
                    <q-th></q-th>                  
                </q-tr>
            </template>
            <template v-slot:body="props">
                <q-tr :props="props">
                    <q-menu
                        touch-position
                        context-menu
                    >
                        <q-list dense style="min-width: 100px">
                            <q-item clickable v-close-popup @click="ins_orden('antes', props.row)">
                                <q-item-section>Insertar Antes</q-item-section>
                            </q-item>
                            <q-item clickable v-close-popup @click="ins_orden('despues',props.row)">
                                <q-item-section>Insertar Despues</q-item-section>
                            </q-item>
                        </q-list>
                    </q-menu>
                    <q-td class="text-center"><q-checkbox v-model="props.row.selected" dense/></q-td>                    
                    <q-td key="fch_orden" :props="props">
                        {{  props.row.fch_orden }}
                    </q-td>
                    <q-td key="num_orden" :props="props">
                        {{ props.row.num_orden }}
                    </q-td>
                    <q-td key="cod_tipo_orden" :props="props">
                        {{  props.row.cod_tipo_orden }}
                    </q-td>                    
                    <q-td key="cod_symbol" :props="props">
                        {{  props.row.cod_symbol }}
                    </q-td>                    
                    <q-td key="cod_opcion" :props="props">
                        {{  props.row.cod_opcion }}
                    </q-td>                    
                    <q-td key="cod_tipo_activo" :props="props">
                        {{  props.row.cod_tipo_activo }}
                    </q-td>                    
                    <q-td key="cantidad" :props="props">
                        {{  props.row.cantidad }}
                    </q-td>
                    <q-td></q-td> 
                </q-tr>
            </template>
        </q-table>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue';
import {get_postconfig} from '@/common/request.js'
export default {
    name:"TableHistorialOrdenes",
    components:{
        MessageBox     
    },
    data: () => {
        return {
            columns:[
                {
                    label:"",                    
                    name:"selected",
                    field:"selected"
                },
                {
                    label:"orden_id",
                    align:"left",
                    name:"order_id",
                    field:"order_id"
                },{
                    label:"N. Orden",
                    align:"left",
                    name:"num_orden",
                    field:"num_orden"
                },{
                    label:"Tipo",
                    align:"left",
                    name:"cod_tipo_orden",
                    field:"cod_tipo_orden"
                },{
                    label:"Symbol",
                    align:"left",
                    name:"cod_symbol",
                    field:"cod_symbol"
                },{
                    label:"Codigo de Opcion",
                    align:"left",
                    name:"cod_opcion",
                    field:"cod_opcion"
                },{
                    label:"T. Activo",
                    align:"left",
                    name:"cod_tipo_activo",
                    field:"cod_tipo_activo"
                },{
                    label:"Cantidad",
                    align:"right",
                    name:"cantidad",
                    field:"cantidad"
                },{
                    label:"F. Orden",
                    align:"left",
                    name:"fch_orden",
                    field:"fch_orden"
                }
            ],
            selected:[],
            data:[],
            pagination:{
                rowsPerPage:30
            },
            all_selected:false
        }
    },
    mounted:function(){
        this.get_historial_ordenes()
    },
    methods:{
        get_historial_ordenes(){
            let postconfig = get_postconfig()
            this.$http.post(
                'OrdenManager/Buscador/get_historial_ordenes',{

            },postconfig).then(httpresp => {
                var appdata = httpresp.data
                appdata.data.forEach(element => {
                    element.selected = false
                })

                this.data = appdata.data                
            })
        },
        del_ordenes(){
            let ids_ordenes = []
            let selected = this.data.filter(elem =>{
                return elem.selected == true
            })
            
            selected.forEach(element => {
                ids_ordenes.push(element.order_id)
            })

            ids_ordenes = [...new Set(ids_ordenes)]            
            
            this.$http.post(
                'OrdenManager/EliminadorEntryPoint/procesar',{
                    ids_ordenes:ids_ordenes
                }
            ).then(httpresp => {
                var appresp = httpresp.data                
                this.$refs.msgbox.new(appresp)
                if (appresp.success == true){
                    this.get_historial_ordenes()
                }
            })            
        },
        rep_todo(){
            this.$http.post(
                'OrdenManager/ReprocesadorEntryPoint/reprocesar_todo'
            ).then(httpresp => {
                var appresp = httpresp.data
                this.$refs.msgbox.new(appresp)
                if (appresp.success == true){
                    this.get_historial_ordenes()
                }
            })
        },
        ins_orden(lugar, row){                
            this.$emit('ins-orden', lugar, row)
        }
    }
}
</script>