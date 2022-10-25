<template>
    <div>
        <q-card>
            <q-card-section class="q-pb-none q-pt-none" >
                <div class="row">
                    <div class="text-h6">Deposit</div>
                    <q-space/>
                    <q-btn  flat dense rounded icon="close" :to="{name:'funds'}"/>
                </div>
            </q-card-section>
            <q-toolbar >
                <q-btn no-caps color="blue-10" label="Guardar" @click="save"/>
            </q-toolbar>
            <q-card-section>
                <div>
                    <q-badge :color="badgeinfo.color" outline multi-line class="q-pt-xs" v-show="badgeinfo_visible">
                    {{badgeinfo.msg}}
                    </q-badge>                
                </div>        
                <div class="row">
                    <SelectMoneda v-on:moneda-select="moneda_select" class="col-6"
                    v-on:httperror="open_httpresp_dialog"
                    />
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
                    @change="ult_transaccion"             
                    />
                </div>
            </q-card-section>            
        </q-card>
        <MessageBox v-bind:config="msgboxconfig"/>
    </div>
</template>
<script>    
import SelectMoneda from '../SelectMoneda.vue'
import MessageBox from '../MessageBox.vue'
import {CLIENT_DATE_FORMAT} from '@/common/constants.js'
import date from 'date-and-time'
import {headers} from '@/common/common.js'

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
            fec_deposito:"",
            msgboxconfig:{},
            badgeinfo:{
                color:"red",
                msg:"",
                visible:false
            }
        }
    },
    computed:{        
        badgeinfo_visible:function(){
            return this.badgeinfo.msg == ""?false:true;            
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
            },{
                headers:headers()
            }).then(httpresp => {                
                this.msgboxconfig = {
                    httpresp:httpresp
                }                
                
                //var appresp = httpresp.data                
                //var appdata = appresp.data 
                /*if (appdata.success == true){
                    this.$emit('btn-save-success',appdata.extradata)
                }*/                
            }).catch(error => {
                console.log(error)
            }).then(()=>{
                this.$emit('deposito-fin')
            })
        },
        cancelar:function(){
            this.$emit('deposit-cancel')
        },
        open_httpresp_dialog:function(httpresp){
            this.$refs.msgbox.httpresp(httpresp)                   
        },
        ult_transaccion:function(){
            this.$http.post(
                '/FundsManager/FundsManager/ult_transaccion',{
                    fch_transaccion:this.fec_deposito
                },
                {
                    headers:headers()
                }
            ).then(httpresp =>{
                //solo si sale error mostrará el mensaje
                this.msgboxconfig = {
                    httpresp:httpresp,
                    open:'error'
                }
                let appresp = httpresp.data
                let data = appresp.data

                if (data.ult_transaccion == false){
                    this.badgeinfo.msg = appresp.message
                }                
            })
        }

    }
}
</script>