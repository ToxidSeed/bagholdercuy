<template>
    <div>
        <q-tabs
            v-model="tab"
            align="left"
            dense
        >
            <q-tab name="Gestion" label="Gestion"/>
            <q-tab name="Historial" label="Historial"/>
        </q-tabs>
        <q-tab-panels
            v-model="tab"
        >
            <q-tab-panel name="Gestion"> 
                <PanelFunds/>
            </q-tab-panel>
            <q-tab-panel name="Historial">
                <TableFundsHistory/>
            </q-tab-panel>
        </q-tab-panels>
    </div>
</template>
<script>
import PanelFunds from '@/components/Funds/PanelFunds.vue';
import TableFundsHistory from '@/components/Funds/TableFundsHistory.vue';

export default {
    name:"MainPanelFunds",
    components:{
        PanelFunds,
        TableFundsHistory
    },
    data: () => {
        return {
            tab:"Gestion"
        }
    }
}
</script>