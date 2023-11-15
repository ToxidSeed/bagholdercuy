<template>
    <q-dialog v-model="abierto" transition-show="flip-down" transition-hide="flip-up">
      <q-card style="min-width:400px;"> 
            <div v-for="elemento in mensajes" :key="elemento.id">
                <q-toolbar>                    
                    <q-toolbar-title class="q-pt-xs text-subtitle1 text-deep-orange-10">{{elemento.title}}</q-toolbar-title>                               
                </q-toolbar>    
                <q-separator/>
                <q-card-section class="q-pt-md q-pb-xs">
                    <span class="text-subtitle1">{{elemento.message}}</span>
                </q-card-section>     
                <q-card-section class="q-pt-none q-mt-none" v-if="elemento.errors.length > 0">
                    <div>
                        <ul class="q-mt-none">
                            <li v-for="error in elemento.errors" v-bind:key="error">
                                {{error}}
                            </li>
                        </ul>
                    </div>
                </q-card-section>  
                <q-card-section class="q-pt-none q-mt-none">
                    <div class="text-subtitle1 text-red text-weight-bold">URL petición</div><div>{{elemento.url}}</div>
                </q-card-section>            
                <q-card-section class="q-pt-none q-mt-none">                
                    <div class="text-subtitle1 text-red text-weight-bold">Parámetros de Petición</div>
                    <ul class="q-mt-none">
                        <li v-for="(value, key) in elemento.parametros" v-bind:key="key">
                            {{key}}:{{value}}
                        </li>
                    </ul>
                </q-card-section>
                <q-card-section class="q-pt-none q-mt-none">
                    <div class="text-subtitle1 text-red text-weight-bold">Stacktrace</div>
                    <div v-for="error in elemento.stacktrace" v-bind:key="error">
                        {{error}}
                    </div>
                </q-card-section>                 
            </div>
        <q-card-actions align="right">
            <q-btn dense color="primary" v-close-popup @click="btn_ok_handler">OK</q-btn>
            <q-btn flat v-close-popup color="red">Cerrar</q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
</template>
<script>
//import {mapState} from 'vuex'

export default {
        name:"MessageBox",
        props:{
            config:{
                type:Object,
                default: () => {}
            }
        },
        computed: {
            abierto:{
                get(){                    
                    return this.$store.state.messagebox.open;
                },
                set(value){
                    this.$store.commit('cerrar_messagebox', value)
                }
            },  
            mensajes:function(){
                let elementos = this.$store.state.messagebox.data
                let records = []
                for (let httpresp of elementos){                    

                    records.push({
                        id:Date.now(),
                        title:"Informacion",
                        message:this.get_message(httpresp),
                        errors: this.get_errors(httpresp),
                        stacktrace: this.get_stacktrace(httpresp),
                        url: this.get_url(httpresp),
                        parametros: this.get_parametros(httpresp)
                    })
                    
                }
                return records
            }
        },            
        data () {
            return {
                title:"",
                message:"",
                action:"",
                errors:[],
                request_config:{},
                stacktrace:[],
                url:"",
                opened: false,
                caller:"",
                mostrar_info_error:false,
                msgdata:{
                    icon:"",
                    color:""
                },
                error:{
                    icon:"fa fa-exclamation",
                    color:"red"
                },
                info:{
                    icon:"fa fa-info-circle",
                    color:"primary"
                }                
            }
        },        
        mounted:function(){
            //this.interface()
        },
        methods:{    
            get_message:function(httpresp){
                let appdata = httpresp.data
                return appdata.message
            },
            get_errors:function(httpresp){
                let appdata = httpresp.data
                return appdata.errors
            },
            get_stacktrace:function(httpresp){
                let appdata = httpresp.data
                return appdata.stacktrace
            },
            get_url:function(httpresp){                
                return httpresp.config.url
            },
            get_parametros:function(httpresp){                
                let parametros =  JSON.parse(httpresp.config.data)
                console.log(parametros)
                return parametros
            },
            btn_ok_handler:function(){
                if (this.expired){
                    this.$router.push({name:"/"})
                }
            }
        }
    }
</script>
<style scoped>
.q-toolbar {
    min-height: auto;
}
</style>