<template>
    <div class="row">        
        <div class="col-3">
            <q-tabs v-model="maintabs">
                <q-tab name="pnl_currency_exchange_rate" label="Currency Exchange"/>
                <q-tab name="pnl_historial_rates_loader" label="Historial Rates Loader"/>
            </q-tabs>
            <q-tab-panels v-model="maintabs"  >
                <q-tab-panel 
                name="pnl_currency_exchange_rate"
                class="q-pa-xs"   
                >
                    <PanelCurrencyExchangeRate/>        
                </q-tab-panel>
                <q-tab-panel name="pnl_historial_rates_loader"
                class="q-pa-xs" 
                >
                    <PanelCurrencyExchangeRateHistLoader/>
                </q-tab-panel>
            </q-tab-panels>
        </div>
        <div class="col-9">     
            <TableCurrencyExchanges/>       
        </div>           
    </div>
</template>
<script>
import PanelCurrencyExchangeRate from './PanelCurrencyExchangeRate.vue'
import TableCurrencyExchanges from './TableCurrencyExchangeRates.vue'
import PanelCurrencyExchangeRateHistLoader from './PanelCurrencyExchangeRateHistLoader.vue'

export default {
    name:"MainPanelCurrencyExchange",
    components:{
        PanelCurrencyExchangeRate,
        TableCurrencyExchanges,
        PanelCurrencyExchangeRateHistLoader
    },
    data: () => {
        return {
            maintabs:"pnl_currency_exchange_rate"
        }
    },

}
</script>