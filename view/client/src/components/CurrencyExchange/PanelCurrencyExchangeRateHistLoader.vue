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
                <q-input label="Pares" v-model="pares"/>                                    
            </q-card-section>            
            <q-separator/>
            <q-card-actions align="right">
                <q-btn label="aceptar" color="primary" @click="btn_aceptar_click"/>
                <q-btn label="cancelar" color="red" @click="btn_cancelar_click"/>
            </q-card-actions>
        </q-card>
    </div>
</template>
<script>
export default {
    name:"PanelCurrencyExchangeRateHistLoader",
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
                console.log(httpresp)
                var appresp = httpresp.data
                var data = appresp.data
                console.log(data)
            })
        }
    }
}
</script>