<template>
    <div>
        <q-card>     
            <q-card-section class="q-pt-xs q-pb-none row">                
                <div class="text-h6 text-blue-10">Registrar T/C</div>
                <q-space/>
                <q-btn  flat dense color="red" rounded icon="close" @click="btn_close_click_handler"/>
            </q-card-section>   
            <q-card-actions align="left">
                <q-btn color="green" label="Procesar" @click="btn_procesar_click_handler"/>                
            </q-card-actions>                                       
            <q-card-section>
                <div class="row">
                    <q-input v-model="fecha_cambio.value" label="Fecha Cambio" mask="##/##/####" fill-mask="#" class="col-5"/>
                    <SelectPair v-on:pair-select="pair_select_handler" class="col-5 q-pl-xs"/>
                </div>
                <div class="row">
                    <q-input v-model="importe_compra" label="Compra" mask="#.##"  input-class="text-right" 
                    stack-label
                    class="col-5"/>
                    <q-input v-model="importe_venta" label="Venta" mask="#.##"  input-class="text-right"
                    stack-label
                     class="col-5 q-pl-xs"/>
                </div>                
            </q-card-section>
            <q-separator dark />            
        </q-card>
        <Confirmar v-model="confirmar_dialog.open" v-bind:msg="confirmar_dialog.msg" v-on:ok="procesar"/>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import SelectPair from '../SelectPair.vue'
import date from 'date-and-time';
import { CLIENT_DATE_FORMAT } from '@/common/constants';
import {postconfig} from '@/common/request.js';
import Confirmar from '@/components/dialogs/Confirmar.vue';
import MessageBox from '@/components/MessageBox.vue';

export default {
    name:"PanelCurrencyExchangeRate",
    components:{
        SelectPair,
        Confirmar,
        MessageBox
    },
    data:() => {
        return {
            fecha_cambio:{
                value:""
            },
            par_id:0,
            importe_compra:"",
            importe_venta: "",
            confirmar_dialog:{
                open:false,
                msg:""
            }
        }
    },
    mounted:function(){        
        this.fecha_cambio.value = date.format(new Date(),CLIENT_DATE_FORMAT)
        this.$emit('open',25)
    },
    methods:{
        btn_close_click_handler:function(){      
            this.$router.push({name:'currencyexchange',params:{inFirstPanelSize:0}})      
            this.$emit('close',0)            
        },
        btn_procesar_click_handler:function(){
            this.confirmar_dialog.open = true
            this.confirmar_dialog.msg = "Se va a registrar el tipo de cambio, ¿Desea continuar?"
        },
        procesar:function(){
            this.$http.post('tipocambio/TipoCambioNuevoController/procesar',{
                fch_cambio: this.fecha_cambio.value,
                par_id: this.par_id,
                imp_compra: this.importe_compra,
                imp_venta: this.importe_venta
            },postconfig()).then(httpresp => {
                this.$refs.msgbox.http_resp(httpresp)
            }).finally(() => {
                this.$emit('procesar-fin')
            })
        },
        pair_select_handler:function(data){
            this.par_id = data.value
        }
    }    
}
</script>