<template>
    <div>
        <q-card>
            <q-toolbar > 
                <q-toolbar-title class="text-blue-10">
                    Symbols
                </q-toolbar-title> 
                <q-btn   dense icon="close" to="/opciones" color="red"/>
            </q-toolbar>
            <q-separator/>
            <q-toolbar>
                <div class="q-gutter-xs">
                    <q-btn label="Guardar" color="blue-10" @click="save"/>                
                    <q-btn label="Carga Masiva" icon="group_work" flat dense color="blue-10" @click="confirm=true" class="text-capitalize"/>
                </div>
            </q-toolbar>  
            <q-separator/>          
            <q-card-section>                
                <div class="row">
                    <q-input stack-label label="ID" readonly v-model="symbol_id" class="col-5"/>
                    <q-input stack-label label="symbol" v-model="symbol" class="col-7 q-pl-xs"/>                    
                </div>
                <q-input stack-label  label="Name" v-model="name" />
                <div class="row">
                    <q-input stack-label label="Region" v-model="region" class="col-5"/>
                    <q-input stack-label label="Exchange" v-model="exchange" class="col-7 q-pl-xs"/>
                </div>
                <div class="row">
                    <q-input stack-label readonly label="Fch. Registro" v-model="fec_registro" class="col-5 q-pl-xs"/>
                    <q-input stack-label readonly label="Fch. Audit" v-model="fec_audit" class="col-7 q-pl-xs"/>
                </div>
            </q-card-section>         
            <q-inner-loading :showing="loading">
                <q-spinner-gears size="50px" color="primary" />
            </q-inner-loading>     
        </q-card>        
        <q-dialog v-model="confirm" persistent>
            <q-card>
                <q-card-section class="row items-center">                    
                    <div class="col-1">
                        <q-avatar icon="directions_run" color="green" text-color="white" />
                    </div>
                    <div class="col-11">
                        <div class="q-ml-sm">Se va a proceder a realizar la carga masiva de symbols, si alguno ya se encuentra registrado se omitirá, ¿Desea continuar?</div>                    
                    </div>
                </q-card-section>

                <q-card-actions align="right">
                    <q-btn flat label="Ejecutar" color="primary" 
                    @click="load" v-close-popup />
                    <q-btn flat label="Cancelar" color="primary" v-close-popup />                
                </q-card-actions>
            </q-card>
        </q-dialog>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '../MessageBox.vue'
import {postconfig} from '@/common/request.js'

export default {
    name:"PanelSymbol",
    components:{
        MessageBox
    },
    data: () => {
        return {
            loading:false,
            confirm:false,
            symbol_id:"#",
            symbol:"",
            name:"",
            region:"",
            exchange:"",
            fec_registro:"",
            fec_audit:""
        }
    },
    mounted:function(){
        
    },
    methods:{
        save:function(){
            this.loading=true
            this.$http.post('SymbolManager/SymbolManager/save',{
                symbol_id:this.symbol_id,
                symbol:this.symbol,
                symbol_name: this.name,
                region:this.region,
                exchange:this.exchange,
                asset_type:""
            }).then(httpresponse => {
                var appdata = httpresponse
                this.$refs.msgbox.new(appdata.data)
            }).catch(error => {
                console.log(error)
            }).then(()=>{
                this.loading=false
            })
        },
        load:function(){
            this.loading=true
            this.$http.post('/SymbolManager/DataLoader/do',{},postconfig())
            .then(httpresp => {                
                this.$refs.msgbox.httpresp(httpresp)
            }).catch(error => {
                console.log(error)
            }).then(() => {
                this.loading = false
            })
        }
    }
}
</script>