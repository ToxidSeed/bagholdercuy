<template>
    <q-select
        color="blue-10"
        v-model="mes"
        use-input
        :options="options"
        @filter="filterFn"
        fill-input
        hide-selected
        @input="select"
        stack-label
        label="mes"
    >
    </q-select>
</template>
<script>
import {get_postconfig} from '@/common/request.js';
export default {
    name:"SelectMesesOrden",
    props:{
        in_anyo:{
            type:String,
            default:""
        },
        in_mes:{
            type:String,
            default:""
        }
    },
    data: () => {
        return {
            mes:"",
            options:[]
        }
    },
    mounted:function(){
        this.mes = this.in_mes
    },
    methods:{
        filterFn:function(val, update){            
            let postconfig = get_postconfig()
            this.options = []
            this.$http.post('/OrdenManager/Buscador/get_meses',{
                anyo:this.in_anyo
            },postconfig).then(httpresp => {
                let appresp = httpresp.data
                if(appresp.success == false){
                    this.$emit("httperror",httpresp)
                    return
                }                
                appresp.data.forEach(element => {
                    this.options.push(element.mes)
                });                
            })
            update()
        },
        select:function(selected){
            console.log(selected)
            this.$emit('select',selected)
        }
    }
}
</script>