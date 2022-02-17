<template>
    <div>
        <q-card>
            <q-card-section>
                Conversion
            </q-card-section>                
            <q-card-section>
                <SelectMoneda v-bind:label="'Moneda Base'"/>
                <q-input v-model="importe" label="Importe"/>
                <SelectMoneda v-bind:label="'Moneda Referencia'"/>
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
    name:"PanelConversionMoneda",
    components:{
        SelectMoneda
    },
    data:() => {
        return {
            importe: 0
        }
    },
    methods:{
        cancelar:function(){
            this.$emit('conversion-moneda-cancel')
        }
    }    
}
</script>