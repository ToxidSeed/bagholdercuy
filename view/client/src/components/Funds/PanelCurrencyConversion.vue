<template>
    <div>
        <q-card>
            <q-card-section class="q-pb-none  q-pt-none row">
                <div class="text-h6 text-primary">Conversion</div> 
                <!--<div class="bg-teal-3 text-white q-pa-xs">{{tc_msg}}</div>-->                
                <q-space/>
                <q-btn  flat dense rounded icon="close" :to="{name:'funds'}"/>
            </q-card-section>
            <q-card-actions class="q-pl-md q-pt-none">
                <q-btn no-caps label="Guardar" color="blue-10" @click="save"/>                
                <q-btn no-caps label="T/C Manual" :color="tc_manual==true?'red':'blue-10'" @click="tc_manual_handler"/>        
            </q-card-actions>
            <q-card-section>
                <div>
                    <q-badge :color="badgeinfo.color" outline multi-line class="q-pt-xs" v-show="badgeinfo_visible">
                    {{badgeinfo.msg}}
                    </q-badge>                
                </div>
                <div class="row">
                    <q-input readonly label="ID" v-model="conversion_id" class="col-3"/>
                    <q-input label="Fch. Conversion" v-model="fch_cambio" mask="##/##/####" fill-mask="_" class="col-3"/>
                    <!--<div class="col-6">
                        <q-radio v-model="tipo_operacion" val="C" label="Compra" />
                        <q-radio v-model="tipo_operacion" val="V" label="Venta" />
                    </div>-->
                </div>
                <div class="row">
                    <SelectMoneda v-bind:label="'Moneda Base'" class="col-6" 
                    v-on:moneda-select="mon_origen_sel"/>
                    <SelectMoneda v-bind:label="'Moneda Cotizada'" class="col-6 q-pl-xs"
                    v-on:moneda-select="mon_destino_sel"/>
                </div>                
                <div class="row">                              
                    <q-input label="Importe" v-model="importe" stack-label
                    input-class="text-right" reverse-fill-mask hint="Format: .00" 
                    v-on:keydown="keydown_numeric" class="col-4"/>

                    <q-input label="importe T/C" v-model="importe_tc"                     
                    input-class="text-right" reverse-fill-mask :readonly="tc_manual==false"
                    hint="Format: .00" v-on:keydown="keydown_numeric"
                    class="col-4 q-pl-md">
                        <template v-slot:after>                            
                            <q-btn round dense flat icon="search" @click="open_helper_tipo_cambio" class="bg-primary text-white"/>
                        </template>
                    </q-input>

                    <q-input label="Imp. Convertido" v-model="imp_convertido" stack-label readonly
                    input-class="text-right" reverse-fill-mask :hint="hint_imp_convertido" 
                    v-on:keydown="keydown_numeric" class="col-4 q-pl-md"/>
                </div>                                
                <!--<q-input label="Concepto" v-model="concepto"/>-->
            </q-card-section>            
        </q-card>
        <MessageBox ref="msgbox"/>
        <HelperTipoCambio ref="HelperTipoCambio"
        v-bind:in_fch_hasta="fch_cambio"
        v-bind:in_pares="par_usado"
        v-bind:input_pares_readonly=true        
        v-on:select="select_tc"
        />
    </div>
</template>
<script>
import SelectMoneda from '../SelectMoneda.vue'
import MessageBox from '../MessageBox.vue'
import func from '@/common/InputNumericHandler.js'
import date from 'date-and-time'
import {CLIENT_DATE_FORMAT} from '@/common/constants.js'
import HelperTipoCambio from '@/components/helpers/HelperTipoCambio.vue'
import {config} from '@/common/request.js'

