<template>
    <div>
        <q-toolbar>
            <q-toolbar-title class="text-blue-10 text-bold">Rentabilidad diaria de opciones</q-toolbar-title>
        </q-toolbar>
        <div class="row q-col-gutter-xs">
            <q-card>
                <q-card-section>
                    <div>
                        <SelectSymbol/>
                    </div>                    
                </q-card-section>
            </q-card>
        </div>
    </div>
</template>
<script>
//import TableListaCuentas from "@/components/cuenta/TableListCuentas.vue"
import SelectSymbol from "@/components/SelectSymbol.vue"

export default {
    name:"PanelSimulacionRentabilidadDiariaOpciones",
    components:{
        SelectSymbol
    },
    data (){
        return {
            ver_panel_izquierdo:false
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