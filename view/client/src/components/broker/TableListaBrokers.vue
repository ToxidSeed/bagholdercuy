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
                        v-on:btn-ver-click="ver(props.row.id_broker)"
                        v-on:btn-editar-click="editar(props.row.id_broker)"
                        />
                    </q-td>
                    <q-td class="text-left" style="width:50px;">{{ props.row.id_broker }}</q-td>
                    <q-td class="text-left">{{ props.row.nom_broker }}</q-td>                    
                    <q-td class="text-left"><q-icon name="circle" :color="props.row.flg_activo==1?'green':'red'"/></q-td>                    
                </q-tr>
            </template>
        </q-table>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import {postconfig} from '@/common/request.js'
import MessageBox from '@/components/MessageBox.vue'
import TableComandos from '@/components/common/TableComandos.vue';

export default {
    name:"TableListaBrokers",
    components:{
        MessageBox,
        TableComandos
    },
    data(){
        return {
            data:[],
            columns:[{
                name:'id_broker',
                label:'ID',
                align:'left',
                field:'id_broker'
            },{
                name:'nom_broker',
                label:'Nombre',
                align:'left',
                field:'nom_broker'
            }],
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
                "/broker/BrokerManager/get_brokers",{},
                postconfig()                
            ).then(httpresp => {
                this.$refs.msgbox.http_resp_on_error(httpresp)
                this.data = []                                
                this.data = httpresp.data.data                
            })
        },
        ver:function(id_broker){            
            this.$router.push({name:"broker-ver", params:{id_broker:id_broker.toString()}})
        },
        editar:function(id_broker){
            this.$router.push({name:"broker-editar", params:{id_broker:id_broker.toString()}})
        }
    }
}
</script>