<template>
    <div>        
        <div class="row">                
            <!--<q-card  class="col-3 q-mt-xs q-ml-md">-->
                <!--<q-input v-model="symbol" label="Symbol" dense />-->
                <!--@filter="filterFn"-->
            <q-card class="col-4 q-pa-sm">
                <q-card-section class="q-pa-xs">
                    <div class="text-h6">Series</div>                    
                </q-card-section>
                <q-card bordered>
                    <q-card-section>                        
                        <SelectSymbol
                            v-on:select-symbol="sel_symbol"
                        />
                        <div class="text-h6 text-weight-bold">{{symbol.value}}</div>
                        <div>{{symbol.name}}</div>
                    </q-card-section>
                </q-card>                
                <q-card-section class="q-pa-none">                                        
                    <div class="row">
                        <q-select 
                        class="col-6"
                        v-model="frequency" 
                        :options="options" 
                        label="Frequency" 
                        dense 
                        />
                        <q-select 
                        class="col-6 q-pl-xs"                        
                        v-model="method" 
                        :options="methods" 
                        label="Method" 
                        dense 
                        />
                    </div>                    
                </q-card-section>
                <q-card-actions>
                    <q-btn color="primary" label="Load" class="q-mt-xs" @click="load"/>
                    <q-btn color="primary" label="Reset" class="q-mt-xs q-ml-xs" @click="load"/>
                </q-card-actions>
            </q-card >            
        </div>
        <MsgBox ref="msgbox"/>
    </div>
</template>
<script>
//import MessageBox from './MessageBox.vue';
import SelectSymbol from "@/components/SelectSymbol.vue"
import MsgBox from "@/components/MessageBox.vue"

export default {
    name:"DataLoader",
    components:{        
        SelectSymbol,
        MsgBox
    },
    props:{
        action:{
            type:String,
            default:"",
        }
    },
    data:() => {
        return {            
            country:"",
            frequency:"daily",
            symbol:{
                value:"",
                name:""
            },
            selected_symbol:{},
            symbol_list:[],
            options:['daily', 'weekly', 'monthly', 'yearly'],
            methods:['replace','append'],
            method:"replace",
            loading:false,
            asset_type:{
                stock:true,
                etf:true,
                options:true
            }
        }
    },    
    watch:{
        action:function(oldval){
            console.log(oldval)
        }
    },
    mounted:function(){
        console.log(this.action)
    },
    methods:{
        load:function(){
            var symbol_value = this.symbol.value
            this.$http.post(
            '/SerieManager/SerieManager/load',{
                symbol:symbol_value,
                method:this.method,
                frequency:this.frequency
            }).then(httpresponse => {
                let appresp = httpresponse.data
                console.log(appresp)
                this.$refs.msgbox.httpresp(httpresponse)
            })
        },
        sel_symbol:function(selected){            
            //this.selected_symbol = selected       
            this.symbol.value = selected.value
            this.symbol.name = selected.label    
            console.log(selected)
        }

    }
}
</script>