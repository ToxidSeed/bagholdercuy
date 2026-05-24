<template>
    <q-dialog v-model="open">                
        <q-card style="width:600px;">
            <q-toolbar>
                <q-toolbar-title class="text-blue-10">Ibkr Operaciones</q-toolbar-title>
            </q-toolbar>
            <q-separator/>
            <q-card-section> 
                <div>
                    <q-file v-model="archivo" label="Archivo" stack-label>
                        <template v-slot:prepend>
                            <q-icon name="attach_file" />
                        </template>
                    </q-file>
                </div>
            </q-card-section>
            <q-separator/>
            <q-card-actions align="right">
                <q-btn dense label="Aceptar" color="primary" @click="btn_aceptar_click"></q-btn>
                <q-btn flat label="Cancelar" color="red" @click="open=false"></q-btn>
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>
<script>
import Operacion from "@/api/operacion"
import { mapActions } from "vuex";
export default {
    name: "WinCargarIbkrOperaciones",      
    props: {        
        value: {
            required: true
        }
    },
    watch: {
        open: function(newval) {
            this.$emit('input', newval)
        },
        value: function(newval) {
            this.open = newval
        }
    },
    data() {
        return {
            open: this.value,
            archivo: null
        }
    },
    methods: {        
        ...mapActions(["incluir_httpresp"]),
        btn_aceptar_click: function() {            
            //this.$emit("btn-aceptar-click", this.archivo)
            Operacion.cargar_operaciones_ibkr(this.archivo).then(response => {
                this.incluir_httpresp(response)
            }).catch(error => {
                this.incluir_httpresp(error)
            })
            this.open = false
        }
    }
}
</script>
