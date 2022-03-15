<template>
    <div>
        <q-card>
            <q-card-section>
                <div class="text-h6">Deposit</div>
            </q-card-section>
            <q-card-section>
                <!--<q-input v-model="moneda_symbol" label="Moneda"/>-->
                <SelectMoneda v-on:moneda-select="moneda_select"/>
                <q-input 
                v-model="importe"
                 label="Importe"
                 mask="#.##"                 
                 reverse-fill-mask               
                 input-class="text-right"
                 />

                 <q-input v-model="fec_registro"
                 label="Fec. Registro"
                 mask="##/##/####"
                 fill-mask="00/00/0000"
                 input-class="text-right"
                 />

            </q-card-section>
            <q-card-section>
                <q-btn color="primary" label="Guardar" @click="save"/>
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
            moneda:"",
            importe:"",
            fec_registro:""
        }
    },
    mounted:function(){

    },
    methods:{
        moneda_select:function(moneda){
            console.log(moneda)
            this.moneda = moneda
        },
        save:function(){
            console.log(this.moneda)
            var moneda_symbol = ""
            if (this.moneda != ""){
                moneda_symbol = this.moneda["value"]
            }

            this.$http.post('FundsManager/Deposit/do',{
                moneda_symbol: moneda_symbol,
                fec_registro: this.fec_registro,
                importe: this.importe
            }).then(httpresponse => {
                
                //guardar resultado
                console.log(httpresponse)
                
            })
        },
        cancelar:function(){
            this.$emit('deposit-cancel')
        }
    }
}
</script>