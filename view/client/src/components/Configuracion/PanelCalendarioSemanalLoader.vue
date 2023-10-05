<template>
    <q-card class="q-pb-xs">
        <div class="row">
        <q-toolbar class="text-blue-10">
            <q-btn icon="call_to_action" flat>
            </q-btn>
            <q-toolbar-title>
                Calendario Semanal Loader
            </q-toolbar-title>
        </q-toolbar>        
        </div>
        <q-separator color=""/>
        <q-card-section>
            <q-btn color="green" icon="directions_run" @click="cargar">Ejecutar</q-btn>
        </q-card-section>     
        <MessageBox :config="msgbox"/>   
    </q-card>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue'
import {postconfig} from '@/common/request.js';

export default {
    name:"PanelCalendarioSemanalLoader",
    components:{
        MessageBox
    },
    data(){
        return {
            msgbox:{}
        }
    },
    methods:{
        cargar:function(){
            this.$http.post(
                '/CalendarioSemanalManager/CalendarioSemanalManager/load',{

                },
                postconfig()
            ).then(httpresp => {
                this.msgbox = {
                    httpresp:httpresp
                } 
            })
        }
    }
}
</script>