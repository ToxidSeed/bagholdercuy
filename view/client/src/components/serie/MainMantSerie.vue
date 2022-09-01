<template>
    <div>
        <q-splitter
            v-model="visible"
            :limits="[0,100]"
            style="height:100hr"
        >
            <template v-slot:before>
                <PanelSerieLoader/>
            </template>
            <template v-slot:after>
                <q-toolbar>                    
                    <q-btn class="q-ml-xs" color="primary" label="Carga de Series" @click="visible=30"></q-btn>
                </q-toolbar>
                <TableResumenSerie/>
            </template>
        </q-splitter>        
    </div>
</template>
<script>
import TableResumenSerie from '@/components/serie/TableResumenSerie.vue'
import PanelSerieLoader from '@/components/serie/PanelSerieLoader.vue'
export default {
    name:"MainMantSerie",
    components:{
        TableResumenSerie,
        PanelSerieLoader
    },
    data: () => {
        return {
            visible:0
        }
    }
}
</script>