<template>
    <q-dialog v-model="abierto" transition-show="flip-down" transition-hide="flip-up">
      <q-card style="min-width:400px;"> 
            <div v-if="httpresponses.length > 0">
                <div v-for="elemento in httpresponses" :key="elemento.id">
                    <q-toolbar>                    
                        <q-toolbar-title class="q-pt-xs text-body2 text-deep-orange-10">{{elemento.title}}</q-toolbar-title>                               
                    </q-toolbar>    
                    <q-separator/>
                    <q-card-section class="q-pt-md q-pb-xs">
                        <span class="text-body2">{{elemento.message}}</span>
                    </q-card-section>     
                    <q-card-section class="q-pt-none q-mt-none" v-if="elemento.errors.length > 0">
                        <div>
                            <ul class="q-mt-none text-red">
                                <li v-for="error in elemento.errors" v-bind:key="error">
                                    {{error}} 
                                </li>
                            </ul>
                        </div>
                    </q-card-section>  
                    <q-card-section class="q-pt-none q-mt-none" v-if="elemento.errors.length > 0 || elemento.stacktrace.length > 0">
                        <div class="text-body2 text-red text-weight-bold">URL petición</div><div>{{elemento.url}}</div>
                    </q-card-section>            
                    <q-card-section class="q-pt-none q-mt-none" v-if="elemento.errors.length > 0 || elemento.stacktrace.length > 0">                
                        <div class="text-body2 text-red text-weight-bold">Parámetros de Petición</div>
                        <ul class="q-mt-none">
                            <li v-for="(value, key) in elemento.parametros" v-bind:key="key">
                                {{key}}:{{value}}
                            </li>
                        </ul>
                    </q-card-section>
                    <q-card-section class="q-pt-none q-mt-none" v-if="elemento.stacktrace.length > 0">
                        <div class="text-body2subtitle1 text-red text-weight-bold">Stacktrace</div>
                        <div v-for="(error,index) in elemento.stacktrace" v-bind:key="error">
                            <span class="text-blue">{{index}}: </span><div class="text-purple">{{error}}</div>
                        </div>
                    </q-card-section>                 
                </div>
            </div>
            <div v-if="msgs.length > 0">
                <q-toolbar>                    
                    <q-toolbar-title class="q-pt-xs text-body2 text-deep-orange-10">Información</q-toolbar-title>                               
                </q-toolbar>
                <q-separator/>
                <div v-for="mensaje in msgs" :key="mensaje">
                    <ul>
                        <li class="text-blue-10 text-body2">{{ mensaje }}</li>
                    </ul>
                </div>
            </div>
        <q-separator/>
        <q-card-actions align="right">
            <q-btn dense color="blue-10" v-close-popup @click="btn_ok_handler">OK</q-btn>
            <q-btn flat v-close-popup color="red-10">Cerrar</q-btn>
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
            httpresponses:function(){
                console.log("ola k ase")                
                let elementos = this.$store.state.messagebox.httpresponses                
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
            },
            msgs: function(){
                return this.$store.state.messagebox.msgs
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
                if (appdata == null){
                    return "No se ha enviado una respuesta del servidor appdata=null"
                }
                return appdata.message
            },
            get_errors:function(httpresp){
                let appdata = httpresp.data
                if (appdata == null){
                    return []
                }
                return appdata.errors
            },
            get_stacktrace:function(httpresp){
                let appdata = httpresp.data                   
                if (appdata == null || appdata.stacktrace == null){
                    return []
                }
                console.log(appdata.stacktrace)

                return appdata.stacktrace
            },
            get_url:function(httpresp){                
                return httpresp.config.url
            },
            get_parametros:function(httpresp){   
                console.log(typeof httpresp.config.data)      
                let parametros = {}                       
                if (httpresp.config.data == undefined){
                    return {}
                }else if (httpresp.config.data instanceof FormData){
                    for (const pair of httpresp.config.data.entries()) {
                        let nom_parameter = pair[0]
                        let val_parameter = pair[1]
                        if (nom_parameter instanceof File){
                            parametros[nom_parameter] = val_parameter                            
                        }
                    }
                } else {
                    parametros =  JSON.parse(httpresp.config.data)   
                }
                
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