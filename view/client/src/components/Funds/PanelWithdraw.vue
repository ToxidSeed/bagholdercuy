<template>
    <div>
        <q-card>
            <q-card-section class="q-pt-none q-pb-none row">
                <div class="text-h6">Retiros</div> 
                <q-space/>
                <q-btn  flat dense rounded icon="close" :to="{name:'funds'}"/>
            </q-card-section>
            <q-card-section class="q-pt-none q-pb-none">
                <q-btn no-caps color="blue-10" label="Guardar" @click="save"/>                
            </q-card-section>
            <q-card-section>
                <div class="row">
                    <SelectFunds class="col-6"
                    v-on:fund-select="fund_select" 
                    v-on:httperror="httpresp_dialog"
                    />
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
                    fill-mask="#"
                    hint="Format: dd/mm/yyyy"                    
                    class="col-4"
                    />
                </div>
            </q-card-section>            
        </q-card>     
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import SelectFunds from './SelectFunds.vue'
import MessageBox from '../MessageBox.vue'
import {CLIENT_DATE_FORMAT} from '@/common/constants.js'
import {config} from '@/common/request.js'
import date from 'date-and-time'

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
    mounted:function(){
        this.fec_retiro = date.format(new Date(), CLIENT_DATE_FORMAT)
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

            this.$http.post('FundsManager/WithdrawResource/retirar',{
                moneda_symbol: symbol,
                importe: this.importe,
                fec_retiro: this.fec_retiro
            },config()).then(httpresp => {
                this.$refs.msgbox.httpresp(httpresp)                   
            }).catch(error => {
                console.log(error)
            }).then(()=>{
                this.$emit("retiro-fin")
            })
        },
        cancelar:function(){
            this.$emit('withdraw-cancel')
        },
        httpresp_dialog:function(httpresp){
            this.$refs.msgbox.httpresp(httpresp)
        }
    }
}
</script>