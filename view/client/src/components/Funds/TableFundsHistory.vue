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
        >
            <template v-slot:top>
                <div>
                    <div class="text-h6">
                        Historial
                    </div>
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
                    field:"id"
                },
                {
                    label:"Fch. transacción",
                    name:"fec_transaccion",
                    field:"fec_transaccion"
                },{
                    label:"Tipo",
                    name:"tipo_transaccion",
                    field:"tipo_transaccion"
                },{
                    label:"Subtipo",
                    name:"subtipo_transaccion",
                    field:"subtipo_transaccion"
                },{
                    label:"Importe",
                    name:"importe",
                    field:"importe"
                },{
                    label:"Concepto",
                    name:"concepto",
                    field:"concepto"
                },{
                    label:"Moneda",
                    name:"moneda_symbol",
                    field:"moneda_symbol"
                },{
                    label:"Saldo",
                    name:"saldo",
                    field:"saldo"
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