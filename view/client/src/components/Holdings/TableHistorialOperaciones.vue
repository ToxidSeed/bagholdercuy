<template>
    <div>
        <q-table

            :data="data"
            :columns="columns"
            selection="multiple"
            :selected.sync="selected"
            row-key="id"
            dense       
            :pagination="pagination"  
            separator="vertical"                      
        >
            <template v-slot:top>
                <div>
                    <div class="text-h5 col text-blue-10">Historial de Operaciones</div>                                    
                </div>
                <q-toolbar class="q-pa-none">
                    <q-btn class="text-capitalize" flat dense color="blue-10" icon="filter_alt">Filtrar</q-btn>
                </q-toolbar>
            </template>
            <!--<template v-slot:header="props">
                <q-tr :props="props">
                    <q-th><q-checkbox dense/></q-th>
                    <q-th>N. Orden</q-th>
                    <q-th>N. Operacion</q-th>
                    <q-th>Symbol</q-th>
                    <q-th>Operacion</q-th>
                    <q-th>F. Operacion</q-th>
                    <q-th class="text-right">Cantidad</q-th>
                    <q-th class="text-right">Saldo</q-th>
                    <q-th class="text-right">Imp. Por Accion</q-th>
                    <q-th class="text-right">Imp. Por Operacion</q-th>
                    <q-th class="text-right">G/P Realizada</q-th>
                </q-tr>
            </template>-->
            <!--<template v-slot:body="props">
                <q-tr :props="props">
                    <q-menu
                        touch-position
                        context-menu
                    >
                        <q-list dense style="min-width: 100px">
                            <q-item clickable v-close-popup @click="ins_row(props.row)">
                                <q-item-section>Insertar</q-item-section>
                            </q-item>
                            <q-item clickable v-close-popup @click="del_row(props.row)">
                                <q-item-section>Eliminar</q-item-section>
                            </q-item>
                        </q-list>
                    </q-menu>
                    <q-td class="text-center"><q-checkbox v-model="props.row.selected" dense/></q-td>
                    <q-td key="num_orden" :props="props">
                        {{ props.row.num_orden }}
                    </q-td>
                    <q-td key="num_operacion" :props="props">
                        {{ props.row.symbol }}-{{date_format(props.row.trade_date)}}-{{ props.row.num_operacion }}
                    </q-td>
                    <q-td key="symbol" :props="props">
                        {{ props.row.symbol }}
                    </q-td>
                    <q-td key="tipo_oper_nombre" :props="props">
                        {{ props.row.tipo_oper_nombre }}
                    </q-td>
                    <q-td key="trade_date" :props="props">
                        {{ props.row.trade_date}}
                    </q-td>
                    <q-td key="cantidad" :props="props">
                        {{ props.row.cantidad}}
                    </q-td>
                    <q-td key="saldo" :props="props">
                        {{ props.row.saldo}}
                    </q-td>
                    <q-td key="imp_accion" :props="props">
                        {{ props.row.imp_accion }}
                    </q-td>
                    <q-td key="imp_operacion" :props="props">
                        {{ props.row.imp_operacion }}
                    </q-td>
                    <q-td key="realized_gl" :props="props">
                        {{ props.row.realized_gl }}
                    </q-td>
                </q-tr>
            </template>-->
        </q-table>  
        <MessageBox ref="msgbox"/>      
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue';
import {get_postconfig} from '@/common/request.js';
export default {
    name:"TableHistorialOperaciones",
    components:{
        MessageBox     
    },
    data: () => {
        return {
            columns:[
                {
                    label:"Fch. Operacion",
                    align:"left",
                    field:"fch_transaccion",
                    name:"fch_transaccion",
                    style:"width:100px;"
                },{
                    label:"orden",
                    align:"left",
                    field:"num_orden",
                    name:"num_orden",
                    style:"width:50px;"
                },{
                    label:"N. Operacion",
                    field:"num_posicion",
                    align:"left",
                    name:"num_posicion",
                    style:"width:50px;"
                },{
                    label:"Symbol",
                    align:"left",
                    field:"cod_symbol",
                    name:"cod_symbol",
                    style:"width:100px;"
                },{
                    label:"Opcion",
                    align:"left",
                    field:"cod_opcion",
                    name:"cod_opcion",
                    style:"width:100px;"
                },{
                    label:"Operacion",
                    align:"left",
                    field:"tipo_oper_nombre",
                    name:"tipo_oper_nombre",
                    style:"width:100px;"
                },{
                    label:"Cantidad",
                    align:"right",
                    field:"cantidad",
                    name:"cantidad",
                    style:"width:100px;"
                },{
                    label:"Saldo",
                    align:"right",
                    field:"ctd_saldo_posicion",
                    name:"ctd_saldo_posicion",
                    style:"width:100px;"
                },{
                    label:"Imp. Accion",
                    align:"right",
                    field:"imp_accion",
                    name:"imp_accion",
                    style:"width:100px;"
                },{
                    label:"Imp. Operacion",
                    align:"right",
                    field:"imp_posicion",
                    name:"imp_posicion",
                    style:"width:100px;"
                },{
                    label:"G/P",
                    align:"right",
                    field:"imp_gp_realizada",
                    name:"imp_gp_realizada",
                    style:"width:100px;"
                }/*,{
                    label:"orden_id",
                    align:"left",
                    field:"order_id",
                    name:"order_id",
                    style:"width:100px;"
                }*/,{
                    label:"",
                    align:"",
                    field:"",
                    name:""
                }
            ],
            data:[],    
            selected:[],
            pagination:{
                rowsPerPage:25
            }
        }
    },
    mounted:function(){
        this.obt_list()
    },
    methods:{
        obt_list:function(){
            this.$http.post(
                'operacion/OperacionManager/get_operaciones',{
                },get_postconfig()).then(httpresp => {
                    this.data = []
                    var appresp = httpresp.data
                    for (let elem of appresp.data){
                        this.data.push(elem)
                    }
                    console.log(appresp)
                    //console.log(appresp)                    
                    /*appresp.data.forEach(element => {
                        let eltmp = element
                        eltmp.imp_operacion = element.imp_operacion.toFixed(2)
                        eltmp.realized_gl = element.realized_gl.toFixed(2)                        
                        eltmp.imp_accion = element.imp_accion.toFixed(2)                        
                        eltmp.saldo = element.saldo.toFixed(2)                        
                        this.data.push(eltmp)
                    })*/
                    //this.data = appresp.data
                })
        },        
        ins_row:function(rclicked_row){
            this.$emit("ins_row",rclicked_row)
        },
        del_opers:function(){
            var del_opers = []
            this.selected.forEach(elem => {
                del_opers.push(elem.id)
            })

            del_opers = [...new Set(del_opers)]

            this.$http.post(
                'OperacionesManager/EliminadorEntryPoint/procesar',{
                    del_opers:del_opers
                }
            ).then(httpresp => {
                var appresp = httpresp.data
                this.$refs.msgbox.new(appresp)
                this.obt_list()
            })
        },
        date_format(in_str){
            var out_str = in_str.replaceAll("-","")    
            return out_str
        }
    }
}
</script>