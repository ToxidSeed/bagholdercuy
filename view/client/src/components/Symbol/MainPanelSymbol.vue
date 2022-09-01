<template>
    <div>
        <div>
            <q-splitter
                v-model="visible"
                :limits="[0,100]"
                style="height: 100hr" 
            >
                <template v-slot:before>
                    <PanelSymbol/>
                </template>
                <template v-slot:after>
                    <TableSymbol class="col-9"/>
                </template>            
            </q-splitter>
        </div>
        
    </div>
</template>
<script>
import PanelSymbol from './PanelSymbol.vue'
import TableSymbol from './TableSymbol.vue'
//import PanelSymbolLoader from './PanelSymbolLoader.vue'

export default {
    name:"MainPanelSymbol",
    components:{
        PanelSymbol,
        TableSymbol/*,
        PanelSymbolLoader*/
    },
    data: () => {
        return {
            visible:25
        }
    }
}
</script>