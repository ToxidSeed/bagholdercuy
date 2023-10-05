<template>
    <div>
        <q-dialog v-model="open">
            <q-card style="width:450px;">
                <q-toolbar>
                    <q-toolbar-title class="text-blue-10">Filtros</q-toolbar-title>
                </q-toolbar>
                <q-separator/>
                <q-card-section>                    
                    <q-input label="Codigo de la opcion" color="blue-10" stack-label v-model="cod_opcion"/>   
                    <SelectSymbol :label="'Seleccionar subyacente'" v-on:select-symbol="select_symbol"/>
                    <div class="q-pt-xs text-blue-10 text-h6">{{cod_subyacente}}</div>
                    <div>{{ nom_subyacente }}</div>
                    <div class="q-col-gutter-xs row">
                        <q-input class="col-4" label="Año expiracion" color="blue-10" stack-label v-model="anyo_expiracion"/>                    
                        <q-input class="col-4" label="Mes expiracion" color="blue-10" stack-label v-model="mes_expiracion"/>                    
                        <q-input class="col-4" label="Dia expiracion" color="blue-10" stack-label v-model="dia_expiracion"/>     
                    </div>                    
                    <div>
                        <q-checkbox label="Call" v-model="flg_call" color="blue-10"/>
                        <q-checkbox label="put" v-model="flg_put" color="blue-10"/>
                    </div>
                </q-card-section>
                <q-separator/>
                <q-card-actions align="right">
                    <q-btn label="Aceptar" color="blue-10" class="text-capitalize" @click="filtrar"></q-btn>
                    <q-btn flat dense color="blue-10" class="text-capitalize" icon="filter_alt_off" @click="reset">Reset</q-btn>
                    <q-btn label="Cancelar" color="red-10" @click="open=false" class="text-capitalize"></q-btn>
                </q-card-actions>                
            </q-card>
        </q-dialog>        
    </div>
</template>
<script>
import SelectSymbol from "@/components/SelectSymbol.vue";

export default {
    name:"WinFiltrosPosicionOpciones",
    props:{
        value:{
            required:true
        }
    },    
    components:{
        SelectSymbol
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
            cod_subyacente:"",
            nom_subyacente:"",
            cod_opcion:"",
            anyo_expiracion:"",
            mes_expiracion:"",
            dia_expiracion:"",
            flg_call: true,
            flg_put:true
        }
    },
    methods:{
        select_symbol:function(item){
            this.cod_subyacente = item.value
            this.nom_subyacente = item.label
        },
        filtrar:function(){
            this.$emit('filtrar-posiciones-opcion',{
                cod_subyacente: this.cod_subyacente,
                cod_opcion: this.cod_opcion,
                anyo_expiracion: this.anyo_expiracion,
                mes_expiracion: this.mes_expiracion,
                dia_expiracion: this.dia_expiracion,
                flg_call: this.flg_call,
                flg_put: this.flg_put
            })
            this.open = false
        },
        reset:function(){
            this.cod_subyacente = ""
            this.nom_subyacente = "",
            this.cod_opcion = "",
            this.anyo_expiracion = "",
            this.mes_expiracion = "",
            this.dia_expiracion = "",
            this.flg_call = true,
            this.flg_put = true
            this.filtrar()
        }
    }
}
</script>