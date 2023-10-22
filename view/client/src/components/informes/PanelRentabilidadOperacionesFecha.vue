<template>
    <div class="row q-gutter-sm q-ml-sm">
        <q-card v-for="item in rentabilidades" v-bind:key="item.periodo" class="text-h6">
            <q-card-section class="q-pb-none q-pt-xs">
                {{ item.periodo }}
            </q-card-section>
            <q-separator/>
            <q-card-section class="text-h3 text-center">
                <span :class="item.imp_rentabilidad>0?'text-green':'text-red'">{{ item.imp_rentabilidad }}</span>
            </q-card-section>
        </q-card>
        <MessageBox :config="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue';
import {postconfig} from '@/common/request.js';

export default {
    name:"PanelRentabilidadOperacionesFecha",
    components:{
        MessageBox
    },
    data(){
        return {            
            rentabilidades:[],
            msgbox:{}
        }
    },
    mounted:function(){
        this.get_rentabilidades_x_periodo()
    },
    methods:{
        get_rentabilidades_x_periodo:function(){
            this.$http.post(
                '/operacion/OperacionManager/get_rentabilidades_x_periodo',{
                    id_cuenta:localStorage.getItem("id_cuenta")
                },
                postconfig()
            ).then(httpresp => {
                this.msgbox = {
                    httpresp:httpresp,
                    onerror:true
                }
                this.rentabilidades = httpresp.data.data
                console.log(this.data)
            })
        }
    }
}
</script>