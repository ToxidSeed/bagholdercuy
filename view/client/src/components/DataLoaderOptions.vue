<template>
    <div>
    <q-card>                 
        <q-card-section class="q-pa-xs">
            <div class="text-h6 text-blue-10">Carga masiva de contratos</div>                      
        </q-card-section>
        <q-card-section class="q-pa-xs">            
            <q-toolbar class="q-pl-xs">                                             
                <q-btn  label="Procesar" color="green" @click="procesar" icon="play_arrow" outline/>                
            </q-toolbar>
            <div class="row q-pl-xs q-pr-xs">
                <SelectSymbol  
                class="col-12"  
                v-on:select-symbol="sel_symbol"
                />    
                <div class="col-12">        
                    <div class="q-pt-xs text-indigo text-h6">{{symbol}}</div>
                    <div class="q-pt-xs text-subtitle1">{{symbol_nombre}}</div>
                </div>
                <q-input v-model="fch_expiracion" stack-label label="Expiración" mask="##/##/####" placeholder="dd/mm/yyyy" color="blue-10"/>
            </div>            
        </q-card-section>      
        <q-inner-loading :showing="loading">
            <q-spinner-gears size="50px" color="primary" />
        </q-inner-loading>  
    </q-card>   
     <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import MessageBox from './dialogs/MessageBox.vue'
import SelectSymbol from '@/components/SelectSymbol.vue'
import {postconfig} from '@/common/request.js'
//import date from 'date-and-time'

export default {
    name:"DataloaderOptions",
    components:{
        SelectSymbol,
        MessageBox
    },
    data:() => {
        return{
            loading:false,
            symbol:"",
            fch_expiracion:"",
            symbol_nombre:"",
            symbol_list:[],
            selected_symbol:{}
        }
    },
    methods:{
        sel_symbol:function(selected){      
            console.log(selected)      
            this.symbol = selected.value
            this.symbol_nombre = selected.label
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
                    symbol:val,
                    asset_type:"stock"
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
            
        },
        procesar:function(){
            //let fch_expiracion = ""

            /*
            if (this.fch_expiracion != ""){
                fch_expiracion = date.transform(this.fch_expiracion,"DD/MM/YYYY","YYYY-MM-DD")
            }       
            */     

            this.loading = true
            this.$http.post('/OpcionesContrato/SymbolLoader/load',{
                cod_symbol:this.symbol,
                fch_expiracion:this.fch_expiracion,
            },
            postconfig()
            ).then(httpresp => {
                this.$refs.msgbox.httpresp(httpresp)                
            }).catch(err => {
                console.log(err)
            }).then(() => {
                this.loading = false
                this.$emit('procesar-completado')
            })
        }
    }
}
</script>