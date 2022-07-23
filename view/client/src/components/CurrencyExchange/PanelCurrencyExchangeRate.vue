<template>
    <div>
        <q-card>                                               
            <q-card-section>
                <div class="row">
                    <q-input v-model="fecha_cambio" label="Fecha Cambio" mask="##/##/####" fill-mask="__/__/____" class="col-6"/>
                    <SelectPair v-on:pair-select="pair_select_handler" class="col-6 q-pl-xs"/>
                </div>
                <div class="row">
                    <q-input v-model="importe_compra" label="Compra" mask="#.##" fill-mask="0" input-class="text-right" reverse-fill-mask class="col-6"/>
                    <q-input v-model="importe_venta" label="Venta" mask="#.##" fill-mask="0" input-class="text-right"
                    reverse-fill-mask class="col-6 q-pl-xs"/>
                </div>                
            </q-card-section>
            <q-separator dark />
            <q-card-actions align="right">
                <q-btn color="primary" label="Guardar"/>
                <q-btn color="white" text-color="red" label="Cancelar" @click="cancelar"/>
            </q-card-actions>
        </q-card>
    </div>
</template>
<script>
import SelectPair from '../SelectPair.vue'

export default {
    name:"PanelCurrencyExchangeRate",
    components:{
        SelectPair
    },
    data:() => {
        return {
            fecha_cambio:"",
            pair_id:0,
            importe_compra:0,
            importe_venta: 0
        }
    },
    methods:{
        cancelar:function(){            
            this.$emit('conversion-moneda-cancel')            
        },
        pair_select_handler:function(data){
            console.log(data)
        }
    }    
}
</script>