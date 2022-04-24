<template>
    <div>
        <q-card>
            <q-card-section class="q-pb-none">
                <div class="text-h6 text-primary">Conversion</div> 
            </q-card-section>
            <q-card-section>
                <div class="row">
                    <q-input readonly label="ID" v-model="conversion_id" class="col-3"/>
                    <q-input label="Fch. Cambio" v-model="fec_cambio" mask="##/##/####" fill-mask="_" class="col-3"/>
                    <div class="col-6">
                        <q-radio v-model="tipo_operacion" val="C" label="Compra" />
                        <q-radio v-model="tipo_operacion" val="V" label="Venta" />
                    </div>
                </div>
                <div class="row">                              
                    <q-input label="Importe" v-model="importe" 
                    input-class="text-right" reverse-fill-mask hint="Format: .00" 
                    v-on:keydown="keydown_numeric" class="col-6 q-pr-xs"/>
                    <q-input label="importe T/C" v-model="importe_tc"                     
                    input-class="text-right" reverse-fill-mask
                    hint="Format: .00" v-on:keydown="keydown_numeric"
                    class="col-6 q-pl-xs"/>
                </div>                
                <div class="row">
                    <SelectMoneda v-bind:label="'Moneda Origen'" class="col-5" 
                    v-on:moneda-select="mon_origen_sel"/>
                    <SelectMoneda v-bind:label="'Moneda Destino'" class="col-7 q-pl-xs"
                    v-on:moneda-select="mon_destino_sel"/>
                </div>
                <q-input label="Concepto" v-model="concepto"/>                
            </q-card-section>
            <q-card-actions align="right">
                <q-btn label="Aceptar" color="primary" @click="save"/>
                <q-btn label="Cancelar"/>
            </q-card-actions>
        </q-card>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import SelectMoneda from '../SelectMoneda.vue'
import MessageBox from '../MessageBox.vue'
import func from '@/common/InputNumericHandler.js'

export default {
    name:"PanelCurrencyConversion",
    components:{
        SelectMoneda,
        MessageBox
    },
    data: () => {
        return {
            conversion_id:"#",
            fec_cambio:"",
            importe:"",
            importe_tc:"",
            concepto:"",
            moneda_origen:"",
            moneda_destino:"",
            tipo_operacion:"C"
        }
    },
    watch:{
        importe:function(newval){                        
            this.importe = func.formatDecimal(newval,2)
        },
        importe_tc:function(newval){
            this.importe_tc = func.formatDecimal(newval,3)
        }
    },
    methods:{
        save:function(){
            this.$http.post(
                'FundsManager/Conversion/convert',{
                    conversion_id:this.conversion_id,
                    fec_cambio:this.fec_cambio,
                    tipo_operacion:this.tipo_operacion,
                    importe:this.importe,
                    importe_tc:this.importe_tc,
                    concepto:this.concepto,
                    moneda_origen:this.moneda_origen,
                    moneda_destino:this.moneda_destino
                }).then(httpresponse => {
                    var appdata = httpresponse.data
                    this.$refs.msgbox.new(appdata)
                })
        },
        keydown_numeric:function(event){      
            console.log(event)                              
           func.preventInvalidNumbers(event)        
        },
        mon_origen_sel:function(data){
            this.moneda_origen = data.value
        },
        mon_destino_sel:function(data){
            this.moneda_destino = data.value
        }
    }
}
</script>