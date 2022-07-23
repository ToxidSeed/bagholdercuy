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
                    <q-input v-model="fec_deposito" label="Fec. Depósito" mask="##/##/####"
                    fill-mask="#" class="q-pl-xs col-5"                 
                    />
                </div>

            </q-card-section>
            <q-card-section>
                <q-btn color="primary" label="Guardar" @click="save"/>
                <q-btn color="red" class="q-ml-xs" label="Cancelar" @click="cancelar"/>
            </q-card-section>
        </q-card>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import SelectMoneda from '../SelectMoneda.vue'
import MessageBox from '../MessageBox.vue'
import {CLIENT_DATE_FORMAT} from '@/common/constants.js'
import date from 'date-and-time'

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
        this.fec_deposito = date.format(new Date(),CLIENT_DATE_FORMAT)
        console.log(this.fec_deposito)
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

            this.$http.post('FundsManager/DepositResource/add',{
                moneda_symbol: moneda_symbol,
                fec_deposito: this.fec_deposito,
                importe: this.importe
            }).then(httpresp => {                
                this.$refs.msgbox.httpresp(httpresp)                
            }).catch(error => {
                console.log(error)
            })
        },
        cancelar:function(){
            this.$emit('deposit-cancel')
        }
    }
}
</script>