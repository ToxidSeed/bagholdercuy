<template>
    <div class="row">
        <div class="col-3">
            <PanelCurrencyExchangeRate/>    
        </div>
        <div class="col-9">
            <TableCurrencyExchanges/>
        </div>
    </div>
</template>
<script>
import PanelCurrencyExchangeRate from './PanelCurrencyExchangeRate.vue'
import TableCurrencyExchanges from './TableCurrencyExchanges.vue'

export default {
    name:"MainPanelCurrencyExchange",
    components:{
        PanelCurrencyExchangeRate,
        TableCurrencyExchanges
    },
    data: () => {
        return {

        }
    },

}
</script>