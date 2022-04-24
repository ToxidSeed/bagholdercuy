<template>
    <div>
        <q-card>
            <q-card-section>
                <div class="text-h6">Withdraw</div> 
            </q-card-section>
            <q-card-section>
                <div class="row">
                    <SelectFunds v-on:fund-select="fund_select" class="col-6"/>
                    <q-input 
                    v-model="importe" 
                    label="Importe"
                    mask="#.##"
                    hint="Format: .00"                
                    reverse-fill-mask
                    input-class="text-right"
                    class="col-6 q-pl-xs"
                    />
                </div>
                <div class="row">
                    <q-input 
                    v-model="fec_retiro" 
                    label="Fec. Retiro"
                    mask="##/##/####"
                    fill-mask="_"
                    hint="Format: dd/mm/yyyy"
                    input-class="text-right"
                    class="col-4"
                    />
                </div>
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
        <MessageBox ref="msgbox"/>   
    </div>
</template>
<script>
import SelectFunds from './SelectFunds.vue'
import MessageBox from '../MessageBox.vue'
export default {
    name:"PanelWithdraw",
    components:{
        SelectFunds,
        MessageBox
    },
    data:() => {
        return {
            moneda:"",
            importe:"",
            fec_retiro:""
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
                fec_retiro: this.fec_retiro
            }).then(httpresponse => {
                var appdata = httpresponse.data
                this.$refs.msgbox.new(appdata)
            })
        },
        cancelar:function(){
            this.$emit('withdraw-cancel')
        }
    }
}
</script>