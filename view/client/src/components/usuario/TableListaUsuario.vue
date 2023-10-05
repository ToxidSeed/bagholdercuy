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
                    <q-th class="text-left" style="width:50px;">Codigo</q-th>
                    <q-th class="text-left" style="width:350px;">Nombres</q-th>                                        
                    <q-th class="text-left">Apellidos</q-th>                                                            
                </q-tr>
            </template>
            <template v-slot:body="props">
                <q-tr :props="props">
                    <q-td style="width:50px;">
                        <TableComandos
                        :ver="true"
                        :configurar="true"
                        v-on:btn-ver-click="ver(props.row.id)"
                        v-on:btn-configurar-click="configurar(props.row.id)"
                        />
                    </q-td>
                    <q-td class="text-left">{{ props.row.id }}</q-td>
                    <q-td class="text-left">{{ props.row.usuario }}</q-td>                    
                    <q-td class="text-left">{{ props.row.nombres }}</q-td>                    
                    <q-td class="text-left">{{ props.row.apellidos }}</q-td>                                        
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
    name:"TableListaUsuario",
    components:{
        MessageBox,
        TableComandos
    },
    data(){
        return {
            data:[],
            columns:[{
                name:'id_usuario',
                label:'ID',
                align:'left',
                field:'id_usuario'
            },{
                name:'nom_usuario',
                label:'Nombre',
                align:'left',
                field:'nom_usuario'
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
            this.get_usuarios()
        },
        get_usuarios:function(){
            this.$http.post(
                "/usuario/UsuarioManager/get_usuarios",{},
                postconfig()                
            ).then(httpresp => {
                this.$refs.msgbox.http_resp_on_error(httpresp)                  
                this.data = this.get_data_from_resp(httpresp)
            })
        },
        get_data_from_resp:function(httpresp){
            let data = []
            let appdata = httpresp.data
            if (appdata == null){
                return []
            }

            data = appdata.data
            if (data == null){
                return []            
            }
            return data
        },
        ver:function(id_usuario){            
            this.$router.push({name:"usuario-ver", params:{id_usuario:id_usuario.toString()}})
        },        
        configurar:function(id_usuario){
            this.$router.push({name:"usuario-config", params:{id_usuario:id_usuario.toString()}})
        }
    }
}
</script>