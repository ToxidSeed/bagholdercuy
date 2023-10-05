<template>
    <div>                
        <q-card>
            <q-toolbar>
                <q-toolbar-title class="text-blue-10">
                    {{ config.title }}
                </q-toolbar-title>
                <q-btn icon="close" color="red" flat :to="{name:'broker'}"/>
            </q-toolbar>
            <q-separator/>
            <q-toolbar>
                <q-btn label="Guardar" icon="save" dense flat class="text-capitalize text-blue-10" @click="btn_guardar_click" :disable="config.lectura==true"/>
                <q-btn label="Editar" icon="edit" dense flat class="text-capitalize text-blue-10" :to="{name:'broker-editar', params:{id_broker:id_broker}}" :disable="config.lectura==false"/>
            </q-toolbar>
            <q-card-section class="q-col-gutter-xs row">
                <div class="col-3">
                    <q-input label="ID" stack-label color="blue-10" readonly v-model="id_broker"/>
                </div>
                <div class="col-9">
                    <q-input label="Nombre" stack-label color="blue-10" v-model="nom_broker" :readonly="config.lectura==true"/>
                </div>
                <q-checkbox v-model="flg_activo" label="Activo" color="blue-10" :true-value="1" :false-value="0" :disable="config.lectura==true"/>
            </q-card-section>
        </q-card>           
        <Confirmar v-model="confirmar.visible" :config="confirmar" v-on:ok="confirmar.callback"/>          
        <MessageBox ref="msgbox"/>   
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue';
import Confirmar from "@/components/dialogs/Confirmar.vue";
import {postconfig} from '@/common/request.js';

export default {
    name:"PanelBroker",
    components:{
        Confirmar,
        MessageBox
    },
    props:{
        id_broker:{
            type:String,
            default:""
        }
    },
    data(){
        return {            
            nom_broker:"",
            flg_activo:1,
            confirmar:{
                visible:false,
                title:"",
                msg:"",
                callback:() => {}
            },            
            config:{
                title:"",
                lectura:false,
                nuevo:false,
                editar:false
            }            
        }
    },
    watch:{
        $route:function(newval){
            this.set_config(newval.name)
        }
    },
    mounted:function(){                
        this.init()
    },
    methods:{
        init:function(){            
            this.set_config(this.$route.name)
        },        
        set_config:function(route_name){
            if (route_name == "broker-new"){
                this.nuevo()
                return
            }
            if (route_name == "broker-ver"){
                this.ver()
                return
            }
            if (route_name == "broker-editar"){
                this.editar()
                return
            }
        },
        btn_guardar_click:function(){                   
            this.confirmar.visible = true
            this.confirmar.title = "Confirmar"
            this.confirmar.msg = "Desea guardar el broker "+this.nom_broker+"?"
            this.confirmar.callback = () => this.guardar()
        },
        nuevo:function(){       
            //
            this.config.title = "Nuevo registro de un broker"
            this.config.lectura = false
            this.config.nuevo = true
            this.config.editar = false
            //     
            this.nom_broker = ""
            this.flg_activo = 1
        },
        ver:function(){
            //
            this.config.title = "Visualizacion de datos del broker"
            this.config.lectura = true
            this.config.nuevo = false
            this.config.editar = false
            //
            this.get_broker()
        },
        get_broker:function(){
            this.$http.post(
                "/broker/BrokerManager/get_broker",{
                    id_broker: this.id_broker
                },
                postconfig()
            ).then(httpresp => {
                this.msgbox = {
                    httpresp: httpresp,
                    onerror: true
                }

                let appdata = httpresp.data.data
                this.nom_broker = appdata.nom_broker
                this.flg_activo = appdata.flg_activo
            })
        },
        editar:function(){
            //
            this.config.title = "Modificar datos del broker"
            this.config.lectura = false
            this.config.nuevo = false
            this.config.editar = true
            //
            this.get_broker()
        },
        guardar:function(){
            if (this.config.nuevo == true){
                this.registrar()
            }else{
                this.actualizar()
            }                        
        },
        registrar:function(){
            this.$http.post(
                "/broker/BrokerManager/registrar",{                    
                    nom_broker:this.nom_broker,
                    flg_activo: this.flg_activo
                },
                postconfig()
            ).then(httpresp => {
                this.$refs.msgbox.http_resp(httpresp)
                            
                let appdata = httpresp.data
                if (appdata.success == true){                                        
                    this.nuevo()
                }
                this.$emit('reload-brokers')
            })
        },
        actualizar:function(){
            console.log("actualizar")
            this.$http.post(
                "/broker/BrokerManager/actualizar",{
                    id_broker:this.id_broker,
                    nom_broker:this.nom_broker,
                    flg_activo: this.flg_activo
                },
                postconfig()
            ).then(httpresp => {                                
                this.$refs.msgbox.http_resp(httpresp)

                let appdata = httpresp.data
                if (appdata.success == true){                                        
                    this.editar()
                }
                this.$emit('reload-brokers')
            })
        }
    }
}
</script>