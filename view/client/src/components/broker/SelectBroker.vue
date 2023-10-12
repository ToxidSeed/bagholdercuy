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
            color="blue-10"
        >
        </q-select>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import {postconfig} from '@/common/request.js';
import MessageBox from '@/components/MessageBox.vue';

export default {
    name:"SelectBroker",
    props:{
        flg_activo:{
            type:Number,
            default:1
        },
        label:{
            type:String,
            default:"Seleccionar Broker"
        }
    },
    data() {
        return {
            selected:"",
            list:[]
        }
    },
    components:{
        MessageBox
    },
    methods:{
        sel_item:function(selected){
            if (selected == null){
                this.$emit('deselect')                
            }else{
                this.selected = selected
                this.$emit('select',this.selected)            
            }
        },
        filter_fn:function(val, update){            
            this.$http.post('/broker/BrokerManager/get_brokers',{
                    nombre:val,
                    flg_activo:this.flg_activo
            },postconfig()).then(httpresponse => {
                this.$refs.msgbox.http_resp_on_error(httpresponse)

                var appdata = httpresponse.data
                var options = []
                for (let elem of appdata.data){
                    options.push({
                        "value":elem["id_broker"],
                        "label":elem["nom_broker"]
                    })
                }
                
                update(() =>{
                    this.list = options
                })
            })
        }
    }
}
</script>