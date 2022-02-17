<template>
    <q-table
        title="Holdings Detail"
        :data="table_data"
        :table_columns="table_columns"
        row-key="name"
        dense
    >
    </q-table>
</template>
<script>
export default {
    name:"TableHoldingsDetail",
    data:() => {
        return {
            table_data:[],
            table_columns:[{
                label:"symbol",
                align:"left",
                field:"symbol",
                name:"symbol"
            },{
                label:"transaction date",
                align:"left",
                field:"transaction_date",
                
            }]
        }
    }
}
</script>