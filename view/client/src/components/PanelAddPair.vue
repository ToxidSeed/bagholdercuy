<template>
    <div>
        <div class="row">
            <div  class="col-8">
            <SelectMoneda 
            v-on:moneda-select="select_currency"
            />
            </div>
            <div class="q-gutter-sm col-3 q-pl-md">
                <q-radio dense v-model="operacion" val="MUL" label="MUL" />
                <q-radio dense v-model="operacion" val="DIV" label="DIV" />
            </div>
            <div class="col-1">
                <q-btn color="green" :disable="comp_disable" round dense icon="fa fa-plus" @click="add_pair"/>
            </div>
        </div>
        <MessageBox ref="msgbox" />
    </div>
</template>
<script>
import SelectMoneda from './SelectMoneda.vue'
import MessageBox from '@/components/MessageBox.vue'

export default {
    name:"PanelAddPair",
    components:{
        SelectMoneda,
        MessageBox
    },
    props:{
        moneda_id:{
            type:String,
            default:""
        }
    },
    data:() => {
        return {            
            moneda_ref_id:"",
            operacion:"MUL"
        }
    },
    mounted:function(){
        console.log(this.moneda_id)
    },
    computed:{
        comp_disable:function(){
            if (this.moneda_id == ""){
                return true;
            }else{
                return false;
            }
        }
    },
    methods:{
        add_pair:function(){                        
            this.$http.post('/CurrencyManager/MonedaParAddController/add',{
                    base:this.moneda_id,
                    ref:this.moneda_ref_id,
                    operacion:this.operacion
                }
            ).then(httpresp => {
                this.$emit("add-par-end")
                this.$refs.msgbox.httpresp(httpresp)
            })
            
        },
        select_currency:function(currency){
            this.moneda_ref_id = currency.value
        }
    }
}
</script>