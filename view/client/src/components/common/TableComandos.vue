<template>
    <q-toolbar class="q-pa-none p-ma-none" id="toolbar">
        <q-btn v-if="ver==true" icon="visibility" dense flat color="blue-10" @click="btn_ver_click"/>
        <q-btn v-if="editar==true" icon="edit" dense flat color="blue-10" @click="btn_editar_click"/>
        <q-btn v-if="configurar==true" icon="settings" dense flat color="blue-10" @click="btn_configurar_click"/>
        <q-btn v-if="eliminar==true" icon="delete" dense flat color="red-10"/>
    </q-toolbar>
</template>
<script>
export default {
    name:"TableComandos",
    props:{
        editar:{
            type: Boolean,
            default: false
        },
        configurar:{
            type: Boolean,
            default: false
        },
        ver:{
            type: Boolean,
            default: false
        },
        eliminar:{
            type: Boolean,
            default: false
        }
    },
    data (){
        return {
            
        }
    },
    methods:{
        btn_ver_click:function(){            
            this.$emit("btn-ver-click")
        },
        btn_editar_click:function(){
            this.$emit("btn-editar-click")
        },
        btn_configurar_click:function(){
            this.$emit("btn-configurar-click")
        }
    }
}
</script>
<style scoped>
.q-toolbar {
    min-height: auto;
}
</style>