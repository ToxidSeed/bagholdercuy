<template>
    <div>
        <div class="row">
            <div  class="col-10">
            <SelectMoneda 
            v-on:moneda-select="select_currency"
            />
            </div>
            <div class="col-2">
                <q-btn color="green" round dense icon="fa fa-plus" @click="add_pair"/>
            </div>
        </div>
    </div>
</template>
<script>
import SelectMoneda from './SelectMoneda.vue'

export default {
    name:"PanelAddPair",
    components:{
        SelectMoneda
    },
    props:{
        in_currency_base_symbol:{
            type:String,
            default:""
        }
    },
    data:() => {
        return {
            currency_ref_symbol:""
        }
    },
    methods:{
        add_pair:function(){
            console.log(this.in_currency_base_symbol)
            var pair = {
                "base": this.in_currency_base_symbol,
                "ref": this.currency_ref_symbol
            }
            this.$emit("add-pair-btn-click", pair)
        },
        select_currency:function(currency){
            this.currency_ref_symbol = currency.value
        }
    }
}
</script>