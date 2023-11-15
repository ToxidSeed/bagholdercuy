<template>
    <q-dialog v-model="abierto">                
        <q-card style="width:500px;">
            <q-toolbar>
                <q-toolbar-title class="text-blue-10">Configuracion de alertas</q-toolbar-title>
            </q-toolbar>
            <q-separator/>
            <!--
            <q-card-section>
                <div class="q-gutter-sm">
                    <q-radio v-model="flg_opciones" :val="true" label="Opciones" color="blue-10"/>
                    <q-radio v-model="flg_opciones" :val="false" label="Stocks" color="blue-10"/>
                </div>
            </q-card-section>
            -->
            <q-separator/>
            <div v-if="flg_opciones==true">
                <q-card-section>                                 
                    <!--opciones-->                                        
                    <div>                    
                        <!--<div class="text-blue-10 text-bold">Opciones</div>-->
                        <SelectSymbol label="Subyacente" v-on:select-symbol="select_symbol"/>
                        <div class="row">
                            <div>
                                <div class="text-blue-10 q-pt-xs">
                                    {{ cod_symbol }}
                                </div>
                                <div>
                                    {{ nom_symbol }}
                                </div>
                            </div>
                            <div class="q-pl-xs q-pt-xs">
                                <q-btn flat icon="close" color="red" round dense v-if="cod_symbol != ''"/>
                            </div>
                        </div>
                        <!--
                        <q-checkbox v-model="flg_compras" label="Compras" color="blue-10"/>
                        <q-checkbox v-model="flg_ventas" label="Ventas" color="blue-10"/>
                        -->
                        <div>                        
                            <div class="row">
                                <div class="col-4 q-pr-md">
                                    <q-input input-style="text-align: right" color="blue-10" label="Cantidad de la variacion" stack-label v-model="ctd_variacion_titulo" ></q-input>
                                </div>
                                <div class="q-pt-xs">
                                    <span class="text-blue-10 text-bold">Expresados en: </span>
                                    <q-radio v-model="cod_tipo_variacion_titulo" :val="TIPO_VARIACION_TITULO.COD_IMPORTE" label="Importe" color="blue-10"/>
                                    <q-radio v-model="cod_tipo_variacion_titulo" :val="TIPO_VARIACION_TITULO.COD_PORCENTAJE" label="% porcentaje" color="blue-10"/>
                                </div>                            
                            </div>                        
                        </div>
                        <div class="row">
                            <div class="col-3  q-pr-md">
                                <q-input input-style="text-align: right" stack-label label="Cantidad de ciclos" color="blue-10" v-model="ctd_ciclos"></q-input>                                                            
                            </div>
                            <div class="col-3  q-pr-md">
                                <q-input input-style="text-align: right" stack-label label="Iniciando en:" color="blue-10" v-model="imp_inicio_ciclos"></q-input>                                                                                        
                            </div>
                        </div>                         
                    </div>                                                          
                </q-card-section>
                <q-card-section>
                    <div class="q-pa-none text-blue-10 text-bold">Datos de las opciones</div>
                    <div>
                        <q-radio v-model="cod_tipo_variacion_ejercicio" :val="TIPO_VARIACION_EJERCICIO.COD_FIJO" color="blue-10">Importe <span class="text-blue-10">Fijo</span></q-radio>
                        <q-radio v-model="cod_tipo_variacion_ejercicio" :val="TIPO_VARIACION_EJERCICIO.COD_VARIACION_SUBYACENTE" color="blue-10">Variacion del <span class="text-blue-10">subyacente</span></q-radio>
                    </div>
                    <div class="q-col-gutter-xs row" v-if="cod_tipo_variacion_ejercicio==TIPO_VARIACION_EJERCICIO.COD_FIJO">
                        <q-input label="Imp. Ejercicio (CALL)" stack-label input-style="text-align: right" color="blue-10" class="col-6" v-model="imp_fijo_ejercicio_call"></q-input>
                        <q-input label="Imp. Ejercicio (PUT)" stack-label input-style="text-align: right" color="blue-10" class="col-6" v-model="imp_fijo_ejercicio_put"></q-input>
                    </div>
                    <div class="q-col-gutter-xs row" v-if="cod_tipo_variacion_ejercicio==TIPO_VARIACION_EJERCICIO.COD_VARIACION_SUBYACENTE">
                        <q-input label="Imp. variacion subyacente (CALL)" stack-label input-style="text-align: right" color="blue-10" class="col-6" v-model="imp_variacion_subyacente_call"></q-input>
                        <q-input label="Imp. variacion subyacente (PUT)" stack-label input-style="text-align: right" color="blue-10" class="col-6" v-model="imp_variacion_subyacente_put"></q-input>
                    </div>
                    <div class="q-col-gutter-xs row">
                        <q-input label="Dias para expiracion (CALL)" stack-label input-style="text-align: right" color="blue-10" class="col-6" v-model="num_dias_expiracion_call"></q-input>
                        <q-input label="Dias para expiracion (PUT)" stack-label input-style="text-align: right" color="blue-10" class="col-6" v-model="num_dias_expiracion_put"></q-input>
                    </div>
                </q-card-section>
            </div>
            <q-separator/>
            <q-card-actions align="right">
                <q-btn label="Aceptar" color="blue-10" @click="btn_aceptar_click"></q-btn>
                <q-btn label="Cancelar" color="red-14" @click="abierto=false"></q-btn>
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>
<script>
import SelectSymbol from "@/components/SelectSymbol.vue"
import {postconfig} from "@/common/request.js"
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
        abierto:{
            get(){
                return this.$store.state.configuracion_alerta.win_gestor_alerta.abierto
            },
            set(){
                this.$store.commit('configuracion_alerta/CERRAR_GESTOR_ALERTA',null, {root:true})
            }
        },
        ctd_ciclos_param:{
            get(){
                return this.$store.state.configuracion_alerta.configuracion_alerta.ctd_ciclos
            }
        }
    },
    watch:{
        abierto:function(newval){            
            if (newval == true){                
                this.$nextTick(() => {
                    this.ctd_ciclos = this.ctd_ciclos_param             
                })             
            }            
        }
        /*open:function(newval){
            this.$emit('input',newval)
        },
        value:function(newval){
            this.open = newval
        }*/
    },
    data(){
        return {
            open:this.value,
            flg_opciones: true,
            flg_compras: true,
            flg_ventas: true,
            cod_tipo_variacion_titulo: TIPO_VARIACION_TITULO.COD_IMPORTE,
            cod_tipo_variacion_ejercicio: TIPO_VARIACION_EJERCICIO.COD_VARIACION_SUBYACENTE,
            ctd_variacion_titulo:"",
            ctd_ciclos:"",
            imp_inicio_ciclos:"",
            imp_fijo_ejercicio_call:null,
            imp_fijo_ejercicio_put:null,
            imp_variacion_subyacente_call:null,
            imp_variacion_subyacente_put:null,
            num_dias_expiracion_call:null,
            num_dias_expiracion_put:null,
            cod_symbol:"",
            nom_symbol:""
        }
    },
    methods:{        
        btn_aceptar_click:function(){                        
            this.registrar()
            //this.open = false
        },
        select_symbol:function(item){
            this.cod_symbol = item.value
            this.nom_symbol = item.label
        },
        registrar:function(){
            this.$http.post(
                "/configuracionalerta/ConfiguracionAlertaController/registrar",
                {
                    flg_compras: this.flg_compras,
                    flg_ventas: this.flg_ventas,
                    cod_symbol: this.cod_symbol,
                    id_cuenta: localStorage.getItem("id_cuenta"),
                    cod_tipo_variacion_titulo: this.cod_tipo_variacion_titulo,
                    ctd_variacion_titulo: this.ctd_variacion_titulo,
                    ctd_ciclos : this.ctd_ciclos,
                    imp_inicio_ciclos: this.imp_inicio_ciclos,
                    cod_tipo_variacion_ejercicio: this.cod_tipo_variacion_ejercicio,
                    imp_fijo_ejercicio_call: this.imp_fijo_ejercicio_call,
                    imp_fijo_ejercicio_put: this.imp_fijo_ejercicio_put,
                    imp_variacion_subyacente_call: this.imp_variacion_subyacente_call,
                    imp_variacion_subyacente_put: this.imp_variacion_subyacente_put,
                    num_dias_expiracion_call: this.num_dias_expiracion_call,
                    num_dias_expiracion_put: this.num_dias_expiracion_put
                },
                postconfig()
            ).then(httpresp => {
                this.$store.commit("message", {"httpresp":httpresp})
                console.log(httpresp)
            })
        }
    },
    mounted:function(){
        
    }
}
</script>