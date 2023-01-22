<template>
    <div>
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
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import {postconfig} from '@/common/request.js';
import MessageBox from '@/components/MessageBox.vue';

export default {
    name:"SelectPair",
    props:{
        in_label:{
            type:String,
            default:""
        }
    },
    components:{
        MessageBox
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
            if (selected == null){
                this.$emit('par-deselect')                
            }else{
                this.selected = selected
                this.$emit('par-select',this.selected)            
            }            
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
                    this.$refs.msgbox.http_resp_on_error(httpresponse)

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