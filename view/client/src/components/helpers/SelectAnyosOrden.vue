<template>    
    <q-select
        color="blue-10"
        v-model="anyo"
        use-input
        :options="options"
        @filter="filterFn"    
        fill-input    
        hide-selected                                      
        @input="select"
        stack-label        
        label="Año"
    >
    </q-select>    
</template>
<script>
import {get_postconfig} from '@/common/request.js';
export default {    
    name:"SelectAnyosOrden",
    props:{
        in_anyo:{
            type:String,
            default:""
        }
    },
    data: () => {
        return {
            anyo:"",
            options:[]
        }
    },
    mounted:function(){
        this.anyo = this.in_anyo
        //this.get_anyos()
    },
    methods:{
        filterFn:function(val, update){               
            let postconfig = get_postconfig()
            this.$http.post('/OrdenManager/Buscador/get_anyos',{},postconfig)
            .then(httpresp => {
                let appresp = httpresp.data
                if(appresp.success == false){
                    this.$emit("httperror",httpresp)
                    return
                }
                //this.data = appresp.data
                let options = []
                appresp.data.forEach(element => {
                    options.push(String(element.anyo).trim())
                });
                
                update(() =>{
                    this.options = options
                })                    
            })
        },
        select:function(selected){
            console.log(selected)
            this.$emit("select",selected)
        }
    }
}
</script>