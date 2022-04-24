<template>
    <div>
        <q-table
            title="Funds"
            :data = "data"
            :columns = "columns"
            row-key="name"
            dense
        >
        </q-table>
    </div>
</template>
<script>
export default {
    name:"TableFunds",
    data: () => {
        return {
            data:[],
            columns:[{
                label:"Moneda",
                align:"left",
                field:"moneda_symbol",
                name:"moneda_symbol"
            },{
                label:"Importe",
                align:"left",
                field:"importe_fmt",
                name:"importe"
            }]
        }
    },
    mounted:function(){
        this.get_funds()
    },
    methods:{
        get_funds:function(){
            this.$http.post('FundsManager/FundsManager/get_funds',{
                symbol:""
            }).then(httpresp => {
                var appresponse = httpresp.data
                this.data = appresponse.data
            })
        }
    }
}
</script>