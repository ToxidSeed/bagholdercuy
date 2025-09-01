<template>
    <div>
        <TableSymbol/>
    </div>
</template>
<script>
import TableSymbol from './TableSymbol.vue'
//import PanelSymbolLoader from './PanelSymbolLoader.vue'

export default {
    name:"MainPanelSymbol",
    components:{        
        TableSymbol
    },
    data: () => {
        return {
            visible:25
        }
    }
}
</script>