<template>
    <div>
        <q-table
            title="Historial Operaciones"
            :data="data"
            :columns="columns"
            row-key="id"
            dense                   
        >
            <template v-slot:header="props">
                <q-tr :props="props">
                    <q-td>N. Operacion</q-td>
                    <q-td>Symbol</q-td>
                    <q-td>Operacion</q-td>
                    <q-td>F. Operacion</q-td>
                    <q-td>Cantidad</q-td>
                    <q-td>Saldo</q-td>
                    <q-td>Imp. Por Accion</q-td>
                    <q-td>Imp. Por Operacion</q-td>
                    <q-td>G/P Realizada</q-td>
                </q-tr>
            </template>
            <template v-slot:body="props">
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
                    <q-td key="num_operacion" :props="props">
                        {{ props.row.num_operacion }}
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
            </template>
        </q-table>        
    </div>
</template>
<script>
export default {
    name:"TableHistorialOperaciones",
    data: () => {
        return {
            columns:[
                {
                    label:"ID",
                    align:"left",
                    field:"id",
                    name:"id"
                },{
                    label:"N. Operacion",
                    field:"num_operacion",
                    align:"left",
                    name:"num_operacion"
                },{
                    label:"Symbol",
                    align:"left",
                    field:"symbol",
                    name:"symbol"
                },{
                    label:"Operacion",
                    align:"left",
                    field:"tipo_oper_nombre",
                    name:"tipo_oper_nombre"
                },{
                    label:"Fch. Operacion",
                    align:"left",
                    field:"trade_date",
                    name:"trade_date"
                },{
                    label:"Cantidad",
                    align:"left",
                    field:"cantidad",
                    name:"cantidad"
                },{
                    label:"Saldo",
                    align:"left",
                    field:"saldo",
                    name:"saldo"
                },{
                    label:"Imp. Accion",
                    align:"left",
                    field:"imp_accion",
                    name:"imp_accion"
                },{
                    label:"Imp. Operacion",
                    align:"left",
                    field:"imp_operacion",
                    name:"imp_operacion"
                },{
                    label:"G/P",
                    align:"right",
                    field:"realized_gl",
                    name:"realized_gl"
                }
            ],
            data:[],
            lastrow_contextmenu:null
        }
    },
    mounted:function(){
        this.obt_list()
    },
    methods:{
        obt_list:function(){
            this.$http.post(
                'TradeManager/BuscadorOperaciones/obt_list',{
                }).then(httpresp => {
                    var appresp = httpresp.data
                    console.log(appresp)
                    this.data = appresp.data
                })
        },
        row_contextmenu:function(evt, row){
            this.lastrow_contextmenu = row     
        },
        ins_row:function(rclicked_row){
            this.$emit("ins_row",rclicked_row)
        },
        del_row:function(rclicked_row){
            console.log(rclicked_row)
        }
    }
}
</script>