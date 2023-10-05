<template>
    <div>
        <q-toolbar>
            <q-toolbar-title class="text-blue-10 text-bold">Cuenta</q-toolbar-title>
        </q-toolbar>
        <div class="row q-col-gutter-xs">
            <div class="col-4" v-if="lpanel_visible==true">
                <router-view
                    v-on:reload-cuentas="get_cuentas"
                />
            </div>
            <div class="col">
                <q-toolbar>
                    <q-btn label="Nuevo" color="blue-10" class="text-capitalize" icon="add" :to="{name:'cuenta-nuevo'}"/>
                </q-toolbar>
                <TableListaCuentas ref="TableListaCuentas"/>            
            </div>
        </div>
    </div>
</template>
<script>
import TableListaCuentas from "@/components/cuenta/TableListCuentas.vue"

export default {
    name:"MainCuenta",
    components:{
        TableListaCuentas
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
            if (this.$route.name == "cuenta"){
                this.lpanel_visible = false
            }
            if (this.$route.name == "cuenta-nuevo"){
                this.lpanel_visible = true
            }
            if (this.$route.name == "cuenta-ver"){
                this.lpanel_visible = true
            }
            if (this.$route.name == "cuenta-editar"){
                this.lpanel_visible = true
            }
        },
        get_cuentas:function(){
            this.$refs.TableListaCuentas.get_cuentas()
        }
    }
}
</script>