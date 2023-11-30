<template>
    <q-select   
        ref="selsymbol"                                     
        :label="label"
        stack-label
        v-model="symbol"  
        color="blue-10"                
        use-input
        hide-selected                                              
        fill-input        
        input-debounce="1000"
        @filter="filterFn"
        @input="sel_symbol"
        :options="symbol_list"                            
        clearable      
        :readonly="readonly"              
    >
    <template v-slot:option="scope">
        <q-item        
        v-bind="scope.itemProps"
        v-on="scope.itemEvents"
        >
            <q-item-section>
                <span class="text-blue-10 text-bold">{{scope.opt.value}}</span><span>{{ scope.opt.label }}</span>
            </q-item-section>
        </q-item>
    </template>
    </q-select>
    
</template>
<script>
import {headers} from '@/common/common.js'

export default {
    name:"SelectSymbol",
    props:{
        in_symbol:{
            type:String,
            default:""
        },
        readonly:{
            type:Boolean,
            default:false
        },
        label:{
            type:String,
            default:"Buscar Symbol"
        }
    },    
    data:() => {
        return {
            symbol:"",
            symbol_list:[]
        }
    },
    mounted:function(){        
        if (this.in_symbol != ""){
            this.symbol = {
                value:this.in_symbol,
                label:this.in_symbol
            }            
        }        
    },
    methods:{
        sel_symbol:function(selected){            
            //this.symbol = selected
            this.symbol=""
            this.$refs.selsymbol.blur()            
            this.$emit('select-symbol',selected)   
        },
        filterFn:function(val, update ) {  
            console.log(val)
            if (val === '') {
                update(() => {
                    this.symbol_list = []
    
                    // here you have access to "ref" which
                    // is the Vue reference of the QSelect
                })
                this.symbol = ""                
            }else{
                this.$http.post(
                'SymbolManager/SymbolFinder/buscar_por_texto',{
                    texto:val                    
                },{
                    headers:headers()
                }).then(httpresponse => {
                    var appresponse = httpresponse.data
                    //console.log(appresponse.data)
                    /*this.symbol_list = appresponse.data*/
                    var options = []
                    for (let element of appresponse.data){
                        options.push({
                            "id_symbol": element["id"],
                            "value":element["symbol"],
                            "label":element["name"]
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