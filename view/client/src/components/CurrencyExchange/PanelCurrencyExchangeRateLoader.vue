<template>
    <div>
        <q-card>
            <q-card-section class="q-pt-xs q-pb-none row">
                <div class="text-h6 text-indigo">Tipos de Cambio - Cargar</div>
                <q-space/>
                <q-btn  flat dense color="red" rounded icon="close" @click="btn_close_click_handler"/>
            </q-card-section>
            <q-card-actions align="left">
                <q-btn label="Procesar" color="green" @click="btn_aceptar_click"/>                
            </q-card-actions>
            <q-card-section>
                <!--
                <div  class="row">
                    <div class="col-6">
                        <q-input label="Desde" mask="##/##/####" fill-mask="#" v-model="desde"/>                    
                    </div>                                
                </div>-->
                <q-input stack-label label="Pares" v-model="pares" class="text-uppercase"/>                                    
            </q-card-section>                               
        </q-card>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue'

export default {
    name:"PanelCurrencyExchangeRateLoader",
    components:{
        MessageBox
    },
    data: () => {
        return {            
            pares:""
        }
    },
    mounted:function(){
        this.$emit('open', 30)
    },
    methods:{        
        btn_close_click_handler:function(){
            this.$router.push({name:'currencyexchange',params:{inFirstPanelSize:0}})      
            this.$emit('close',0)            
        },
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