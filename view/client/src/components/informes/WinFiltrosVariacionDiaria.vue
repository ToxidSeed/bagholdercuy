<template>
    <q-dialog v-model="open">
        <q-card style="width:500px;">
            <q-toolbar class="text-blue-10">
                <q-btn flat round dense icon="filter_alt"></q-btn>
                <q-toolbar-title>
                    Filtros
                </q-toolbar-title>
                <q-btn flat round dense icon="close" color="red" @click="btn_cerrar_click"/>
            </q-toolbar>
            <q-card-section>
                <SelectSymbol v-on:select-symbol="select_symbol_handler"/>
                <div class="q-gutter-sm q-pt-md">
                    <div class="text-h6">{{ symbol_value }}</div>
                    <div>{{ symbol_text }}</div>
                </div>                          
                <q-separator spaced/>
                <div>
                    <div class="row text-blue-10 text-body1">
                        <div>Condiciones</div>
                        <q-space />
                        <q-btn no-caps icon="add" label="Añadir" flat dense color="blue-10" @click="btn_agregar_condicion"></q-btn>
                    </div>
                    <div class="row q-col-gutter-xs" v-for="item in condiciones" v-bind:key="item">
                        <!--
                        <span>{{item.campo.label}}</span><span class="q-pl-xs">{{item.operador.label}}</span><span class="q-pl-xs">{{ item.valor }}</span>                    
                        -->
                        
                        <div class="row col-7 q-col-gutter-xs">
                            <div class="col-3">
                                <q-input label="Cond." stack-label color="blue-10"></q-input>
                            </div>
                            <div class="col">
                                <q-select
                                label="Campo"
                                color="blue-10"
                                stack-label
                                :options="campos"
                                v-model="item.campo"
                                >

                                </q-select>         
                            </div>
                        </div>
                        <div class="col-2">
                            <q-select
                            label="Comp."
                            color="blue-10"
                            stack-label
                            :options="operadores_comparacion"
                            v-model="item.oper_comparacion"
                            >

                            </q-select>
                        </div>
                        <div class="col">
                            <q-input
                            stack-label
                            label="Valor"
                            color="blue-10"
                            v-model="item.valor"
                            input-class="text-right"
                            type="number"
                            mask="#.#"
                            >
                            </q-input>
                        </div>
                        <div class="column justify-center" >
                            <div>
                                <q-btn icon="close" flat dense color="red" round/>
                            </div>
                        </div>
                    </div>      
                </div>
            </q-card-section>
            <q-card-actions  align="right">
                <q-btn label="Aceptar" color="blue-10" @click="btn_aceptar_click" v-close-popup />
                <q-btn label="Cerrar" color="red-10" @click="btn_cerrar_click"/>
            </q-card-actions>
        </q-card>   
    </q-dialog>
</template>
<script>
import SelectSymbol from "@/components/SelectSymbol.vue";

export default {
    name:"WinFiltrosVariacionDiaria",
    components:{
        SelectSymbol
    },
    props:{
        value:{
            required:true
        }
    },
    data() {
        return {
            open:this.value,
            symbol_value:"",
            symbol_text:"",
            condiciones:[],
            campos: [
                {
                    value:"pct_variacion_cierre",
                    label:"pct. variacion cierre"
                },{
                    value:"pct_variacion_maximo",
                    label:"pct. variacion maximo"
                },{
                    value:"pct_variacion_minimo",
                    label:"pct. variacion minimo"
                }
            ],
            operadores_logicos:[
                {
                    value:"and",
                    label:"and"
                },
                {
                    value:"or",
                    label:"or"
                }
            ],
            operadores_comparacion: [
                {
                    value:"igual",
                    label:"="
                },{
                    value:"menor_que",
                    label:"<="
                },{
                    value:"mayor_que",
                    label:">="
                },{
                    value:"mayor",
                    label:">"
                },{
                    value:"menor",
                    label:">"
                }
            ],
            campo_selectionado:null,
            operador_comparacion: null,
            valor_actual: null
        }
    },
    watch:{
        open:function(newval){
            this.$emit('input',newval)
        },
        value:function(newval){
            this.open = newval
        }
    },
    methods:{        
        select_symbol_handler:function(selected){
            this.symbol_value = selected.value
            this.symbol_text = selected.label
        },
        btn_aceptar_click:function(){
    
            this.$emit('btn-aceptar-click',{
                symbol_value:this.symbol_value,
                symbol_text: this.symbol_text
            })
        },
        btn_cerrar_click:function(){
            this.$emit('btn-cerrar-click')
            this.open = false
        },
        btn_agregar_condicion: function(){
            /*
            let element = {
                campo: this.campo_selectionado,
                operador: this.operador_comparacion,
                valor: this.valor_actual
            }
            */
            let campo = null
            let oper_comparacion = null

            let row = {
                campo: campo,
                oper_comparacion: oper_comparacion,
                valor:null
            }
            
            this.condiciones.push(row)
        }
    }
}
</script>