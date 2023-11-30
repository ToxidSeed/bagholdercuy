<template>
    <q-dialog v-model="open">                
        <q-card style="width:600px;">
            <q-toolbar>
                <q-toolbar-title class="text-blue-10">{{ WinGestorAlertaStore.state.title }}</q-toolbar-title>
            </q-toolbar>
            <q-separator/>                                    
            <q-card-section class="q-pt-none">                                 
                <!--opciones-->                                        
                <div>                                            
                    <SelectSymbol v-if="WinGestorAlertaStore.state.configuracion_alerta.id_config_alerta == '' && WinGestorAlertaStore.state.configuracion_alerta.id_monitoreo == ''" label="Subyacente" v-on:select-symbol="select_symbol"/>
                    <div class="row">
                        <div>
                            <div class="text-blue-10 q-pt-xs">
                                {{ WinGestorAlertaStore.state.symbol.cod_symbol }}
                            </div>
                            <div>
                                {{ WinGestorAlertaStore.state.symbol.nom_symbol }}
                            </div>
                        </div>
                        <div class="q-pl-xs q-pt-xs" v-if="btn_remover_sel_symbol_oculto==true">
                            <q-btn flat icon="close" color="red" round dense/>
                        </div>
                    </div>
                    <!--
                    <q-checkbox v-model="flg_compras" label="Compras" color="blue-10"/>
                    <q-checkbox v-model="flg_ventas" label="Ventas" color="blue-10"/>
                    -->
                    <div>                        
                        <div class="row">
                            <div class="col-4 q-pr-md">
                                <q-input input-style="text-align: right" color="blue-10" label="Cantidad de la variacion" stack-label v-model="WinGestorAlertaStore.state.configuracion_alerta.ctd_variacion_imp_accion" ></q-input>
                            </div>
                            <div class="q-pt-xs">
                                <span class="text-blue-10 text-bold">Expresados en: </span>
                                <q-radio v-model="WinGestorAlertaStore.state.configuracion_alerta.cod_tipo_variacion_imp_accion" :val="TIPO_VARIACION_TITULO.COD_IMPORTE" label="Importe" color="blue-10"/>
                                <q-radio v-model="WinGestorAlertaStore.state.configuracion_alerta.cod_tipo_variacion_imp_accion" :val="TIPO_VARIACION_TITULO.COD_PORCENTAJE" label="% porcentaje" color="blue-10"/>
                            </div>                            
                        </div>                        
                    </div>
                    <div class="row">
                        <div class="col-3  q-pr-md">
                            <q-input input-style="text-align: right" stack-label label="Cantidad de ciclos" color="blue-10" v-model="WinGestorAlertaStore.state.configuracion_alerta.ctd_ciclos"></q-input>                                                            
                        </div>
                        <div class="col-3  q-pr-md">
                            <q-input input-style="text-align: right" stack-label label="Iniciando en:" color="blue-10" v-model="WinGestorAlertaStore.state.configuracion_alerta.imp_inicial_ciclos"></q-input>
                        </div>
                    </div>                         
                </div>                                                          
            </q-card-section>        
            <q-separator/>
            <q-card-actions align="right">
                <q-btn icon="engineering" class="text-capitalize" label="Avanzado" flat color="blue-10"/>                                
                <!--
                    <q-btn icon="sync_alt" class="text-capitalize" label="Regenerar" flat color="blue-10"/>                    
                -->
                <q-btn icon="done" class="text-capitalize" flat label="Aceptar" color="green-10" @click="WinGestorAlertaStore.guardar()"></q-btn>
                <q-btn icon="delete" class="text-capitalize" flat label="Eliminar" color="red-10" ></q-btn>
                <q-btn label="Cerrar"  class="text-capitalize"  color="red-14" @click="WinGestorAlertaStore.cerrar()"></q-btn>
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>
<script>
import SelectSymbol from "@/components/SelectSymbol.vue"
import WinGestorAlertaStore from "./win-gestor-alerta-store"

import { 
    TIPO_VARIACION_TITULO, 
    TIPO_VARIACION_EJERCICIO
} from "@/common/app-constants.js"

export default {
    name:"WinGestionAlerta",    
    components:{
        SelectSymbol
    },
    created:function(){
        this.TIPO_VARIACION_EJERCICIO = TIPO_VARIACION_EJERCICIO,
        this.TIPO_VARIACION_TITULO = TIPO_VARIACION_TITULO
    },     
    props:{        
        value:{
                required:true
        }
    },
    computed:{
        btn_remover_sel_symbol_oculto: function(){
            if (this.WinGestorAlertaStore.state.estado == 'nuevo' && WinGestorAlertaStore.state.symbol.cod_symbol != ''){
                return true
            }else{
                return false
            }
        }
    },
    watch:{
        open:function(newval){
            this.$emit('input',newval)
        },  
        value:function(newval){           
            if (newval == false){
                this.WinGestorAlertaStore.cerrar()
            }
            this.open = newval
        }
    },
    data(){
        return {
            open:this.value,                
            WinGestorAlertaStore:WinGestorAlertaStore
        }
    },
    methods:{                
        select_symbol:function(item){
            this.WinGestorAlertaStore.state.configuracion_alerta.id_symbol = item.id_symbol

            this.WinGestorAlertaStore.set_symbol({
                id:item.id_symbol,
                symbol: item.value,
                name: item.label
            })             
        }
    }
}
</script>