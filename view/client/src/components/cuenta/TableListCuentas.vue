<template>
    <div>
        <q-table
            :data="data"
            :columns="columns"
            row-key="name"
            dense
            :pagination="pagination"
        >
            <template v-slot:header="props">
                <q-tr :props="props">
                    <q-th style="width:50px;"></q-th>
                    <q-th class="text-left" style="width:50px;">ID</q-th>
                    <q-th class="text-left" style="width:100px;">Codigo</q-th>                                        
                    <q-th class="text-left" style="width:350px;">Nombre</q-th>                                        
                    <q-th class="text-left">Activo</q-th>
                </q-tr>
            </template>
            <template v-slot:body="props">
                <q-tr :props="props">
                    <q-td style="width:50px;">
                        <TableComandos 
                        :ver="true"
                        :editar="true"
                        v-on:btn-ver-click="ver(props.row.id_cuenta)"
                        v-on:btn-editar-click="editar(props.row.id_cuenta)"
                        />
                    </q-td>
                    <q-td class="text-left" style="width:50px;">{{ props.row.id_cuenta }}</q-td>
                    <q-td class="text-left" style="width:100px;">{{ props.row.cod_cuenta }}</q-td>
                    <q-td class="text-left">{{ props.row.nom_cuenta }}</q-td>                    
                    <q-td class="text-left"><q-icon name="circle" :color="props.row.flg_activo==1?'green':'red'"/></q-td>                    
                </q-tr>
            </template>
        </q-table>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue'
import TableComandos from '@/components/common/TableComandos.vue';
import {postconfig} from '@/common/request.js'

export default {
    name:"TableListaCuentas",
    components:{
        MessageBox,
        TableComandos
    },
    data(){
        return {
            data:[],
            columns:[
                {
                    name:'id_cuenta',
                    label:'ID',
                    align:'left',
                    field:'id_cuenta'
                },{
                    name:'cod_cuenta',
                    label:'Codigo',
                    align:'left',
                    field:'cod_cuenta'
                },{
                    name:"nom_cuenta",
                    label:"Nombre",
                    align:"left",
                    field:"nom_cuenta"
                },{
                    name:"flg_activo",
                    label:"Activo",
                    align:"left",
                    field:"flg_activo"
                }
            ],
            pagination:{
                rowsPerPage:15
            }
        }
    },
    mounted:function(){
        this.init()
    },
    methods:{
        init:function(){
            this.get_brokers()
        },
        get_brokers:function(){
            this.$http.post(
                "/cuenta/CuentaManager/get_cuentas",{

                },
                postconfig()
            ).then(httpresp => {
                this.$refs.msgbox.http_resp_on_error(httpresp)
                this.data = []                                
                this.data = httpresp.data.data                
            })
        },
        ver:function(id_cuenta){
            this.$router.push({name:"cuenta-ver", params:{id_cuenta:id_cuenta.toString()}})
        },
        editar:function(id_cuenta){
            this.$router.push({name:"cuenta-editar", params:{id_cuenta:id_cuenta.toString()}})
        }
    }    
}
</script>