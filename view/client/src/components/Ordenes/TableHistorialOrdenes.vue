<template>
    <div>
        <div class="text-h5 q-pa-xs">Historial de Ordenes</div>
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
                <q-btn color="primary"  label="Nuevo" />
                <q-btn class="q-ml-sm" color="red"  label="Eliminar" @click="del_orden" />
                <q-btn class="q-ml-sm" color="warning"  label="Reprocesar Todo" @click="rep_todo" />
            </template>
            <template v-slot:header="props">
                <q-tr :props="props">
                    <q-th style="width:15px"><q-checkbox dense v-model="all_selected"/></q-th>
                    <q-th class="text-left" 
                    style="width:30px"
                    >N. Orden</q-th>                    
                    <q-th class="text-left"
                    style="width:30px"
                    >Fch. Orden</q-th>                    
                    <q-th class="text-left"
                    style="width:30px"
                    >Tipo</q-th>
                    <q-th class="text-left"
                    style="width:30px"
                    >Symbol</q-th>
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
                    <q-td key="num_orden" :props="props">
                        {{ props.row.num_orden }}
                    </q-td>
                    <q-td key="order_date" :props="props">
                        {{  props.row.order_date }}
                    </q-td>
                    <q-td key="order_type" :props="props">
                        {{  props.row.order_type }}
                    </q-td>                    
                    <q-td key="symbol" :props="props">
                        {{  props.row.symbol }}
                    </q-td>                    
                    <q-td key="asset_type" :props="props">
                        {{  props.row.asset_type }}
                    </q-td>                    
                    <q-td key="quantity" :props="props">
                        {{  props.row.quantity }}
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
                    name:"order_type",
                    field:"order_type"
                },{
                    label:"Symbol",
                    align:"left",
                    name:"symbol",
                    field:"symbol"
                },{
                    label:"T. Activo",
                    align:"left",
                    name:"asset_type",
                    field:"asset_type"
                },{
                    label:"Cantidad",
                    align:"right",
                    name:"quantity",
                    field:"quantity"
                },{
                    label:"F. Orden",
                    align:"left",
                    name:"order_date",
                    field:"order_date"
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
            this.$http.post(
                'OrdenManager/Buscador/get_historial_ordenes',{

            }).then(httpresp => {
                var appdata = httpresp.data
                appdata.data.forEach(element => {
                    element.selected = false
                })

                this.data = appdata.data                
            })
        },
        del_orden(){
            var ids_ordenes = []
            
            this.selected.forEach(element => {
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