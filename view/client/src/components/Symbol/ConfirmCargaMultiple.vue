<template>
<q-dialog v-model="open" persistent>
            <q-card>
                <q-card-section class="row items-center">                    
                    <div class="col-1">
                        <q-avatar icon="play_arrow" color="green" text-color="white" />
                    </div>
                    <div class="col-11">
                        <div class="q-ml-sm">Se va a proceder a realizar la carga masiva de symbols, si alguno ya se encuentra registrado se omitirá, ¿Desea continuar?</div>                    
                    </div>
                </q-card-section>

                <q-card-actions align="right">
                    <q-btn label="Ejecutar" color="blue-10" 
                    @click="btnEjecutarClick" v-close-popup />
                    <q-btn flat label="Cancelar" color="red-10" v-close-popup />                
                </q-card-actions>
            </q-card>
        </q-dialog>
</template>
<script>
export default {
    name:"ConfirmCargaMultiple",
    props:{
        value:{
            required:true
        }
    },
    watch:{
        open:function(newVal){
            this.$emit('input', newVal)
        },
        value:function(newVal){
            this.open = newVal
        }
    },
    data(){
        return {
            open: this.value
        }
    },
    methods:{
        btnEjecutarClick:function(){
            this.$emit('ejecutar')
        }
    }
}
</script>