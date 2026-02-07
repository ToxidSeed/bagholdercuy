<template>
    <div>
        <q-dialog v-model="open">
            <q-card style="min-width: 500px;">
                <q-toolbar>
                    <q-toolbar-title class="text-blue-10">
                        Symbols
                    </q-toolbar-title>
                    <q-btn flat dense icon="close" to="/opciones" color="red" />
                </q-toolbar>
                <q-separator />
                <q-card-section>
                    <div class="row">
                        <q-input stack-label label="ID" readonly v-model="symbol_id" class="col-3" />
                        <q-input stack-label label="Symbol" v-model="symbol" class="col q-pl-xs"
                            :rules="[val => !!val || 'Campo requerido']" ref="symbol" />
                    </div>
                    <q-input stack-label label="Name" v-model="nombre" :rules="[val => !!val || 'Campo requerido']" ref="nombre"/>
                    <div class="row">
                        <q-input stack-label label="Region" v-model="region" class="col-5" />
                        <q-input stack-label label="Exchange" v-model="exchange" class="col-7 q-pl-xs" />
                    </div>
                    <div class="row">
                        <q-input stack-label readonly label="Fch. Registro" v-model="fec_registro"
                            class="col-5 q-pl-xs" />
                        <q-input stack-label readonly label="Fch. Audit" v-model="fec_audit" class="col-7 q-pl-xs" />
                    </div>
                </q-card-section>
                <q-card-actions align="right">
                    <q-btn label="Guardar" color="blue-10" @click="save" />
                    <q-btn flat label="Cancelar" color="red-10" v-close-popup />
                </q-card-actions>
                <q-inner-loading :showing="loading">
                    <q-spinner-gears size="50px" color="primary" />
                </q-inner-loading>
            </q-card>
        </q-dialog>        
    </div>
</template>
<script>

import {postconfig} from "@/common/request.js"
import store from "../../store/store"
export default {
    name:"WinGestionSymbol",
    components:{
        
    },
    props:{
        value:{
            required:true
        },
        proceso:{
            type:String,
            required:true
        }
    },
    watch:{
        open:function(newVal){
            this.$emit('input',newVal)
        },
        value:function(newVal){
            this.open = newVal
        }
    },
    data(){
        return {
            open: this.value,
            loading:false,
            symbol_id:"",
            symbol:"",
            nombre:"",
            region:"",
            exchange:"",
            fec_registro:"",
            fec_audit:""            
        }
    },
    methods:{
        validateSave:function(){
            const vals = [
                this.$refs.symbol.validate(),    
                this.$refs.nombre.validate()
            ]
            return vals.every(elem => elem == true)            
        },
        save:function(){
            if (!this.validateSave()){
                return
            }

            this.loading=true
            this.$http.post('SymbolManager/SymbolManager/save',{
                symbol_id:this.symbol_id,
                symbol:this.symbol,
                symbol_name: this.nombre,
                region:this.region,
                exchange:this.exchange,
                asset_type:""
            },postconfig()).then(httpresponse => {                
                store.dispatch("incluir_httpresp_si_apperror", httpresponse)
            }).catch(error => {
                console.log(error)
            }).then(()=>{
                this.loading=false
            })
        }
    }
}
</script>