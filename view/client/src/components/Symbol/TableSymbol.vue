<template>
    <div>
        <q-table
            :data="data"
            :columns="columns"
            row-key="symbol_id"
            dense     
            :pagination="pagination"       
        >
            
        </q-table>
    </div>
</template>
<script>
export default {
    name:"TableSymbol",
    data: () => {
        return {
            pagination:{
                rowsPerPage:20
            },
            columns:[{
                label:"ID",
                aling:"left",
                field:"symbol_id",
                name:"symbol_id"
            },{
                label:"Symbol",
                align:"left",
                name:"symbol",
                field:"symbol"
            },{
                label:"Name",
                align:"left",
                name:"name",
                field:"name"
            },{
                label:"Region",
                align:"left",
                name:"region",
                field:"region"
            },{
                label:"Exchange",
                align:"left",
                name:"exchange",
                field:"exchange"
            },{
                label:"Asset Type",
                align:"left",
                name:"asset_type",
                field:"asset_type"
            }],
            data:[]
        }
    },
    mounted:function(){
        console.log('mounted')
        this.get_list()
    },
    methods:{
        get_list:function(){
            this.$http.post('SymbolManager/SymbolFinder/get_list',{

            }).then(httpresponsse => {
                var appdata = httpresponsse.data
                this.data = appdata.data
            })
        }
    }
}
</script>