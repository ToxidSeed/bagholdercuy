<template>
    <div>
        <q-card>
            <q-card-section class="q-pt-xs q-pb-none row">
                <div class="text-h6 text-indigo">Tipos de Cambio - Cargar</div>
                <q-space/>
                <q-btn  flat dense color="red" rounded icon="close" @click="btn_close_click_handler"/>
            </q-card-section>
            <q-card-actions align="left">
                <q-btn label="Procesar" color="green" @click="btn_procesar_click_handler"/>                
            </q-card-actions>
            <q-card-section class="row">
                <!--
                <div  class="row">
                    <div class="col-6">
                        <q-input label="Desde" mask="##/##/####" fill-mask="#" v-model="desde"/>                    
                    </div>                                
                </div>-->
                <!--<q-input stack-label label="Pares" v-model="pares" class="text-uppercase"/>-->
                <SelectPair class="col-6" v-on:par-select="par_select_handler"/>
            </q-card-section>                               
            <q-card-section class="q-pt-none">
                <!--<q-chip removable v-model="icecream" @remove="log('Icecream')" color="primary" text-color="white" icon="cake">-->                
                <q-chip removable v-for="(props, key) in pares" v-bind:key="key" color="primary" 
                text-color="white" v-model="pares[key].active"
                @remove="remove_chip_handler(key)"
                >
                    {{props.label}}
                </q-chip>            
            </q-card-section>
        </q-card>
        <MessageBox ref="msgbox"/>
        <Confirmar v-model="confirmar_dialog.open" :msg="confirmar_dialog.msg" v-on:ok="procesar"/>
    </div>
</template>
<script>
import SelectPair from '@/components/SelectPair.vue'
import MessageBox from '@/components/MessageBox.vue'
import Confirmar from '@/components/dialogs/Confirmar.vue';

export default {
    name:"PanelCurrencyExchangeRateLoader",
    components:{
        MessageBox,
        SelectPair,
        Confirmar
    },
    data: () => {
        return {            
            pares:{},
            confirmar_dialog:{
                open:false,
                msg:""
            }
        }
    },
    mounted:function(){
        this.$emit('open', 25)
    },
    destroyed:function(){
        this.$emit('close')
    },    
    methods:{        
        btn_close_click_handler:function(){
            this.$router.push({name:'currencyexchange',params:{inFirstPanelSize:0}})      
            //this.$emit('close',0)            
        },
        btn_cancelar_click:function(){
            this.$emit('btn_cancelar_click')
        },
        btn_procesar_click_handler:function(){
            this.confirmar_dialog.open = true
            this.confirmar_dialog.msg = "Se va a procesar la carga de los pares seleccionados, ¿Desea continuar?"
        },
        par_select_handler:function(selected){
            let newobj = this.pares
            let key = "par_"+selected.value
            let props = {
                active:true,
                label:selected.label
            }
            newobj[key] = props
            this.pares = {}
            this.pares = newobj            
        },
        remove_chip_handler:function(key){            
            let newobj = this.pares
            delete newobj[key]
            this.pares = {}
            this.pares = newobj            
        },
        procesar:function(){
            this.$http.post('CurrencyExchangeManager/DataLoader/do',{                
                pares:this.pares
            }).then(httpresp => {
                this.$refs.msgbox.httpresp(httpresp)                
            })
        }
    }
}
</script>