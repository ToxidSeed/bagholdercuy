<template>
    <div>                
        <q-card flat bordered>
            <q-toolbar>
                <q-toolbar-title class="text-blue-10">
                    Carga de stock splits
                </q-toolbar-title>
                <q-btn icon="close" color="red" flat/>
            </q-toolbar>            
            <q-card-actions class="q-pt-none q-pl-xs">
                <q-btn color="blue-10" icon="play_arrow" label="Procesar" class="q-mt-xs text-capitalize" flat dense 
                @click="split_store.procesar()"
                />                
            </q-card-actions>
            <q-separator/>
            <q-card-section>
                <SelectSymbol v-on:select-symbol="sel_symbol"/>
                <div class="text-h6 text-weight-bold">{{split_store.state.panel_stock_split_loader.symbol.value}}</div>
                <div>{{split_store.state.panel_stock_split_loader.symbol.name}}</div>
            </q-card-section>
        </q-card>
    </div>
</template>
<script>
import SelectSymbol from "@/components/SelectSymbol.vue"
import split_store from "./split-store.js"

export default {
    name:"PanelStockSplitLoader",
    components:{
        SelectSymbol
    },
    data() {
        return {
            split_store:split_store
        }
    },
    methods: {
        sel_symbol:function(selected){
            split_store.sel_symbol_procesar(selected)
        }
    }
}
</script>