<template>
    <q-dialog v-model="open">                
        <q-card style="width:400px;">
            <q-toolbar>
                <q-toolbar-title class="text-blue-10">Filtrar Operaciones</q-toolbar-title>
            </q-toolbar>
            <q-separator/>
            <q-card-section> 
                <div>
                <SelectSymbol v-on:select-symbol="sel_symbol"/>
                <div v-if="filtros.cod_symbol != ''"><span class="text-bold">{{filtros.cod_symbol}}</span> : <span>{{nom_symbol}}</span></div>
                </div>
                <div>
                    <q-checkbox v-model="filtros.flg_opciones" label="Opciones" color="blue-10" @input="check_flg_opciones"/>
                </div>
                <div>
                    <q-input stack-label label="Codigo de contrato opcion"
                    v-model="filtros.cod_contrato_opcion" color="blue-10" :disable="filtros.flg_opciones==false"/>
                </div>                
            </q-card-section>
            <q-separator/>
            <q-card-actions align="right">
                <q-btn label="Aceptar" color="blue-10" @click="btn_aceptar_click"></q-btn>
                <q-btn label="Cancelar" color="red-14" @click="open=false"></q-btn>
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>
<script>
import SelectSymbol from "@/components/SelectSymbol.vue"

export default {
    name:"WinFIltrarOperaciones",    
    components:{
        SelectSymbol
    },
    props:{        
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
            filtros:{
                cod_symbol:"",                
                cod_contrato_opcion:"",
                flg_opciones:false
            },
            nom_symbol:""
        }
    },
    methods:{        
        check_flg_opciones:function(valor){            
            if (valor == false){
                this.filtros.cod_contrato_opcion = ""
            }                   
        },
        sel_symbol:function(item){
            this.filtros.cod_symbol = item.value
            this.nom_symbol = item.label
        },
        btn_aceptar_click:function(){            
            this.$emit("btn-aceptar-click", this.filtros)

            this.open = false
        }
    }
}
</script>