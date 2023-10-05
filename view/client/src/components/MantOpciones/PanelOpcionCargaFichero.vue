<template>
    <div>        
        <q-card>
            <q-toolbar>
                <q-toolbar-title class="text-h6 text-blue-10">
                # Carga de opciones desde Archivo .csv
                </q-toolbar-title>
            </q-toolbar>
            <q-separator/>
            <q-toolbar>
                <q-btn label="Procesar" color="green-8" @click="procesar"/>
            </q-toolbar>
            <q-card-section>
                <q-file
                    v-model="fichero"
                    label="Seleccionar fichero de opciones"
                    use-chips        
                    stack-label                
                >                
                    <template v-slot:prepend>
                    <q-icon name="attach_file" />
                    </template>
                </q-file>
                <div class="row">
                    <SelectMoneda class="col-7"
                    v-on:httperror="set_error"
                    v-on:moneda-select="sel_moneda"
                    :in_cod_moneda="'USD'"
                    />
                    <q-input class="col-5 q-pl-xs" label="Multiplicador" stack-label input-class="text-right" 
                    v-model="ctd_multiplicador"/>
                </div>
                <q-select label="Formato del symbol de la opcion" stack-label v-model="formato_cod_opcion" 
                :options="formatos_cod_opcion"/>
                <q-checkbox v-model="flg_excluir_errores" label="Excluir errores"/>
            </q-card-section>
            <q-inner-loading :showing="loading">
                <q-spinner-gears size="50px" color="primary" />
            </q-inner-loading>
        </q-card>
        <MessageBox :config="msgbox"/>
    </div>
</template>
<script>
import SelectMoneda from '@/components/SelectMoneda.vue'
import MessageBox from '@/components/MessageBox.vue';
import {get_postconfig} from '@/common/request.js'
export default {
    name:"PanelOpcionCargaFichero",
    components:{
        MessageBox,
        SelectMoneda
    },
    data(){
        return {
            fichero:null,
            formatos_cod_opcion:[
                {
                    value:1,
                    label:"Default"
                },{
                    value:2,
                    label:"Interactive Brokers"
                }
            ],
            formato_cod_opcion:{
                value:1,
                label:"Default"
            },
            ctd_multiplicador:100,
            msgbox:{},
            cod_moneda:"USD",
            loading:false,
            flg_excluir_errores:true  
        }
    },
    methods:{
        set_error:function(httpresp){
            this.msgbox = {
                httpresp: httpresp
            }
        },
        sel_moneda:function(moneda){
            this.cod_moneda = moneda.value
            console.log(this.cod_moneda)
        },
        procesar:function(){
            this.loading = true
            let postconfig = get_postconfig()
            postconfig.headers['Content-Type'] = "multipart/form-data"
            let form_data = new FormData();            

            form_data.append("fichero", this.fichero)
            form_data.append("cod_moneda", this.cod_moneda)
            form_data.append("formato_cod_opcion", this.formato_cod_opcion.value)
            form_data.append("ctd_multiplicador", this.ctd_multiplicador)
            form_data.append("flg_excluir_errores", this.flg_excluir_errores)

            console.log(postconfig)

            this.$http.post(
                '/OpcionesContrato/CsvLoader/procesar',form_data,postconfig                
            ).then(httpresp => {
                this.msgbox = {
                    httpresp: httpresp
                }
            }).finally(() => {
                this.loading = false
            })
        }
    }
}
</script>
