<template>
    <div>
        <q-card>
            <q-toolbar>
                <q-toolbar-title class="text-blue-10">Rentabilidad de opciones</q-toolbar-title>
            </q-toolbar>            
            <q-card-section class="q-pt-none">
                <div class="row">
                    <div>
                        <SelectSymbol v-on:select-symbol="select_symbol"/>                        
                        <div class="col-12 q-pt-xs">
                            <span class="text-subtitle1 text-blue-10">
                                {{ cod_symbol }}
                            </span>
                            <span>
                                {{ nom_symbol }}
                            </span>
                        </div>
                    </div>
                    <div class="column justify-center">
                        <q-btn label="Cadena de Opciones" no-caps flat icon="link" color="blue-10" @click="win_opciones.visible=true"/>
                    </div>
                </div>                    
            </q-card-section>                            
        </q-card>
        <q-dialog v-model="win_opciones.visible">
            <PanelOptionsChain style="max-width:750px"
                v-bind:symbol_val="cod_symbol"
                v-bind:symbol_name="nom_symbol"
                v-on:option-select="option_selected"
                v-on:close="win_opciones.visible=false"
                v-on:sel-contract="option_selected"
            />
        </q-dialog>   
    </div>
</template>
<script>
//import TableListaCuentas from "@/components/cuenta/TableListCuentas.vue"
import SelectSymbol from "@/components/SelectSymbol.vue"
import PanelOptionsChain from "@/components/common/PanelOptionsChain.vue"

export default {
    name:"PanelSimulacionRentabilidadOpciones",
    components:{
        SelectSymbol,
        PanelOptionsChain
    },
    data (){
        return {
            ver_panel_izquierdo:false,
            cod_symbol:"",
            nom_symbol:"",
            win_opciones:{
                visible: false
            }
        }   
    },
    watch:{
        $route: function(){
            this.habilitar()
        }
    },
    mounted:function(){
        this.habilitar()                
    },
    methods:{
        select_symbol: function(item){
            this.cod_symbol = item.value
            this.nom_symbol = item.label
        },
        habilitar:function(){
            /*if (this.$route.name == "cuenta"){
                this.lpanel_visible = false
            }
            if (this.$route.name == "cuenta-nuevo"){
                this.lpanel_visible = true
            }
            if (this.$route.name == "cuenta-ver"){
                this.lpanel_visible = true
            }
            if (this.$route.name == "cuenta-editar"){
                this.lpanel_visible = true
            }*/
        },
        get_cuentas:function(){
            //this.$refs.TableListaCuentas.get_cuentas()
        }
    }
}
</script>