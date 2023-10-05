<template>
    <div>                
        <q-card>
            <q-toolbar>
                <q-toolbar-title class="text-blue-10">
                    {{ config.title }}
                </q-toolbar-title>
                <q-btn icon="close" color="red" flat :to="{name:'usuario'}"/>
            </q-toolbar>
            <q-separator/>
            <q-toolbar>
                <q-btn label="Nuevo" icon="add" dense flat class="text-capitalize text-blue-10" @click="nuevo"/>
                <q-btn label="Guardar" icon="save" dense flat class="text-capitalize text-blue-10" @click="btn_guardar_click" :disable="config.lectura==true"/>
                <q-btn label="Configurar" icon="settings" dense flat class="text-capitalize text-blue-10" :to="{name:'usuario-config', params:{id_usuario:id_usuario}}" :disable="config.lectura==false"/>
            </q-toolbar>
            <q-card-section class="q-col-gutter-xs row">                
                <div class="col-3">
                    <q-input label="ID" stack-label color="blue-10" readonly v-model="id_usuario"/>
                </div>
                <div class="col-9">
                    <q-input label="Codigo" stack-label color="blue-10" v-model="codigo" ref="codigo"
                    :rules="[
                        val => !!val || '* Requerido'
                    ]"
                    />
                </div>
                <div class="col-6">
                    <q-input label="Nombres" stack-label color="blue-10" v-model="nombres" ref="nombres"
                    :readonly="config.lectura==true" autocomplete="off"
                    :rules="[
                        val => !!val || '* Requerido'
                    ]"
                    />
                </div>
                <div class="col-6">
                    <q-input label="Apellidos" stack-label color="blue-10" v-model="apellidos" ref="apellidos"
                    :readonly="config.lectura==true" autocomplete="off"
                    :rules="[
                        val => !!val || '* Requerido'
                    ]"
                    />
                </div>
                <div class="col-6" v-if="config.nuevo">
                    <q-input label="Password" autocomplete="new-password" :type="passinputtype" ref="password"
                    stack-label color="blue-10" v-model="password" :readonly="config.lectura==true" 
                    :rules="[
                        val => !!val || '* Requerido', confirmar_password
                    ]"
                    />
                </div>
                <div class="col-6" v-if="config.nuevo">
                    <q-input label="Confirmar password" autocomplete="new-password" :type="passinputtype" ref="re_password"  
                    stack-label color="blue-10" v-model="re_password" :readonly="config.lectura==true"
                    :rules="[
                        val => !!val || '* Requerido', confirmar_password
                    ]"
                    />
                </div>         
                <div>
                    <SelectCuenta :id_usuario="id_usuario"/>
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
import SelectCuenta from "@/components/cuenta/SelectCuenta.vue"
import Confirmar from "@/components/dialogs/Confirmar.vue";
import {postconfig} from '@/common/request.js';

