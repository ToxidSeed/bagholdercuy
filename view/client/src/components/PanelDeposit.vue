<template>
    <div>
        <q-card>
            <q-card-section>
                <div class="text-h6">Deposit</div>
            </q-card-section>
            <q-card-section>
                <!--<q-input v-model="moneda_symbol" label="Moneda"/>-->
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
    name:"PanelDeposit",
    components:{
        SelectMoneda
    },
    data: () => {
        return {
            moneda_symbol:"",
            importe:""
        }
    },
    mounted:function(){

    },
    methods:{
        cancelar:function(){
            this.$emit('deposit-cancel')
        }
    }
}
</script>