<template>
    <q-card class="q-pb-xs">
        <div class="row">
            <q-toolbar class="text-blue-10">
                <q-toolbar-title>
                    Calendario Diario Loader
                </q-toolbar-title>
            </q-toolbar>
        </div>
        <q-separator/>
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
    name:"PanelCalendarioDiarioLoader",
    components:{
        MessageBox
    },
    data(){
        return {
            msgbox: {}
        }
    },
    methods:{
        cargar:function(){
            this.$http.post(
                '/calendariodiario/CalendarioDiarioLoader/procesar',{

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