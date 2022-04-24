<template>
    <q-select
        :label="label"
        v-model="selected"
        use-input
        hide-selected
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
                this.$http.post('CurrencyPairManager/PairFinder/get_list_by_text',{
                    search_text:val
                }).then(httpresponse => {
                    var appdata = httpresponse.data
                    var options = []
                    for (let elem of appdata.data){
                        options.push({
                            "value":elem["pair_id"],
                            "label":elem["pair_name"]
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