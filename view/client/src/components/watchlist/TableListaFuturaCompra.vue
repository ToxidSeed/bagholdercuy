<template>
    <div>
        <q-table
            :data="data"
            title="Alertas"
            title-class="text-blue-10"
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
        
        <WinManagerFuturaOperacion v-model="WinManagerFuturaOperacion.open"/>
    </div>
</template>
<script>

import WinManagerFuturaOperacion from "@/components/watchlist/WinManagerFuturaOpercion.vue"

export default {
    name:"TableListaFuturaCompra",
    components:{
        
        WinManagerFuturaOperacion
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
            },
            WinManagerFuturaOperacion:{
                open:false
            }
        }
    },
    mounted:function(){
        this.init()
    },
    methods:{
        init:function(){
            
        }
    }
}
</script>