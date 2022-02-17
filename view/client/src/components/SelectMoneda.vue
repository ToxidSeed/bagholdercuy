<template>
    <q-select                                        
        :label="cmp_label"
        v-model="moneda"  
        use-input
        hide-selected                                      
        fill-input
        input-debounce="1000"
        @filter="filter_fn"
        @input="sel_moneda"
        :options="list"
        dense                    
        clearable                    
    />
</template>
<script>
export default {
    name:"SelectMoneda",
    props:{
        label:{
            type:String,
            default:""
        }
    },
    computed:{
        cmp_label:function(){
            if (this.label == ""){
                return "Moneda"
            }
            return this.label
        }
    },
    data:() => {
        return {
            /**Se pone "" en la variable moneda porque si se pone como objeto {} falla, si no recuerdas volver a probarlo**/
            moneda:"",
            //moneda_id:"",
            list:[]
        }
    },
    methods:{
        sel_moneda:function(selected){            
            this.moneda = selected         
            console.log(this.moneda)   
        },
        filter_fn:function(val, update){
           if (val == ''){
               update(() => {
                   this.list = []
               })
           }else{
               this.$http.post('MonedaManager/MonedaManager/get_list',{
                   search_text:val
               }).then(httpresponse => {
                   
                   var appresponse = httpresponse.data
                   var options = []
                   for (let elem of appresponse.data){
                       options.push({
                           "value":elem["symbol"],
                           "label":elem["symbol"],
                           "moneda_id":elem["moneda_id"]
                       })
                   }

                   update(() =>{
                       this.list = options
                   })
               })
           }
        }
    }
}
</script>