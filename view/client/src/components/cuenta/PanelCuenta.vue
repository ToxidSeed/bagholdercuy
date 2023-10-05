<template>
    <div>                
        <q-card>
            <q-toolbar>
                <q-toolbar-title class="text-blue-10">
                    {{ config.title }}
                </q-toolbar-title>
                <q-btn icon="close" color="red" flat :to="{name:'cuenta'}"/>
            </q-toolbar>
            <q-separator/>
            <q-toolbar>
                <q-btn label="Guardar" icon="save" dense flat class="text-capitalize text-blue-10" @click="btn_guardar_click" :disable="config.lectura==true"/>
                <q-btn label="Editar" icon="edit" dense flat class="text-capitalize text-blue-10" :to="{name:'cuenta-editar', params:{id_cuenta:id_cuenta}}" :disable="config.lectura==false"/>
            </q-toolbar>
            <q-card-section class="q-col-gutter-xs row">
                <div class="col-3">
                    <q-input label="ID" stack-label color="blue-10" readonly v-model="id_cuenta"/>
                </div>
                <div class="col-9">
                    <q-input label="Codigo" stack-label color="blue-10" v-model="codigo" :readonly="config.lectura==true"/>
                </div>
                <div class="col-12">
                    <q-input label="Nombre" stack-label color="blue-10" v-model="nombre" :readonly="config.lectura==true"/>
                </div>                        
                <div>
                    <SelectBroker v-on:select="select_broker"/>
                </div>                
                <q-checkbox v-model="flg_activo" label="Activo" color="blue-10" :true-value="1" :false-value="0" :disable="config.lectura==true"/>
                <div v-if="usuario.usuario_id!=''" class="col-12 q-pt-md">
                    <span>Usuario: </span><span class="text-bold text-blue-10">{{ usuario.id_usuario }} - {{ usuario.nombre }}</span>
                </div>
            </q-card-section>
        </q-card>           
        <Confirmar v-model="confirmar.visible" :config="confirmar" v-on:ok="confirmar.callback"/>          
        <MessageBox ref="msgbox"/>   
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue';
import Confirmar from "@/components/dialogs/Confirmar.vue";
import SelectBroker from "@/components/broker/SelectBroker.vue";
import {postconfig} from '@/common/request.js';

export default {
    name:"PanelCuenta",
    components:{
        MessageBox,
        Confirmar,
        SelectBroker
    },
    props:{
        id_cuenta:{
            type:String,
            default:""
        }
    },
    data(){
        return {     
            codigo:"",
            nombre:"",
            id_broker:"",
            flg_activo:"",                    
            usuario:{
                id_usuario:"",
                nombre:""
            },
            config:{
                title:"",
                lectura:false,
                nuevo:false,
                editar:false
            },
            confirmar:{
                visible:false,
                title:"",
                msg:"",
                callback:() => {}
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
            //console.log(localStorage)            
            this.usuario.id_usuario = localStorage.getItem("id_usuario")
            this.usuario.nombre = localStorage.getItem("usuario")            
        },        
        set_config:function(route_name){
            if (route_name == "cuenta-nuevo"){
                this.nuevo()
                return
            }
            if (route_name == "cuenta-ver"){
                this.ver()
                return
            }
            if (route_name == "cuenta-editar"){
                this.editar()
                return
            }
        },
        btn_guardar_click:function(){
            this.confirmar.visible = true
            this.confirmar.title = "Confirmar"
            this.confirmar.msg = "Desea guardar la cuenta "+this.nombre+"?"
            this.confirmar.callback = () => this.guardar()
        },
        guardar:function(){
            if (this.id_cuenta == ""){
                this.registrar()
            }else{
                this.actualizar()
            }
        },
        nuevo:function(){
            //
            this.config.title = "Nuevo registro de una cuenta"
            this.config.lectura = false
            this.config.nuevo = true
            this.config.editar = false
            //     
            this.nombre = ""
            this.flg_activo = 1
        },
        ver:function(){
            //
            this.config.title = "Detalles de la cuenta"
            this.config.lectura = true
            this.config.nuevo = false
            this.config.editar = false
            //
            this.get_cuenta()
        },
        editar:function(){
            //
            this.config.title = "Modificar datos de la cuenta"
            this.config.lectura = false
            this.config.nuevo = false
            this.config.editar = true
            //
            this.get_broker()
        },
        registrar:function(){
            this.$http.post(
                '/cuenta/CuentaManager/registrar',{
                    id_cuenta:this.id_cuenta,
                    codigo: this.codigo,
                    nombre:this.nombre,
                    id_broker: this.id_broker,
                    flg_activo: this.flg_activo,
                    id_usuario: this.usuario.id_usuario
                },
                postconfig()
            ).then(httpresp => {
                this.$refs.msgbox.http_resp(httpresp)

                let appdata = httpresp.data
                if (appdata.success == true){                                        
                    this.nuevo()
                }
                this.$emit('reload-cuentas')
            })
        },
        actualizar:function(){

        },
        get_cuenta:function(){

        },
        select_broker:function(params){
            this.id_broker = params.value
        }
    }
}
</script>