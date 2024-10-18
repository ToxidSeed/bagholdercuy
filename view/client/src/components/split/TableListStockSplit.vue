<template>
    <div>
        <q-table
            :data="data"
            :columns="columns"
            row-key="name"
            dense
            :pagination="pagination"
            flat bordered
            separator="vertical"
        >
        </q-table>
    </div>
</template>
<script>

export default {
    name:"TableListaUsuario",
    components:{
    },
    data(){
        return {
            data:[],
            columns:[{
                label:"Id",
                name:"id_symbol",
                field:"id_symbol",
                headerStyle: 'width: 60px',
                style: 'width: 60px'
            },{
                label:"Fch. Split",
                name:"fch_split",
                field:"fch_split",
                headerStyle: 'width: 100px',
                style: 'width: 60px'
            },{
                label:"Numerador",
                name:"numerador",
                field:"numerador",
                headerStyle: 'width: 60px',
                style: 'width: 60px'
            },{
                label:"Denominador",
                name:"denominador",
                field:"denominador",
                headerStyle: 'width: 60px',
                style: 'width: 60px'
            },{
                label:"",
                name:"",
                field:""
            }],
            pagination:{
                rowsPerPage:15
            }
        }
    },
    mounted:function(){
        
    },
    methods:{
        
    }
}
</script>