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
                    field:"symbol",
                    name:"symbol"                
                },{
                    label:"Nombre",
                    align:"left",
                    field:"nombre",
                    name:"nombre"
                },{
                    label:"Fch. Registro",
                    align:"left",
                    field:"fec_registro",
                    name:"fec_registro"
                }
            ],
            data:[]
        }
    }
}
</script>