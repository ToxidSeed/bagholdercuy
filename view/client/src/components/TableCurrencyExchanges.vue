<template>
    <div>
        <q-table
            title="Historial de Tipos de Cambio"
            :data="data"
            :columns="columns"
            row-key="par_name"
            dense
        >
        </q-table>
    </div>
</template>
<script>
export default {
    name:"TableCurrencyExchanges",
    data: () => {
        return {
            columns:[
                {
                    label:"Fecha Cambio",
                    align:"left",
                    field:"fecha_cambio",
                    name:"fecha_cambio"
                },{
                    label: "Par",
                    align:"left",
                    field:"par_name",
                    name:"par_name"
                },{
                    label:"Ind. Activo",
                    align:"left",
                    field:"ind_activo",
                    name:"ind_activo"
                },{
                    label:"Imp. Compra",
                    align:"right",
                    field:"importe_compra",
                    name:"importe_compra"
                },{
                    label:"Imp. Venta",
                    align:"right",
                    field:"importe_venta",
                    name:"importe_venta"
                }
            ],
            data:[]
        }
    },
    mounted:function(){

    },
    methods:{
        get_historic_rates:function(){

        }
    }
}
</script>