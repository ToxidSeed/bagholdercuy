<template>
    <div>
        <q-select                                        
        label="Moneda"
        v-model="fund"  
        use-input
        hide-selected                                      
        fill-input
        input-debounce="1000"
        @filter="filter_fn"
        @input="sel_funds"
        :options="list"                            
        clearable                    
        />
    </div>
</template>
<script>
export default {
    name:"SelectFunds",
    data: () => {
        return {
            fund:"",
            list:[]
        }
    },
    methods:{
        sel_funds:function(selected){
            this.fund = selected
            this.$emit('fund-select',this.fund)
        },
        filter_fn:function(val, update){
            this.$http.post('FundsManager/FundsManager/get_funds',{
                symbol:val
            }).then(httpresponse => {
                var appresponse = httpresponse.data
                var options = []
                for (let elem of appresponse.data){
                    var label = elem["moneda_symbol"]+" - "+elem["importe"]
                    options.push({
                        "symbol":elem["moneda_symbol"],
                        "label":label
                    })
                }

                update(() => {
                    this.list = options
                })
            })
        }
    }
}
</script>