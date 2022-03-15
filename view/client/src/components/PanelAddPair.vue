<template>
    <div>
        <div class="row">
            <div  class="col-10">
            <SelectMoneda/>
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
    data:() => {
        return {
            currency_symbol:""
        }
    },
    methods:{
        add_pair:function(){
            this.$emit('add-pair-btn-click')
        }
    }
}
</script>