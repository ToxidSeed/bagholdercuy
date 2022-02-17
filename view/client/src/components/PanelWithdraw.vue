<template>
    <div>
        <q-card>
            <q-card-section>
                <div class="text-h6">Withdraw</div> 
            </q-card-section>
            <q-card-section>
                <SelectMoneda/>
                <q-input v-model="importe" label="Importe"/>
            </q-card-section>
            <q-card-section>
                <q-btn color="primary" label="Guardar"/>
                <q-btn color="white" text-color="red" label="Cancelar" @click="cancelar"/>
            </q-card-section>
        </q-card>
    </div>
</template>
<script>
import SelectMoneda from './SelectMoneda.vue'
export default {
    name:"PanelWithdraw",
    components:{
        SelectMoneda
    },
    data:() => {
        return {
            importe:0
        }
    },
    methods:{
        cancelar:function(){
            this.$emit('withdraw-cancel')
        }
    }
}
</script>