<template>
    <q-select                                        
        label="Symbol"
        v-model="symbol"  
        use-input
        hide-selected                                      
        fill-input
        input-debounce="1000"
        @filter="filterFn"
        @input="sel_symbol"
        :options="symbol_list"                            
        clearable                    
    />
</template>
<script>
export default {
    name:"SelectSymbol",
    data:() => {
        return {
            symbol:"",
            symbol_list:[]
        }
    },
    methods:{
        sel_symbol:function(selected){            
            this.selected_symbol = selected
            this.$emit('select-symbol',selected)   
        },
        filterFn:function(val, update ) {  
            if (val === '') {
                update(() => {
                    this.symbol_list = []
    
                    // here you have access to "ref" which
                    // is the Vue reference of the QSelect
                })
                return
            }else{
                this.$http.post(
                this.$backend_url+'DataManager/Symbol/search',{
                    symbol:val,
                    asset_type:"stock"
                }).then(httpresponse => {
                    var appresponse = httpresponse.data
                    //console.log(appresponse.data)
                    /*this.symbol_list = appresponse.data*/
                    var options = []
                    for (let element of appresponse.data){
                        options.push({
                            "value":element["symbol"],
                            "label":element["symbol"]+" ("+element["name"]+")"
                        })
                    }
                                                            
                    update(() => {
                        this.symbol_list = options                            
                    })
                })
            }
            
        }
    }
}
</script>