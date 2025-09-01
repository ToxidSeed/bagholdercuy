<template>
    <div>        
        <q-dialog v-model="open">
            <q-card style="width:550px;">
                <q-toolbar>
                    <q-toolbar-title class="text-h6 text-blue-10">
                    Carga de Series desde Investing CSV
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
                        ref="refFichero"
                        label="Seleccionar fichero de opciones"
                        use-chips        
                        color="blue-10"
                        stack-label  
                        :rules="rulesFichero"              
                    >                
                        <template v-slot:prepend>
                            <q-icon name="attach_file" />
                        </template>
                    </q-file>                 
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
import {postconfig} from "@/common/request.js"
import store from "../../store/store"
export default {
    name: "WinInvestingLoader",
    props:{
        value: {
            required: true
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
            nom_symbol: "",
            cod_symbol: "",
            loading:false,
            rulesFichero: [val => !!val]        
        }
    },
    methods:{
        select_symbol:function(symbol){
            this.cod_symbol = symbol.value
            this.nom_symbol = symbol.label
        },
        procesar: function(){
            let postConfig = postconfig()
            if (!this.validar()){
                return
            }            

            this.loading = true            
            postConfig.headers['Content-Type'] = "multipart/form-data"
            let form_data = new FormData();            

            form_data.append("fichero", this.fichero)
            form_data.append("cod_symbol", this.cod_symbol)                        
            
            this.$http.post(
                '/SerieManager/InvestingLoader/load',form_data,postConfig                
            ).then(httpresp => {                
                store.dispatch("incluir_httpresp_si_apperror", httpresp)
            }).finally(() => {
                this.loading = false
            })

        },
        validar: function(){
            const vals = [
                this.$refs.refFichero.validate()
            ]
            return vals.every(res => res == true);
        }
    }
}
</script>