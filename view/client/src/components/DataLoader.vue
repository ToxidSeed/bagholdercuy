<template>
    <div>        
        <div class="row">                
            <!--<q-card  class="col-3 q-mt-xs q-ml-md">-->
                <!--<q-input v-model="symbol" label="Symbol" dense />-->
                <!--@filter="filterFn"-->
            <q-card class="col-3 q-pa-sm">                
                <q-card-section class="q-pa-none">                    
                    <div class="text-h6">Series</div>                    
                    <q-select                                        
                        label="Symbol"
                        v-model="symbol"  
                        use-input
                        hide-selected                                      
                        fill-input
                        input-debounce="1000"
                        @filter="filterFn"
                        @input="sel_symbol"
                        :options="symbol_list"
                        dense                    
                        clearable                    
                    >                                   
                    </q-select>
                    <div class="q-gutter-sm">     
                    </div>
                    <q-select 
                    v-model="frequency" 
                    :options="options" 
                    label="Frequency" 
                    dense 
                    />
                    <q-btn color="primary" label="Load" class="q-mt-xs" @click="load"/>
                </q-card-section>
            </q-card >
            <DataloaderOptions class="col-3"/>
        </div>
    </div>
</template>
<script>
//import MessageBox from './MessageBox.vue';
import DataloaderOptions from './DataLoaderOptions.vue'

export default {
    name:"DataLoader",
    components:{
        DataloaderOptions
    },
    data:() => {
        return {            
            country:"",
            frequency:"",
            symbol:"",
            selected_symbol:{},
            symbol_list:[],
            options:['daily', 'weekly', 'monthly', 'yearly'],
            loading:false
        }
    },    
    mounted:function(){

    },
    methods:{
        load:function(){
            var symbol_value = this.symbol.value
            this.$http.post(
            this.$backend_url+'DataManager/DataManager/load',{
                symbol:symbol_value,
                frequency:this.frequency
            }).then(httpresponse => {
                console.log(httpresponse);
            })
        },
        sel_symbol:function(selected){            
            this.selected_symbol = selected            
        },

        filterFn:function(val, update ) {  
            if (val === '') {
                update(() => {
                    this.symbol_list = []
    
                    // here you have access to "ref" which
                    // is the Vue reference of the QSelect
                })
                return
            }else{
                this.$http.post(
                this.$backend_url+'DataManager/Symbol/search',{
                    symbol:val
                }).then(httpresponse => {
                    var appresponse = httpresponse.data
                    //console.log(appresponse.data)
                    /*this.symbol_list = appresponse.data*/
                    var options = []
                    for (let element of appresponse.data){
                        options.push({
                            "value":element["symbol"],
                            "label":element["symbol"]+" ("+element["name"]+")"
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