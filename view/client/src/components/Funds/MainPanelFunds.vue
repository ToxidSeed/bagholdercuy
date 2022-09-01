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
            <q-tab-panel name="Gestion" class="q-pl-none"> 
                <PanelFunds v-bind:visible="mantvisible"/>
            </q-tab-panel>
            <q-tab-panel name="Historial" class="q-pl-none q-pr-none">
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
            mantvisible:0,
            tab:"Gestion"
        }
    },
    mounted:function(){
        this.reset()    
    },
    watch:{
        $route:function(){
            this.reset()    
        }
    },
    methods:{
        reset:function(){
            if(this.$route.name!="funds"){
                this.mantvisible = 30
            }else{
                this.mantvisible = 0
            }            
        }
    }
}
</script>