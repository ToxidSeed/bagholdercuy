<template>
    <div>
        <q-table
            :data="data"
            :columns="columns"        
            row-key="symbol"
            dense
            :pagination="pagination"
            separator="vertical"
        />
    </div>
</template>
<script>
export default {
    name:"TableOpciones",
    data: () => {
        return {
            data:[],
            columns:[
                {
                    label:"Subyacente",
                    align:"left",
                    field:"underlying",
                    name:"underlying",
                    style:"width:100px;"                
                },{
                    label:"Ult. fch. Carga",
                    align:"left",
                    field:"fch_registro",
                    name:"fch_registro",
                    style:"width:100px;"                
                },{
                    label:"Ult. Vencimiento",
                    align:"left",
                    field:"fch_vencimiento",
                    name:"fch_vencimiento",
                    style:"width:100px;"                
                },{
                    label:"",
                    align:"",
                    field:"",
                    name:""
                }
            ],
            pagination:{
                rowsPerPage:20
            }
        }
    },
    mounted:function(){
        this.get_opciones()
    },
    methods:{
        get_opciones:function(){
            this.$http.post('/OpcionesContratoManager/OpcionesContratoManager/get_resumen_subyacentes').then(
                httpresp => {
                    let appresp = httpresp.data
                    this.data = appresp.data
                }
            )
        }
    }
}
</script>