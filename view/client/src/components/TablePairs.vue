<template>
    <div>
        <q-table
            title="Pares"
            :data = "data"
            :columns = "columns"
            row-key = "pair_name"
            dense
        >
        </q-table>
    </div>
</template>
<script>
export default {
    name:"TablePairs",
    data:() => {
        return {
            columns:[
                {
                    label:"#ID",
                    align:"left",
                    field:"pair_id",
                    name:"pair_id"
                },
                {
                    label:"Par",
                    align:"left",
                    field:"pair_name",
                    name:"pair_name"
                }],
            data:[{
                pair_id:1,
                pair_name:"USD/PEN"
            }]
        }
    }
}
</script>