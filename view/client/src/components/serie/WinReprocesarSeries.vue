<template>
    <div>
        <q-dialog v-model="open">
            <q-card style="width:450px;">
                <q-toolbar>
                    <q-toolbar-title class="text-blue-10">Reparar Serie: {{ store.state.w_reprocesar.cod_symbol }}</q-toolbar-title>
                </q-toolbar>
                <q-separator/>
                <q-card-section>
                    <q-file
                        v-model="store.state.w_reprocesar.fichero"
                        label="Seleccionar fichero"
                        use-chips                
                        color="blue-10"        
                    >                
                        <template v-slot:prepend>
                            <q-icon name="attach_file" />
                        </template>
                    </q-file>                    
                </q-card-section>
                <q-separator/>
                <q-card-actions align="right">
                    <q-btn label="Aceptar" color="blue-10" @click="store.reprocesar_serie(store.state.w_reprocesar.cod_symbol)"></q-btn>
                    <q-btn label="Cancelar" color="red-10" @click="open=false"></q-btn>
                </q-card-actions>
                <q-inner-loading :showing="loading">
                    <q-spinner-gears size="50px" color="primary" />
                </q-inner-loading>     
            </q-card>
        </q-dialog>        
    </div>
</template>
<script>

import store from './store'
export default {
    name:"WinCargaMultiple",
    props:{
        value:{
            required:true
        }
    },
    components:{
        
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
            store: store
        }
    },
    methods:{
        
    }
}
</script>