export default {
    name:"PanelCurrencyConversion",
    components:{
        SelectMoneda,
        MessageBox,
        HelperTipoCambio
    },
    data: () => {
        return {
            tc_manual:false,
            conversion_id:"#",
            fch_cambio:"",
            importe:"",
            importe_tc:"0.00",
            //imp_convertido:"0.00",
            concepto:"",
            operacion:"MUL",
            mon_base_id:"",
            mon_ref_id:"",
            tipo_operacion:"C",
            badgeinfo:{
                msg:"",
                color:"red",
                visible:false
            },
            par_usado:"",
            wintipocambio:{
                open:false
            }
        }
    },
    mounted:function(){
        this.fch_cambio = date.format(new Date(),CLIENT_DATE_FORMAT)
        //get imp tc
        this.get_tipo_cambio(this.fch_cambio, this.mon_base_id, this.mon_ref_id)
    },
    watch:{
        importe:function(newval){                        
            this.importe = func.formatDecimal(newval,2)            
        },
        importe_tc:function(newval){
            this.importe_tc = func.formatDecimal(newval,3)
        },
        mon_base_id:function(newval){            
            if(newval == ""){
                this.badgeinfo.msg = ""
            }else{
                //this.get_par_info(newval, this.mon_ref_id)
                this.get_tipo_cambio(this.fch_cambio, newval, this.mon_ref_id)
            }            
        },
        mon_ref_id:function(newval){            
            if(newval == ""){
                this.badgeinfo.msg = ""
            }else{
                //this.get_par_info(this.mon_base_id, newval)
                this.get_tipo_cambio(this.fch_cambio, this.mon_base_id, newval)
            }            
        }
    },
    computed:{
        imp_convertido:function(){
            if(this.importe == "" || this.importe_tc == 0){
                return 0
            }
            console.log(this.operacion)
            if(this.operacion == "MUL" ){
                return (this.importe * this.importe_tc).toFixed(2)
            }else{
                return (this.importe / this.importe_tc).toFixed(2)
            }
            
        },
        badgeinfo_visible:function(){
            return this.badgeinfo.msg == ""?false:true;            
        },
        hint_imp_convertido:function(){
            let text = String(this.importe)
            let opertext = " x "
            if(this.operacion=="DIV"){
                opertext = ' / '
            }
            text = text + opertext +String(this.importe_tc)
            return text
        }
    },
    methods:{
        tc_manual_handler:function(){
            this.tc_manual = !this.tc_manual
            if(this.tc_manual == false){
                this.importe_tc = 0
            }
        },
        save:function(){
            this.$http.post(
                'FundsManager/Conversion/convert',{
                    conversion_id:this.conversion_id,
                    fch_cambio:this.fch_cambio,
                    tipo_operacion:this.tipo_operacion,
                    importe:this.importe,
                    importe_tc:this.importe_tc,
                    operacion:this.operacion,
                    concepto:this.concepto,
                    mon_base_id:this.mon_base_id,
                    mon_ref_id:this.mon_ref_id,
                    tc_manual:this.tc_manual
                },config()).then(httpresponse => {
                    /*var appdata = httpresponse.data
                    console.log(appdata)*/
                    this.$refs.msgbox.httpresp(httpresponse)
                }).catch(error=> {
                    console.log(error)
                }).then(()=>{
                    this.$emit('conversion-fin')
                })
        },
        get_tipo_cambio:function(fch_cambio, mon_base_id, mon_ref_id){            
            if (fch_cambio == ""){
                return
            }
            if (mon_base_id == ""){
                return
            }
            if (mon_ref_id == ""){
                return 
            }            

            this.$http.post(
                '/TipoCambio/TipoCambioFinder/get_tc',{
                    fch_cambio:fch_cambio,
                    mon_base_id: mon_base_id,
                    mon_ref_id: mon_ref_id
                },
                config()
            ).then(httpresp => {
                let appdata = httpresp.data    
                console.log(appdata)            
                if (appdata.success == false){
                    this.$refs.msgbox.httpresp(httpresp)
                }else{
                    let extradata = appdata.extradata
                    if(extradata.msg.text != ""){
                        this.badgeinfo.msg = extradata.msg.text
                        if(extradata.msg.type == "warning"){
                            this.badgeinfo.color = "orange"
                        }
                        if(extradata.msg.type == "error"){
                            this.badgeinfo.color = "red"
                        }
                    }                    
                    this.par_usado = extradata.par_usado
                    this.operacion = extradata.operacion
                    
                }
            })
        },
        keydown_numeric:function(event){                            
            func.preventInvalidNumbers(event)        
        },
        mon_origen_sel:function(data){
            if(data == null){
                this.mon_base_id = ""
            }else{
                this.mon_base_id = data.value
            }            
        },
        mon_destino_sel:function(data){
            if (data == null){
                this.mon_ref_id = ""   
            }else{
                this.mon_ref_id = data.value
            }            
        },
        open_helper_tipo_cambio:function(){
            this.$refs.HelperTipoCambio.open()
        },
        select_tc:function(row){
            this.fch_cambio = row.fch_cambio
            this.importe_tc = row.imp_compra            
        }
    }
}
</script>