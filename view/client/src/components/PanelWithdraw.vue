<template>
    <div>
        <q-card>
            <q-card-section>
                <div class="text-h6">Withdraw</div> 
            </q-card-section>
            <q-card-section>
                <SelectFunds v-on:fund-select="fund_select"/>
                <q-input 
                v-model="importe" 
                label="Importe"
                mask="#.##"
                reverse-fill-mask
                input-class="text-right"
                />
                <q-input 
                v-model="fec_registro" 
                label="Fec. Registro"
                mask="##/##/####"
                fill-mask="00/00/0000"
                input-class="text-right"
                />
            </q-card-section>
            <q-card-section>
                <q-btn color="primary" label="Guardar" @click="save"/>
                <q-btn 
                color="white" 
                text-color="red" 
                label="Cancelar" 
                @click="cancelar"/>
            </q-card-section>
        </q-card>
    </div>
</template>
<script>
import SelectFunds from './SelectFunds.vue'
export default {
    name:"PanelWithdraw",
    components:{
        SelectFunds
    },
    data:() => {
        return {
            moneda:"",
            importe:"",
            fec_registro:""
        }
    },
    methods:{
        fund_select:function(selected){
            console.log(selected)
            this.moneda = selected
        },
        save:function(){
            var symbol = ""
            console.log(this.moneda)
            if (this.moneda != ""){
                symbol = this.moneda["symbol"]                
            }

            this.$http.post('FundsManager/Withdraw/do',{
                moneda_symbol: symbol,
                importe: this.importe,
                fec_registro: this.fec_registro
            }).then(httpresponse => {
                console.log(httpresponse)
            })
        },
        cancelar:function(){
            this.$emit('withdraw-cancel')
        }
    }
}
</script>