export default {
    name:"PanelBroker",
    components:{
        Confirmar,
        MessageBox,
        SelectCuenta
    },
    props:{
        id_usuario:{
            type:String,
            default:""
        }
    },
    data(){
        return {            
            codigo:"",
            nombres:"",
            apellidos:"",
            password:"",
            re_password:"",
            id_cuenta_default:"",
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
            },
            passinputtype:"text"            
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
            this.passinputtype = "password"
            this.set_config(this.$route.name)
        },        
        set_config:function(route_name){            
            if (route_name == "usuario-nuevo"){                
                this.nuevo()                
                return
            }
            if (route_name == "usuario-ver"){
                this.ver()
                return
            }
            if (route_name == "usuario-config"){
                this.configurar()
                return
            }
        },
        btn_guardar_click:function(){                   
            this.confirmar.visible = true
            this.confirmar.title = "Confirmar"
            this.confirmar.msg = "Desea guardar el usuario "+this.codigo+"?"
            this.confirmar.callback = () => this.guardar()
        },
        nuevo:function(){       
            //
            this.config.title = "Nuevo registro de un usuario"
            this.config.lectura = false
            this.config.nuevo = true
            this.config.editar = false

            //     

            this.codigo = ""
            this.nombres = ""    
            this.apellidos = ""
            this.password = ""
            this.re_password = ""
            this.id_cuenta_default = ""        
            this.flg_activo = 1
                        
            //
            this.$nextTick(() => {
                this.reset_nuevo()
            })                        
        },
        reset_nuevo:function(){
            this.$refs.codigo.resetValidation()
            this.$refs.nombres.resetValidation()
            this.$refs.apellidos.resetValidation()
            this.$refs.password.resetValidation()
            this.$refs.re_password.resetValidation()            
        },
        ver:function(){
            //
            this.config.title = "Visualizacion de datos del usuario"
            this.config.lectura = true
            this.config.nuevo = false
            this.config.editar = false
            //
            this.get_usuario()
        },
        get_usuario:function(){
            this.$http.post(
                "/usuario/UsuarioManager/get_usuario",{
                    id_usuario: this.id_usuario
                },
                postconfig()
            ).then(httpresp => {                
                this.$refs.msgbox.http_resp_on_error(httpresp)

                let appdata = httpresp.data.data
                //this.id_usuario = appdata.id
                this.codigo = appdata.usuario
                this.nombres = appdata.nombres
                this.apellidos= appdata.apellidos
                this.id_cuenta_default = appdata.id_cuenta_default                
            })            
        },
        configurar:function(){
            //            
            this.config.title = "Configurar usuario"
            this.config.lectura = false
            this.config.nuevo = false
            this.config.editar = true
            //
            

            this.get_usuario()
        },
        guardar:function(){
            if (this.config.nuevo == true){
                this.registrar()
            }else{
                this.actualizar()
            }                        
        },
        confirmar_password:function(){
            if (this.password != "" && this.re_password != "" && this.password != this.re_password){
                return "Los passwords no coinciden"
            }
        },
        registrar:function(){            
            this.$refs.codigo.validate()
            this.$refs.nombres.validate()
            this.$refs.apellidos.validate()
            this.$refs.password.validate()
            this.$refs.re_password.validate()

            if (this.error_registrar()){
                return;
            }

            this.$http.post(
                "/usuario/UsuarioManager/registrar",{      
                    id_usuario:"",              
                    codigo:this.codigo,
                    nombres:this.nombres,
                    apellidos:this.apellidos,                    
                    password:this.password,                                        
                    flg_activo: this.flg_activo,
                    id_cuenta_default: this.id_cuenta_default
                },
                postconfig()
            ).then(httpresp => {
                this.$refs.msgbox.http_resp(httpresp)                            
                let appdata = httpresp.data
                if (appdata.success == true){                                        
                    this.nuevo()
                    this.$refs.codigo.resetValidation()
                }                
                this.$emit('reload-usuarios')
            })
        },
        error_registrar:function(){
            let error = false

            error = this.$refs.codigo.hasError
            error = this.$refs.nombres.hasError || error
            error = this.$refs.apellidos.hasError || error
            error = this.$refs.password.hasError || error
            error = this.$refs.re_password.hasError || error
            
            if (error){
                this.$refs.msgbox.open({
                    title:"Informacion",
                    message:"Se han encontrado errores al registrar, por favor revisar",
                    type:"error"
                })
                return error
            }
        },
        actualizar:function(){            
            this.$http.post(
                "/usuario/UsuarioManager/registrar",{                    
                    id_usuario:this.id_usuario,
                    nom_usuario:this.nom_usuario,
                    flg_activo: this.flg_activo
                },
                postconfig()
            ).then(httpresp => {                                
                this.$refs.msgbox.http_resp(httpresp)

                let appdata = httpresp.data
                if (appdata.success == true){                                        
                    this.editar()
                }
                this.$emit('reload-usuarios')
            })
        }
    }
}
</script>