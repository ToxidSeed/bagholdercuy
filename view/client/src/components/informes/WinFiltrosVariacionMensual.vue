<template>
    <q-dialog v-model="open">
        <q-card style="width:500px;">            
            <q-toolbar class="text-blue-10">
                <q-btn flat round dense icon="filter_alt"/>
                <q-toolbar-title>
                    Filtros
                </q-toolbar-title>
                <q-btn flat round dense icon="close" color="red"/>
            </q-toolbar>
            <q-card-section>
                <SelectSymbol v-on:select-symbol="select_symbol_handler"/>
                <div class="q-gutter-sm q-pt-md">
                    <div class="text-h6">{{ symbol_value }}</div>
                    <div>{{ symbol_text }}</div>
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
    name:"WinFiltrosVariacionMensual",    
    components:{
        SelectSymbol
    },
    props:{
        value:{
            required:true
        }
    },
    data(){
        return {
            open:this.value,
            symbol_value:"",
            symbol_text:""
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
            console.log(selected)
            //this.symbol_value = selected-symbol
            this.symbol_value = selected.value
            this.symbol_text = selected.label
        },
        btn_aceptar_click:function(){
            this.$emit('btn-aceptar-click',{
                symbol_value: this.symbol_value,
                symbol_text: this.symbol_text
            })
        },
        btn_cerrar_click:function(){
            this.$emit('btn-cerrar-click')
            this.open = false
        }        
    }
}
</script>