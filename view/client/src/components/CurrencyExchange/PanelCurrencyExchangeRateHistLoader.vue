<template>
    <div style="min-width: 25vw" >
        <q-card>
            <q-card-section class="q-pb-none">
                <div class="text-h6 text-indigo">Datos de Carga</div>
            </q-card-section>
            <q-card-section>
                <!--
                <div  class="row">
                    <div class="col-6">
                        <q-input label="Desde" mask="##/##/####" fill-mask="#" v-model="desde"/>                    
                    </div>                                
                </div>-->
                <q-input stack-label label="Pares" v-model="pares" class="text-uppercase"/>                                    
            </q-card-section>            
            <q-separator/>
            <q-card-actions align="right">
                <q-btn label="aceptar" color="primary" @click="btn_aceptar_click"/>
                <q-btn label="cancelar" color="red" @click="btn_cancelar_click"/>
            </q-card-actions>
        </q-card>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue'

export default {
    name:"PanelCurrencyExchangeRateHistLoader",
    components:{
        MessageBox
    },
    data: () => {
        return {            
            pares:""
        }
    },
    methods:{        
        btn_cancelar_click:function(){
            this.$emit('btn_cancelar_click')
        },
        btn_aceptar_click:function(){
            this.$http.post('CurrencyExchangeManager/DataLoader/do',{                
                pares:this.pares
            }).then(httpresp => {
                this.$refs.msgbox.httpresp(httpresp)                
            })
        }
    }
}
</script>