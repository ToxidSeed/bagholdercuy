<template>
    <div>
        <q-card>
            <q-card-section>
                <div class="text-h6">Currency Exchange Rate</div>
            </q-card-section>                
            <q-card-section>
                <q-input v-model="fecha_cambio" label="Fecha Cambio"/>
                <SelectMoneda v-bind:label="'Moneda Base'"/>                
                <SelectMoneda v-bind:label="'Moneda Referencia'"/>
                <q-input v-model="importe_compra" label="Compra"/>
                <q-input v-model="importe_venta" label="Venta"/>
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
    name:"PanelCurrencyExchangeRate",
    components:{
        SelectMoneda
    },
    data:() => {
        return {
            fecha_cambio:"",
            importe_compra:0,
            importe_venta: 0
        }
    },
    methods:{
        cancelar:function(){
            this.$emit('conversion-moneda-cancel')
        }
    }    
}
</script>