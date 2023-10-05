<template>
    <div>
        <q-toolbar>
            <q-toolbar-title class="text-blue-10">Usuario</q-toolbar-title>
        </q-toolbar>
        <div class="row q-col-gutter-xs">
            <div class="col-4" v-if="lpanel_visible==true">
                <router-view
                    v-on:reload-usuarios="get_usuarios"
                />
            </div>
            <div class="col">
                <q-toolbar>
                    <q-btn label="Nuevo" color="blue-10" class="text-capitalize" icon="add" :to="{name:'usuario-nuevo'}"/>
                </q-toolbar>
                <TableListaUsuario ref="TableListaUsuario"/>            
            </div>
        </div>
    </div>
</template>
<script>
import TableListaUsuario from '@/components/usuario/TableListaUsuario.vue'
export default {
    name:"MainUsuario",
    components:{
        TableListaUsuario
    },
    props:{
        action:{
            type:String,
            default:""
        }
    },
    data (){
        return {
            lpanel_visible:false
        }
    },
    watch:{
        $route: function(){
            this.habilitar()
        }
    },
    mounted:function(){
        this.habilitar()                
    },
    methods:{
        habilitar:function(){
            if (this.$route.name == "usuario"){
                this.lpanel_visible = false
            }
            if (this.$route.name == "usuario-nuevo"){
                this.lpanel_visible = true
            }
            if (this.$route.name == "usuario-ver"){
                this.lpanel_visible = true
            }
            if (this.$route.name == "usuario-config"){
                this.lpanel_visible = true
            }
        },
        get_usuarios:function(){            
            this.$refs.TableListaUsuario.get_usuarios()
        }
    }    
}
</script>