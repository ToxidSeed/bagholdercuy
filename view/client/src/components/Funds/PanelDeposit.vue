<template>
    <div>
        <q-card>
            <q-card-section>
                <div class="text-h6">Deposit</div>
            </q-card-section>
            <q-card-section>                
                <div class="row">
                    <SelectMoneda v-on:moneda-select="moneda_select" class="col-6"/>
                    <q-input 
                    v-model="importe" label="Importe"
                    mask="#.##" reverse-fill-mask               
                    hint="format: .00"
                    input-class="text-right" class="col-6 q-pl-xs"
                    />
                </div>
                <div class="row">
                    <q-input v-model="fec_deposito"
                    label="Fec. Depósito" mask="##/##/####"
                    fill-mask="_" input-class="text-right q-pl-xs"                 
                    />
                </div>

            </q-card-section>
            <q-card-section>
                <q-btn color="primary" label="Guardar" @click="save"/>
                <q-btn color="white" text-color="red" label="Cancelar" @click="cancelar"/>
            </q-card-section>
        </q-card>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import SelectMoneda from '../SelectMoneda.vue'
import MessageBox from '../MessageBox.vue'

export default {
    name:"PanelDeposit",
    components:{
        SelectMoneda,
        MessageBox
    },
    data: () => {
        return {
            moneda:"",
            importe:"",
            fec_deposito:""
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
                fec_deposito: this.fec_deposito,
                importe: this.importe
            }).then(httpresponse => {
                var appdata = httpresponse.data
                this.$refs.msgbox.new(appdata)                
            })
        },
        cancelar:function(){
            this.$emit('deposit-cancel')
        }
    }
}
</script>