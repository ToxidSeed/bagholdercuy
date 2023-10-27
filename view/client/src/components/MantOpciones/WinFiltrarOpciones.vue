<template>
    <q-dialog v-model="open">                
        <q-card style="width:400px;">
            <q-toolbar>
                <q-toolbar-title class="text-blue-10">Filtros</q-toolbar-title>
            </q-toolbar>
            <q-separator/>
            <q-card-section>
                <div >
                    <q-input color="blue-10" stack-label v-model="id_contrato_opcion" label="Identificador contrato opcion"/>
                </div>
                <SelectSymbol
                    v-on:select-symbol="sel_symbol" :label="'Subyacente'"
                />
                <div class="q-pt-xs text-blue-10 text-h6">{{ cod_symbol }}</div>
                <div>{{ nom_symbol }}</div>
                <div class="row">
                    <div class="col-4">
                        <q-checkbox v-model="selection" val="call" label="call"/>
                        <q-checkbox v-model="selection" val="put" label="put"/>
                    </div>
                    <div class="col-3 q-pl-xs">
                        <q-input stack-label label="strike" v-model="imp_ejercicio" />
                    </div>
                    <div class="col-5 q-pl-xs">
                        <q-input stack-label label="Fch. Expiración" v-model="fch_expiracion" hint="dd/mm/yyyy" mask="##/##/####" ></q-input>
                    </div>
                </div>
            </q-card-section>
            <q-separator/>
            <q-card-actions align="right">
                <q-btn label="Aceptar" color="blue-10" @click="aplicar_filtro"></q-btn>
                <q-btn label="Cancelar" color="red-14" @click="open=false"></q-btn>
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>
<script>
import SelectSymbol from '@/components/SelectSymbol.vue'
import date from 'date-and-time'

export default {
    name:"WinFiltrarOpciones",
    components:{
        SelectSymbol
    },
    props:{
        infiltros:{
            type:Object,
            default: () => {}
        },
        value:{
            required:true
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
    data(){
        return {
            open:this.value,
            id_contrato_opcion:"",
            selection:[],
            cod_symbol:"",
            fch_expiracion:"",
            imp_ejercicio:"",
            nom_symbol:""
        }
    },
    methods:{
        sel_symbol:function(selected){
            this.cod_symbol = selected.value
            this.nom_symbol = selected.label
        },
        aplicar_filtro:function(){
            let fch_exp_iso_format = ""

            if (this.fch_expiracion != ""){
                fch_exp_iso_format = date.transform(this.fch_expiracion, "DD/MM/YYYY","YYYY-MM-DD")
            }            

            this.$emit(
                'btn-aceptar-click',{
                    id_contrato_opcion: this.id_contrato_opcion,
                    cod_symbol:this.cod_symbol,
                    sentidos:this.selection,
                    fch_expiracion:fch_exp_iso_format,
                    imp_ejercicio:this.imp_ejercicio
                }
            )
            this.open = false
        }
    }
}
</script>