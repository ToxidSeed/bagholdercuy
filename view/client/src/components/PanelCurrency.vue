<template>
    <div>
        <q-card>
            <q-card-section>
                <div class="text-h6">Currency</div>
            </q-card-section>
            <q-card-section>
                <div class="row">
                    <q-input v-model="currency_id" readonly label="ID" class="col-4" label-color="indigo"/>
                    <q-input v-model="symbol" label="Symbol" class="col-8" @change="symbol_update_handler"/>
                </div>
                <q-input v-model="currency_name" label="Nombre"/>                
            </q-card-section>
            <!--<q-card-actions align="right">
                <q-btn color="primary" @click="btn_save_click_handler">Guardar</q-btn>
                <q-btn color="orange">Cancelar</q-btn>                
            </q-card-actions>-->
        </q-card>
    </div>
</template>
<script>

export default {
    name:"PanelCurrency",
    props:{
        in_data:{
            type:Object,
            default: () => {}
        }
    },
    data: () => {
        return {
            currency_id:"#",
            symbol: "",
            currency_name:"",
            fec_registro:""
        }
    },
    watch:{
        /*symbol:function(new_value, old_value){    
            if (new_value.length == 3){
                var symbol_obj = {"new":new_value,"old":old_value}    
                console.log(symbol_obj)    
                this.$emit("symbol-changed", symbol_obj)
                //@change="symbol_update_handler"
            }            
        }*/
    },
    mounted:function(){
        this.symbol = "xxx"
    },
    methods:{
        get_currency_data:function(){
            return this.$data
        },
        symbol_update_handler:function(){            
            this.$emit("symbol-changed", {"new":this.symbol})
        },
        btn_save_click_handler:function(){
            this.$emit("btn-save-click")
        }
    },
    beforeDestroy:function(){
        this.$emit('panel-close',this.$data)
    },
    created:function(){
        if (Object.keys(this.in_data).length != 0){            
            this.currency_id = this.in_data.currency_id
            this.symbol = this.in_data.symbol
            this.currency_name = this.in_data.currency_name
        }
    }
}
</script>