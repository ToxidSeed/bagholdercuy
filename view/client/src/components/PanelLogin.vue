<template>
    <div>
        <q-card class="absolute-center" >
            <q-card-section>
                <q-img
                src="/bagholder_full_logo_300px.png"
                style="width: 100%"
                >          
                </q-img>
            </q-card-section>
            <q-card-section  class="q-gutter-md">
                <q-input outlined bg-color="" color="primary" label="Usuario" dense v-model="usuario"/>                
                <q-input outlined bg-color="" label="Password" dense type="password" v-model="password"/>                
                <div class="row">
                    <q-btn label="Login" no-caps color="blue-9 " class="col-12" @click="login"/>
                </div>
            </q-card-section>
        </q-card>
    </div>
</template>
<script>
import store from '../store/store.js'

export default {
    name:"PanelLogin",
    data: () => {
        return {
            usuario:"",
            password:""
        }
    },
    methods:{
        login: async function(){
            try{
                const loginResp = await this.$http.post(
                    '/auth/LoginController/login',{
                        usuario:this.usuario,
                        password:this.password
                    }
                )

                const loginData = loginResp.data

                if (loginData.success == true){
                    this.set_auth_data(loginData.data)
                    await store.dispatch('serverConstants/getList')
                    this.$router.push({name:"main"})                    
                }
            } catch(error){
                console.log(error)
            }        
        },
        set_auth_data:function(appdata){         
            localStorage.setItem("id_usuario", appdata.id_usuario)   
            localStorage.setItem("usuario", appdata.usuario)
            localStorage.setItem("logeado",true)
            localStorage.setItem("token", appdata.token)                                    
            localStorage.setItem("id_cuenta",appdata.id_cuenta_default)
            localStorage.setItem("cod_cuenta",appdata.cod_cuenta)
            localStorage.setItem("nom_cuenta",appdata.nom_cuenta)
        }
    }
}
</script>