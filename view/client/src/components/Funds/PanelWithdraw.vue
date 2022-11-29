<template>
    <div>
        <q-card>
            <q-card-section class="q-pt-none q-pb-none row">                
                <div class="text-h6 text-blue-10">Retiros</div>
                <q-space/>
                <q-btn  flat dense color="red" rounded icon="close" :to="{name:'funds'}"/>
            </q-card-section>
            <q-card-section class="q-pt-none q-pb-xs">
                <q-badge :color="info.color" outline multi-line class="q-pt-xs" v-show="info.visible">
                {{info.msg}}
                </q-badge>   
            </q-card-section>
            <q-card-section class="q-pt-none q-pb-none q-gutter-xs">
                <q-btn no-caps outline color="blue-10" label="Nuevo" @click="nuevo"/>                
                <q-btn no-caps color="green" label="Procesar" @click="confirm_procesar=true"/>                
            </q-card-section>
            <q-card-section>
                <div class="row">
                    <SelectMoneda class="col-4"
                    v-on:moneda-select="moneda_select"                     
                    />
                    <q-input readonly stack-label borderless class="col-6"
                    v-model="imp_saldo_moneda" label="Saldo" input-class="text-right"/>
                </div>
                <div class="row">                    
                    <q-input 
                    v-model.lazy="fec_retiro.value" 
                    label="Fec. Retiro"
                    mask="##/##/####"
                    fill-mask="#"
                    hint="Format: dd/mm/yyyy"                    
                    class="col-4"   
                    :error-message="fec_retiro.msg"
                    :error="fec_retiro.error"
                    @change="ult_transaccion"                 
                    />
                    <q-input 
                    v-model="importe" 
                    stack-label
                    label="Importe"
                    mask="#.##"
                    hint="Format: .00"                
                    reverse-fill-mask
                    input-class="text-right"
                    class="col-6 q-pl-xs"
                    />
                </div>
            </q-card-section>            
        </q-card>     
        <MessageBox ref="msgbox"/>
        <q-dialog v-model="confirm_procesar" persistent>
            <q-card>
                <q-card-section class="row items-center">
                <q-avatar icon="question_mark" color="warning" text-color="white" />
                <span class="q-ml-sm">Se va a procesar el retiro, ¿Desea continuar?</span>
                </q-card-section>

                <q-card-actions align="right">
                <q-btn flat label="Cancel" color="primary" v-close-popup />
                <q-btn flat label="Si" color="primary" v-close-popup @click="procesar"/>
                </q-card-actions>
            </q-card>
        </q-dialog>
    </div>
</template>
<script>
//import SelectFunds from './SelectFunds.vue'
import SelectMoneda from '@/components/SelectMoneda.vue'
import MessageBox from '../MessageBox.vue'
import {CLIENT_DATE_FORMAT} from '@/common/constants.js'
import {config} from '@/common/request.js'
import date from 'date-and-time'

export default {
    name:"PanelWithdraw",
    components:{
        SelectMoneda,
        MessageBox
    },
    data:() => {
        return {
            moneda:"",
            importe:"",
            imp_saldo_moneda:"0.00",
            fec_retiro:{
                value:"",
                error:false,
                msg:""
            },            
            info:{
                visible:false,
                color:"orange",
                msg:""
            },
            confirm_procesar:false
        }
    },
    mounted:function(){
        this.nuevo()
        //this.fec_retiro.value = date.format(new Date(), CLIENT_DATE_FORMAT)
        //this.$emit('cambiar-fecha', this.fec_retiro.value)
    },
    watch:{
        /*fec_retiro:function(newval){
            console.log(newval)
            //this.ult_transaccion()
        }*/
    },
    methods:{
        ult_transaccion: function(){            
            let fch_transaccion = this.fec_retiro.value
            if(this.fecha_incompleta(fch_transaccion)){                
                this.fec_retiro.error = true
                this.fec_retiro.msg = "Ingresar una fecha válida"
                return;
            }else{                
                this.fec_retiro.error = false
                this.fec_retiro.msg = "Ingresar una fecha válida"
            }

            this.$http.post('/FundsManager/FundsManager/ult_transaccion',{
                fch_transaccion: fch_transaccion
            },config()).then(httpresp => {
                this.$refs.msgbox.http_resp_on_error(httpresp)
                let appresp = httpresp.data
                let appdata = appresp.data
                if (appdata.ult_transaccion == false){
                    this.info.msg = appresp.message
                    this.info.visible = true                                      
                }else{
                    this.info.msg = ""
                    this.info.visible = false 
                }
            })
        },
        procesar:function(){
            var symbol = ""            
            if (this.moneda != ""){
                symbol = this.moneda.moneda_id
            }

            if (this.fec_retiro.error){                
                return;
            }

            let data = {
                fch_transaccion: this.fec_retiro.value
            }

            this.$http.post('FundsManager/WithdrawResource/retirar',{
                moneda_symbol: symbol,
                importe: this.importe,
                fec_retiro: this.fec_retiro.value
            },config()).then(httpresp => {
                this.$refs.msgbox.httpresp(httpresp)    
                let appresp = httpresp.data
                if(appresp.success == true){
                    this.nuevo()
                }
            }).catch(error => {
                this.$refs.msxbox.http_error(error)
            }).finally(()=>{
                this.$emit("procesar-fin",data)
            })
        },
        cancelar:function(){
            this.$emit('withdraw-cancel')
        },
        httpresp_dialog:function(httpresp){
            this.$refs.msgbox.httpresp(httpresp)
        },
        nuevo:function(){
            this.moneda = ""
            this.importe = ""
            this.imp_saldo_moneda = "0.00"
            this.fec_retiro.value = date.format(new Date(), CLIENT_DATE_FORMAT)
            this.fec_retiro.error = false
        },
        moneda_select:function(selected){
            this.moneda = selected
            let symbol = selected.value
            
            this.$http.post('/FundsManager/FundsManager/get_funds',{
                symbol: symbol
            },config()).then(httpresp => {
                this.$refs.msgbox.http_resp_on_error(httpresp)

                let appdata = httpresp.data
                if (appdata.data.length == 1){
                    let row = appdata.data.shift();
                    this.imp_saldo_moneda = row.importe
                }
            }).catch(error => {
                this.$refs.msgbox.http_error(error)
            })
        },
        fecha_incompleta:function(text){            
            return (text.search(/(#|\s)/i) >= 0)?true:false;
        }
    }
}
</script>