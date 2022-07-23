<template>
    <div class="row">        
        <!--<div class="col-3">
            <q-tabs v-model="maintabs">
                <q-tab name="pnl_currency_exchange_rate" label="Currency Exchange"/>
                <q-tab name="pnl_historial_rates_loader" label="Historial Rates Loader"/>
            </q-tabs>
            <q-tab-panels v-model="maintabs"  >
                <q-tab-panel 
                name="pnl_currency_exchange_rate"
                class="q-pa-xs"   
                >
                            
                </q-tab-panel>
                <q-tab-panel name="pnl_historial_rates_loader"
                class="q-pa-xs" 
                >
                    <PanelCurrencyExchangeRateHistLoader/>
                </q-tab-panel>
            </q-tab-panels>
        </div>-->        
        <div class="col-12">     
            <div class="q-ma-sm">
                <q-btn label="Nuevo" color = "primary" @click="win_currexchange_open=true"/>
                <q-btn class="q-ml-sm" label="Loader" color="green" @click="win_loader_open=true"/>
            </div>
            <TableCurrencyExchanges/>       
        </div>       
        <q-dialog v-model="win_currexchange_open">
            <PanelCurrencyExchangeRate
                v-on:conversion-moneda-cancel="win_currexchange_open=false"
            />
        </q-dialog>    
        <q-dialog v-model="win_loader_open">
            <PanelCurrencyExchangeRateHistLoader
                v-on:btn_cancelar_click="win_loader_open=false"
            />
        </q-dialog>
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
            maintabs:"pnl_currency_exchange_rate",
            win_currexchange_open:false,
            win_loader_open:false
        }
    },

}
</script>