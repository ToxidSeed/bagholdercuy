<template>
    <q-select
        :label="label"
        v-model="selected"
        use-input
        hide-selected
        stack-label
        fill-input
        input-debounce="500"
        @filter="filter_fn"
        @input="sel_item"
        :options="list"
        clearable
    >
    </q-select>
</template>
<script>
import {postconfig} from '@/common/request.js';
export default {
    name:"SelectPair",
    props:{
        in_label:{
            type:String,
            default:""
        }
    },
    computed:{
        label:function(){
            if (this.in_label == ""){
                return "Par"
            }
            return this.in_label
        }
    },
    data:() => {
        return {
            selected:"",
            list:[]
        }
    },
    methods:{
        sel_item:function(selected){
            this.selected = selected
            this.$emit('pair-select',this.selected)
        },
        filter_fn:function(val, update){
            if (val == ''){
                update(() => {
                    this.list = []
                })
            }else{
                this.$http.post('CurrencyPairManager/ParFinder/get_list_by_text',{
                    search_text:val
                },postconfig()).then(httpresponse => {
                    var appdata = httpresponse.data
                    var options = []
                    for (let elem of appdata.data){
                        options.push({
                            "value":elem["par_id"],
                            "label":elem["nombre"]
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