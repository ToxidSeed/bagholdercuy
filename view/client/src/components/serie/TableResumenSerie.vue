<template>
    <div>
        <q-table
            :columns="columns"
            :data="data"
            :pagination="pagination"
            row-key="symbol_id"
            separator="vertical"
            dense
        >
        </q-table>
    </div>
</template>
<script>
export default {
    name:"TableResumenSerie",
    data: () => {
        return {
            columns:[{
                label:"symbol",
                align:"left",
                name:"symbol",
                field:"symbol"
            },{
                label:"Fch. Inicio",
                align:"left",
                name:"fch_desde",
                field:"fch_desde"
            },{
                label:"Fch. Fin",
                align:"left",
                name:"fch_hasta",
                field:"fch_hasta"
            },{
                label:"Fch. ult. carga dia",
                align:"left",
                name:"fch_ult_carga_dia",
                field:"fch_ult_carga_dia"
            },{
                label:"Fch. ult. carga mes",
                align:"left",
                name:"fch_ult_carga_mes",
                field:"fch_ult_carga_mes"
            },{
                label:"Fch. ult. carga sem",
                align:"left",
                name:"fch_ult_carga_sem",
                field:"fch_ult_carga_sem"
            },{
                label:"Fch. ult. carga anyo",
                align:"left",
                name:"fch_ult_carga_anyo",
                field:"fch_ult_carga_anyo"
            },{
                label:"",
                align:"",
                name:"",
                field:""
            }],
            data:[],
            pagination:{
                rowsPerPage:20
            }
        }
    }
}
</script>