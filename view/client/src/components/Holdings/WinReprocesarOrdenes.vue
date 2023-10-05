<template>
    <div>
        <q-dialog v-model="open">
            <q-card style="width:400px;">
                <q-toolbar>
                    <q-toolbar-title class="text-blue-10">Reprocesar</q-toolbar-title>                    
                </q-toolbar>
                <q-separator/>
                <q-card-section class="q-pb-none">
                    <q-checkbox v-model="flg_reprocesar_todo" label="Reprocesar todo"/>
                </q-card-section>
                <div v-if="flg_reprocesar_todo==false">
                    <q-card-section class="q-pb-xs">
                        <div class="q-gutter-sm">
                            <q-radio v-model="flg_opcion" label="symbols" :val="false"></q-radio>
                            <q-radio v-model="flg_opcion" label="opciones" :val="true" ></q-radio>
                        </div>
                    </q-card-section>
                    <q-card-section class="q-pt-xs" v-if="flg_opcion==false">
                        <SelectSymbol v-on:select-symbol="sel_symbol"/>
                        <div class="q-pt-xs">
                            <div class="text-blue-10 text-h6">{{ cod_symbol }}</div>
                            <div>{{ des_symbol }}</div>
                        </div>
                    </q-card-section>
                    <q-card-section class="q-pt-xs" v-if="flg_opcion==true">
                        <q-input v-model="cod_opcion" label="Codigo de opcion" stack-label/>                    
                    </q-card-section>                    
                </div>
                <q-separator/>
                <q-card-actions align="right">
                    <q-btn label="Aceptar" color="blue-10" @click="reprocesar"/>
                    <q-btn label="Cancelar" color="red-10" @click="open=false"/>
                </q-card-actions>
                <q-inner-loading :showing="progress">
                    <q-spinner-gears size="50px" color="primary" />
                </q-inner-loading>
            </q-card>
        </q-dialog>
        <MessageBox :config="MsgBox"/>
    </div>
</template>
<script>
import SelectSymbol from "@/components/SelectSymbol.vue";
import MessageBox from '@/components/MessageBox.vue';
import {get_postconfig} from "@/common/request.js"
export default {
    name:"WinReprocesarOrdenes",
    props:{
        value:{
            required:true
        }
    },
    components:{
        SelectSymbol,
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
            open: this.value,
            flg_opcion: false,
            cod_opcion:"",
            cod_symbol:"",
            des_symbol:"",
            MsgBox:{},
            progress:false,
            flg_reprocesar_todo: true
        }
    },
    methods:{
        reprocesar:function(){
            let postconfig = get_postconfig()
            this.progress = true

            this.$http.post(
                '/OrdenManager/ReprocesadorManager/ejecutar',{
                    flg_reprocesar_todo: this.flg_reprocesar_todo,
                    flg_opcion:this.flg_opcion,
                    cod_symbol: this.cod_symbol,
                    cod_opcion: this.cod_opcion
                },
                postconfig
            ).then(httpresp => {
                this.MsgBox = {
                    httpresp : httpresp
                }
            }).finally(() => {
                this.progress = false
            })
        },
        sel_symbol:function(item){
            this.cod_symbol = item.value
            this.des_symbol = item.label
        }
    }
}
</script>