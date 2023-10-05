<template>
    <div>
        <q-card>                        
            <q-toolbar>                
                <q-toolbar-title class="text-h6 text-blue-10">
                    # Nuevo Contrato
                </q-toolbar-title>
                <q-btn flat round dense icon="close" to="/opciones" color="red"/>
            </q-toolbar>            
            <q-separator/>
            <q-toolbar>                                                             
                <q-btn label="Guardar" color="green-10" @click="btn_guardar_click"/>
                <q-space />                
            </q-toolbar>
            <q-card-section>
                <div class="row">
                    <q-input class="col-3"
                        label="ID"
                        readonly
                        stack-label
                        v-model="opcion_id"
                    />
                    <q-input class="col-9 q-pl-xs" stack-label label="Symbol" v-model="cod_symbol" @change="change_cod_symbol"                 
                    />
                </div>
                <div class="row">
                    <q-select class="col-3" stack-label label="Side" v-model="side" :options="lista_sides" 
                    @input="build_cod_symbol"/>
                    <div class="col-9 q-pl-xs">
                        <SelectSymbol label="Seleccionar Subyacente"
                        v-on:select-symbol="sel_subyacente"
                        />                        
                    </div>                    
                </div>
                <div class="text-h6 text-blue-10">{{cod_subyacente}}</div>
                <div>{{nom_subyacente}}</div>                
                <div class="row">
                    <q-input stack-label label="Fch. exp" v-model="fch_exp" @change="build_cod_symbol"
                    mask="##/##/####"
                    class="col-3"
                    hint="dd/mm/yyyy"                                     
                    />
                    <q-input stack-label label="Strike" v-model="strike" @change="build_cod_symbol"
                    class="col-2 q-pl-xs"                    
                    input-class="text-right"
                    />
                    <q-input stack-label label="Tamaño" v-model="ctd_tamano_contrato"
                    class="col-2 q-pl-xs"
                    input-class="text-right"
                    />                
                    <div class="col-5 q-pl-xs">
                        <SelectMoneda 
                            v-on:moneda-select="sel_moneda"
                        />      
                        <div class="text-h7 q-pt-xs text-blue-10 text-bold">{{cod_moneda}}</div>
                        <div>{{ nom_moneda }}</div>
                    </div>                    
                </div>                       
            </q-card-section>            
        </q-card>
        <MessageBox :config="msgbox"/>
    </div>
</template>
<script>
import SelectSymbol from '@/components/SelectSymbol.vue'
import SelectMoneda from '@/components/SelectMoneda.vue'
import date from "date-and-time"
import {postconfig} from "@/common/request.js"
import MessageBox from "@/components/MessageBox.vue"

