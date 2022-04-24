<template>
    <div>
        <q-table
            title="Monedas"
            :data= "data"
            :columns = "columns"
            row-key="symbol"
            dense
        >
        </q-table>
    </div>
</template>
<script>
export default {
    name:"TableCurrency",
    data: () => {
        return {
            columns:[
                {
                    label:"Symbol",
                    align:"left",
                    field:"currency_symbol",
                    name:"currency_symbol"                
                },{
                    label:"Nombre",
                    align:"left",
                    field:"currency_name",
                    name:"currency_name"
                },{
                    label:"Fch. Registro",
                    align:"left",
                    field:"fec_registro",
                    name:"fec_registro"
                }
            ],
            data:[]
        }
    },
    mounted:function(){
        this.get_currency_list()
    },
    methods:{
        get_currency_list:function(){
            this.$http.post('CurrencyManager/CurrencyFinder/get_list',{

            }).then(httpresponse => {
                var appdata = httpresponse.data
                this.data = appdata.data
            })
        }
    }
}
</script>