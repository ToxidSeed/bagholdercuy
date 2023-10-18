<template>
    <div>
        <q-dialog v-model="open">
            <q-card style="width:400px;">
                <q-toolbar>
                    <q-toolbar-title class="text-blue-10">Carga Multiple</q-toolbar-title>
                </q-toolbar>
                <q-separator/>
                <q-card-section>
                    <q-file
                        v-model="fichero"
                        label="Seleccionar fichero"
                        use-chips                
                        color="blue-10"        
                    >                
                        <template v-slot:prepend>
                        <q-icon name="attach_file" />
                        </template>
                    </q-file>
                    <q-checkbox v-model="flg_procesar_ordenes" color="blue-10" label="Procesar ordenes"></q-checkbox>
                </q-card-section>
                <q-separator/>
                <q-card-actions align="right">
                    <q-btn label="Aceptar" color="blue-10" @click="ejecutar_carga_multiple"></q-btn>
                    <q-btn label="Cancelar" color="red-10" @click="open=false"></q-btn>
                </q-card-actions>
                <q-inner-loading :showing="loading">
                    <q-spinner-gears size="50px" color="primary" />
                </q-inner-loading>     
            </q-card>
        </q-dialog>
        <MessageBox :config="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue';
import {get_postconfig} from '@/common/request.js';
export default {
    name:"WinCargaMultiple",
    props:{
        value:{
            required:true
        }
    },
    components:{
        MessageBox
    },
    watch:{
        open:function(newval){
            this.$emit('input',newval)
        },  
        value:function(newval){
            this.open = newval
        }
    },
    data(){
        return {
            fichero:null,
            open: this.value,
            msgbox:{},
            flg_procesar_ordenes:true,
            loading:false
        }
    },
    methods:{
        ejecutar_carga_multiple:function(){
            this.loading = true
            let postconfig = get_postconfig()
            let form_data = new FormData();

            form_data.append("fichero", this.fichero)
            form_data.append("flg_procesar_ordenes", this.flg_procesar_ordenes)
            form_data.append("id_cuenta", localStorage.getItem("id_cuenta"))
            this.$http.post(
                '/orden/CargadorMultipleManager/ejecutar',form_data,postconfig
            ).then(httpresp => {
                this.msgbox = {
                    httpresp:httpresp
                }
            }).finally(() => {
                this.loading = false
            })
        }
    }
}
</script>