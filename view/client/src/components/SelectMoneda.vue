<template>    
    <q-select                                        
        :label="cmp_label"
        v-model="moneda"  
        stack-label
        use-input
        hide-selected                                      
        fill-input  
        input-debounce="500"
        @filter="filter_fn"
        @input="sel_moneda"
        :options="list"                            
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
        },
        in_cod_moneda:{
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
    mounted:function(){
        if (this.in_cod_moneda != ""){
            this.moneda = {
                value: this.in_cod_moneda,
                label: this.in_cod_moneda
            }
        }
    },
    methods:{
        sel_moneda:function(selected){                    
            console.log(selected)
            this.moneda = selected.value                
            this.$emit('moneda-select',selected) 
        },
        filter_fn:function(val, update){
           if (val == ''){
               update(() => {
                   this.list = []
               })
           }else{
               this.$http.post('CurrencyManager/CurrencyManager/get_list',{
                   search_text:val
               },{
                    headers:{
                        'Authorization':localStorage.getItem('token')
                    }
                }).then(httpresp => {
                   var appresp = httpresp.data
                   if (appresp.success == false){
                       this.$emit('httperror',httpresp)                       
                   }                                   
                   if (appresp.expired == true){
                       this.$router.push({name:"login"})
                   }
                   var options = []
                   for (let elem of appresp.data){
                        let label = elem["codigo_iso"] + " - " +elem["nombre"] 
                       options.push({
                           "value":elem["codigo_iso"],
                           "label":label,
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