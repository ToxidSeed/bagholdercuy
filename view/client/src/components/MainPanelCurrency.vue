<template>
    <div class="row">
        <div class="col-3">
            <q-tabs
                v-model="tab"
                class="text-primary"
                align="left"
                dense
            >
                <q-tab name="currency"  label="Moneda" />
                <q-tab name="pairs" label="Pares" />
            </q-tabs>
            <q-tab-panels v-model="tab" animated>
            <q-tab-panel name="currency">
                <PanelCurrency v-on:panel-removed="store_panel_currency_data"
                v-bind:in_data="panel_currency_data"
                />
            </q-tab-panel>
            <q-tab-panel name="pairs">
                <PanelAddPair/>
                <TablePairs class="q-pt-xs"/>
            </q-tab-panel>
            </q-tab-panels>
        </div>
        <div class="col-9">
            <TableCurrency/>
        </div>
    </div>
</template>
<script>

import PanelCurrency from './PanelCurrency.vue'
import TablePairs from './TablePairs.vue'
import TableCurrency from './TableCurrency.vue'
import PanelAddPair from './PanelAddPair.vue'

export default {
    name:"MainPanelCurrency",
    components:{
        PanelCurrency,
        TablePairs,
        TableCurrency,
        PanelAddPair
    },
    data:() => {
        return {
            tab:"currency",
            panel_currency_data:{}
        }
    },
    methods:{
        store_panel_currency_data:function(data){
            this.panel_currency_data = data            
        }
    }
}
</script>