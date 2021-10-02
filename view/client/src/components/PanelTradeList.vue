<template>
    <div>
        <div class="q-ma-md text-h6">Posiciones</div>
        <q-table
        title="Posiciones"
        :data="data"
        :columns="columns"
        row-key="name"
        >
            <template v-slot:top>
                <q-btn color="primary" :disable="loading" label="Agregar" to="/trade" />                
            </template>
        </q-table>
    </div>
</template>
<script>
export default {
    name:"PanelTradeList",
    data:() =>{
        return {
            columns:[
                {
                    label:"symbol",
                    field:"symbol",
                    align: 'left'
                },{
                    label:"% change",
                    field:"change",
                    align:"left"
                },{
                    label:"shares",
                    field:"shares",
                    align:"left"
                },{
                    label:"avg. cost",
                    field:"cost",
                    align:"left"
                },{
                    label:"last price",
                    field:"cost",
                    align:"left"
                },{
                    label:"market value",
                    field:"market_value",
                    align:"left"
                }
            ],
            data:[]
        }
    }
}
</script>