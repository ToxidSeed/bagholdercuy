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
    props:{
        throwerror:{
            type:Boolean,
            default:true
        }
    },
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
            update(()=>{})
            this.$http.post('FundsManager/FundsManager/get_funds',{
                symbol:val
            },{
                headers:{
                    'Authorization':localStorage.getItem('token')
                }
            }).then(httpresponse => {                
                let appresponse = httpresponse.data
                if(appresponse.success == false){
                    if(this.throwerror == true){
                        this.$emit('httperror',httpresponse)
                    }                    
                    if(appresponse.expired == true){
                        this.$router.push({name:"login"})                        
                    }                    
                }else{
                    let options = []                
                    for (let elem of appresponse.data){
                        var label = elem["moneda"]+" - "+elem["importe_fmt"]
                        options.push({
                            "symbol":elem["moneda"],
                            "label":label
                        })
                    }                
                    update(() => {
                        this.list = options
                    })
                }                                                                               
            }).then(()=>{
                console.log('final')
            })  
        }
    }
}
</script>