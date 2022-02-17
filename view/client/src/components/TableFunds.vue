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
                field:"importe",
                name:"importe"
            }]
        }
    },
    mounted:function(){
        //this.get_list()
    },
    methods:{
        get_list:function(){
            this.$http.post('FundsManager/FundsManager/get_funds').then(httpresp => {
                console.log(httpresp)
            })
        }
    }
}
</script>