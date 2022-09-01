<template>
    <q-dialog v-model="opened" transition-show="flip-down" transition-hide="flip-up">
      <q-card> 
            <q-card-section class="q-pt-xs q-pb-xs" >
                <q-icon :name="msgdata.icon" size="md" :color="msgdata.color" text-color="white" /> {{title}}            
            </q-card-section>
            <q-separator/>
            <q-card-section class="q-pt-md q-pb-xs">
            {{message}}
            </q-card-section>            
            <q-card-section class="q-pt-none q-mt-none" >
                <div>
                    <ul class="q-mt-none">
                        <li v-for="item in errors" v-bind:key="item">
                            {{item}}
                        </li>
                    </ul>
                </div>
            </q-card-section>
            <q-card-section class="q-pt-none q-mt-none" v-if="mostrar_info_error">
                <div class="text-accent text-weight-bold">URL petición</div><div>{{url}}</div>
            </q-card-section>
            <q-card-section class="q-pt-none q-mt-none" v-if="mostrar_info_error">
                <div class="text-red text-weight-bold">Stacktrace</div>
                <div v-for="error in stacktrace" v-bind:key="error">
                    {{error}}
                </div>
            </q-card-section>            
        <q-separator />
        <q-card-actions align="right">
            <q-btn dense color="primary" v-close-popup>OK</q-btn>
            <q-btn flat v-close-popup>Cerrar</q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
</template>
<script>
    export default {
        name:"MessageBox",
        data () {
            return {
                title:"",
                message:"",
                action:"",
                errors:[],
                stacktrace:[],
                url:"",
                opened: false,
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
        methods:{            
            new:function(args=null){
                this.errors = []
                if (args.title != undefined){
                    this.title = args.title
                }
                if (args.action != undefined){
                    this.action = args.action
                }
                if (args.message != undefined){
                    this.message = args.message
                }       
                this.opened = true      
            },
            httpresp:function(httpresp=null){
                this.errors = []
                this.stacktrace=[]
                this.url = ""
                this.opened = true;
                this.url = httpresp.config.url
                var appdata = httpresp.data
                this.appresp(appdata)
            },            
            appresp:function(appresp=null){
                let error = false
                let stacktrace = false
                //var has_errors = false                                            
                if (appresp != null){
                    //
                    if (appresp.errors.length > 0){
                        //has_errors = true
                        this.errors = appresp.errors                        
                        error = true
                    }
                    if (appresp.stacktrace != null && appresp.stacktrace.length > 0){
                        this.stacktrace = appresp.stacktrace
                        stacktrace = true
                    }
                    
                    //mostrar el dialogo si hay error
                    if (error == true || stacktrace==true){
                        this.mostrar_info_error = true
                        this.msgdata = this.error
                        this.title = "Error"
                    }else{
                        this.mostrar_info_error = false
                        this.msgdata = this.info
                        this.title = "Información"
                    }                                                        
                    this.message = appresp.message                                        
                }
            },
            onOk(){
                if (this.action != ""){
                    this.$emit(this.action)
                }                
            }
        }
    }
</script>
