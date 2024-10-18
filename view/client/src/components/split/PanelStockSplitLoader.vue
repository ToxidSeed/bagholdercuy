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
                <q-btn color="blue-10" icon="play_arrow" label="Procesar" class="q-mt-xs text-capitalize" flat dense />                
            </q-card-actions>
            <q-separator/>
            <q-card-section>
                <SelectSymbol/>
            </q-card-section>
        </q-card>
    </div>
</template>
<script>
import SelectSymbol from "@/components/SelectSymbol.vue"

export default {
    name:"PanelStockSplitLoader",
    components:{
        SelectSymbol
    },
    data() {
        return {

        }
    },
    methods: {
        procesar: function(){
            
        }
    }
}
</script>