export default {
    name:"PanelMantOpciones",
    components:{
        SelectSymbol,
        SelectMoneda,
        MessageBox
    },
    props:{
        action:{
            type:String,
            default:""
        },
        test:{
            type:String,
            default:""
        },
        in_datos_opcion:{
            type:Object,
            default: () => {}
        }
    },
    data: () => {
        return {
            title:"",            
            opcion_id:"",
            symbol:"",
            cod_symbol:"",
            cod_subyacente:"",
            nom_subyacente:"",
            fch_exp:"",
            strike:"",
            side:"",
            ctd_tamano_contrato:100,
            lista_sides:[
                "call",
                "put"
            ],
            cod_moneda:"",
            nom_moneda:"",
            msgbox:{}
        }
    },
    mounted:function(){        
        
        if (this.in_datos_opcion != undefined && Object.keys(this.in_datos_opcion).length > 0){
            
            this.cod_subyacente = this.in_datos_opcion.subyacente
            this.fch_exp = this.in_datos_opcion.fch_expiracion
            this.side = this.in_datos_opcion.lado
            this.strike = this.in_datos_opcion.strike
            this.cod_moneda = this.in_datos_opcion.moneda_id
            //this.ctd_tamano_contrato = this.in_datos_opcion.ctd_tamano_contrato
        }

        //
        this.reset(this.action)
    },
    watch:{
        action:function(newval){
            this.reset(newval)
        },
        in_datos_opcion:function(newval){            
            this.cod_subyacente = newval.subyacente
            this.fch_exp = newval.fch_expiracion
            this.side = newval.lado
            this.strike = newval.strike
            this.cod_moneda = newval.moneda_id
        }
    },
    computed:{
        cod_symbol_calc:function(){
            let fch_exp = "" 
            if (this.fch_exp != ""){
                fch_exp = date.transform(this.fch_exp, "DD/MM/YYYY","YYYYMMDD")
            }            

            let cod_subyacente = ""
            if (this.cod_subyacente != ""){
                cod_subyacente = this.cod_subyacente
            }
            
            let sentido = ""
            if (this.side == "call"){
                sentido = "C"
            }
            if (this.side == "put"){
                sentido = "P"
            }

            let strike = ""
            if (this.strike != ""){
                strike = (this.strike*1000).toString().padStart(8,'0')
            }

            let cod_symbol = cod_subyacente+fch_exp+sentido+strike
                                
            return cod_symbol
        }
    },
    methods:{
        btn_guardar_click:function(){
            this.$http.post(
                '/OpcionesContrato/OpcionesContratoManager/guardar',
                {
                    cod_symbol: this.cod_symbol,
                    sentido: this.side,
                    cod_subyacente: this.cod_subyacente,
                    fch_expiracion: date.transform(this.fch_exp, "DD/MM/YYYY","YYYY-MM-DD"),
                    imp_ejercicio: parseFloat(this.strike),
                    ctd_tamano_contrato: parseInt(this.ctd_tamano_contrato),
                    cod_moneda: this.cod_moneda
                },
                postconfig()
            ).then(httpresp => {
                this.msgbox = {
                    httpresp: httpresp
                }
            })
        },
        reset:function(action){
            if(action=="new"){
                this.title = "Nuevo contrato"
            }
        },
        sel_subyacente:function(selection){
            this.cod_subyacente = selection.value
            this.nom_subyacente = selection.label
            this.build_cod_symbol()
        },
        sel_moneda:function(selection){
            this.cod_moneda = selection.value   
            this.nom_moneda = selection.label            
        },
        change_cod_symbol:function(){
            
            let cod_subyacente = this.cod_symbol.slice(0,-17)
            let fch_exp_yyyymmdd = this.cod_symbol.slice(-17,-9)
            let fch_exp = date.transform(fch_exp_yyyymmdd,"YYYYMMDD","DD/MM/YYYY")

            let sentido = this.cod_symbol.slice(-9,-8)
            if (sentido == "C"){
                sentido = "call"
            }
            if (sentido == "P"){
                sentido = "put"
            }
            
            let imp_ejercicio = parseFloat(parseInt(this.cod_symbol.slice(-8))/1000)
            this.cod_subyacente = cod_subyacente
            this.fch_exp = fch_exp
            this.side = sentido
            this.strike = imp_ejercicio
            this.cod_moneda = "USD"
        },
        build_cod_symbol:function(){
            let fch_exp = "" 
            if (this.fch_exp != ""){
                fch_exp = date.transform(this.fch_exp, "DD/MM/YYYY","YYYYMMDD")
            }            

            let cod_subyacente = ""
            if (this.cod_subyacente != ""){
                cod_subyacente = this.cod_subyacente
            }
            
            let sentido = ""
            if (this.side == "call"){
                sentido = "C"
            }
            if (this.side == "put"){
                sentido = "P"
            }

            let strike = ""
            if (this.strike != ""){
                strike = (this.strike*1000).toString().padStart(8,'0')
            }

            this.cod_symbol = cod_subyacente+fch_exp+sentido+strike
        }

    }
}
</script>