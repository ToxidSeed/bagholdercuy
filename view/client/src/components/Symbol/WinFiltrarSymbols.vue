<template>
    <q-dialog v-model="open">                
        <q-card style="width:400px;">
            <q-toolbar>
                <q-toolbar-title class="text-blue-10">Filtro de symbols</q-toolbar-title>
            </q-toolbar>
            <q-separator/>
            <q-card-section> 
                <div>
                    <q-input color="blue-10" label="Identificador del Symbol" stack-label v-model="id_symbol"></q-input>
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

export default {
    name:"WinFiltrarSymbols",    
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
            id_symbol:""
        }
    },
    methods:{        
        btn_aceptar_click:function(){            
            this.$emit(
                'btn-aceptar-click',{
                    id_symbol: this.id_symbol
                }
            )

            this.open = false
        }
    }
}
</script>