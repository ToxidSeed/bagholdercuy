<template>
    <div class="row">
        <div class="col-3">
            <q-tabs
            v-model="tab"                    
            >
                <q-tab name="symbol" label="Symbol" />
                <q-tab name="symbol_loader" label="Symbol Loader" />
            </q-tabs>
            <q-tab-panels
            v-model="tab"             
            >
                <q-tab-panel name="symbol">
                    <PanelSymbol/>
                </q-tab-panel>
                <q-tab-panel name="symbol_loader">
                    <PanelSymbolLoader/>
                </q-tab-panel>
            </q-tab-panels>
        </div>
        <TableSymbol class="col-9"/>
    </div>
</template>
<script>
import PanelSymbol from './PanelSymbol.vue'
import TableSymbol from './TableSymbol.vue'
import PanelSymbolLoader from './PanelSymbolLoader.vue'

export default {
    name:"MainPanelSymbol",
    components:{
        PanelSymbol,
        TableSymbol,
        PanelSymbolLoader
    },
    data: () => {
        return {
            tab:"symbol"
        }
    }
}
</script>