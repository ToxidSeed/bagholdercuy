<template>
    <div>
        <q-table
            title="Historial"
            :columns=columns
            :data=data
            row-key="id"
            dense
            selection="multiple"
            :selected.sync="selected"
            separator="vertical"
        >
            <template v-slot:top>
                <div>                    
                    <q-btn label="Rec. Saldos" color="primary"/>                    
                </div>
            </template>
        </q-table>
    </div>
</template>
<script>
export default {
    name:"TableFundsHistory",
    data: () => {
        return {
            columns:[
                {
                    label:"id",
                    name:"id",
                    field:"id",
                    style:"width:100px;"
                },
                {
                    label:"Fch. transacción",
                    name:"fec_transaccion",
                    field:"fec_transaccion",
                    style:"width:100px;"
                },{
                    label:"Tipo",
                    name:"tipo_trans_id",
                    field:"tipo_trans_id",
                    style:"width:100px;"
                },{
                    label:"Imp. Transaccion",
                    name:"imp_transaccion",
                    field:"imp_transaccion",
                    style:"width:100px;"
                },{
                    label:"Mon. Transaccion",
                    name:"mon_trans_id",
                    field:"mon_trans_id",
                    style:"width:100px;"
                },{
                    label:"Concepto",
                    align:"left",
                    name:"info_adicional",
                    field:"info_adicional"
                },{
                    label:"",
                    name:"",
                    field:""
                }
            ],
            data:[],
            selected:[]
        }
    },
    mounted:function(){
        this.get_historial()
    },
    methods:{
        get_historial:function(){
            this.$http.post('FundsManager/Historial/get',{

            }).then(httpresp => {
                var appresp = httpresp.data
                var data = appresp.data
                this.data = data
            })
        }
    }
}
</script>