<template>
    <div>        
        <q-dialog v-model="open">
            <q-card style="width:450px;">
                <q-toolbar>
                    <q-toolbar-title class="text-h6 text-blue-10">
                    Carga de series desde Csv NASDAQ
                    </q-toolbar-title>
                </q-toolbar>
                <q-separator/>                
                <q-card-section>
                    <SelectSymbol  v-on:select-symbol="select_symbol"/>
                    <div class="col-12 q-pt-xs">
                        <span class="text-subtitle1 text-blue-10">
                            {{ cod_symbol }}
                        </span>
                        <span>
                            {{ nom_symbol }}
                        </span>
                    </div>
                    <q-file
                        v-model="fichero"
                        label="Seleccionar fichero de opciones"
                        use-chips        
                        color="blue-10"
                        stack-label                
                    >                
                        <template v-slot:prepend>
                            <q-icon name="attach_file" />
                        </template>
                    </q-file>    
                    <q-select v-model="modo_carga" :options="lista_modos_carga" label="Standard" stack-label/>                            
                </q-card-section>            
                <q-inner-loading :showing="loading">
                    <q-spinner-gears size="50px" color="primary" />
                </q-inner-loading>
                <q-card-actions align="right">
                    <q-btn flat @click="procesar" no-caps color="blue-10" icon="play_arrow">Procesar</q-btn>
                    <q-btn flat v-close-popup no-caps icon="close" color="red-10">Cerrar</q-btn>
                </q-card-actions>
            </q-card>  
        </q-dialog>      
    </div>
</template>
<script>
import SelectSymbol from "@/components/SelectSymbol.vue"
import {HttpResponseHandler} from "@/common/http-response-handler"

import {get_postconfig} from '@/common/request.js'
export default {
    name:"PanelNasdaqCsvLoader",
    props:{
        value:{
            required:true
        }
    },
    components:{
        SelectSymbol
    },
    watch:{
        open:function(newval){
            this.$emit('input',newval)
        },
        value:function(newval){
            this.open = newval
        }
    },
    data(){
        return {
            open: this.value,
            fichero:null,
            cod_symbol:"",
            nom_symbol:"",
            loading: false,
            modo_carga:"",
            lista_modos_carga:["Agregar","Reemplazar"]
        }
    },
    methods:{        
        select_symbol:function(symbol){
            this.cod_symbol = symbol.value
            this.nom_symbol = symbol.label
        },
        procesar:function(){
            this.loading = true
            let postconfig = get_postconfig()
            postconfig.headers['Content-Type'] = "multipart/form-data"
            let form_data = new FormData();            

            form_data.append("fichero", this.fichero)
            form_data.append("cod_symbol", this.cod_symbol)            
            form_data.append("modo_carga", this.modo_carga)

            console.log(postconfig)

            this.$http.post(
                '/SerieManager/NasdaqCsvLoader/load',form_data,postconfig                
            ).then(httpresp => {
                console.log(httpresp)
                HttpResponseHandler.showMessage(httpresp)
            }).finally(() => {
                this.loading = false
            })
        }
    }
}
</script>
