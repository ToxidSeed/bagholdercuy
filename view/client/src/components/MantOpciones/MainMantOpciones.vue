<template>
    <div>              
        <q-toolbar class="text-blue-10">
            <q-btn flat round dense icon="menu">
                <q-menu>
                    <q-list dense>
                        <q-item clickable v-close-popup :to="{name:'opciones-loader'}">
                            <q-item-section class="text-subtitle1">
                                <div>Carga desde <span class="text-blue-10 text-bold">iexcloud</span></div>
                            </q-item-section>                            
                        </q-item>
                        <q-item clickable v-close-popup :to="{name:'opciones-loader-fichero'}">
                            <q-item-section class="text-subtitle1">
                                <div>Carga desde <span class="text-blue-10 text-bold">archivo .csv</span></div>                                 
                            </q-item-section>                            
                        </q-item>
                    </q-list>
                </q-menu>
            </q-btn>
            <q-toolbar-title>
                Contratos de Opciones
            </q-toolbar-title>
        </q-toolbar>
        <q-splitter
            v-model="visible"
            :limits="[0, 100]"    
            style="height: 100hr"    
        >                
            <template v-slot:before>
                <router-view
                    v-on:procesar-completado="actualizar_lista_opciones"                
                    v-bind:in_datos_opcion="datos_opcion"
                ></router-view>
            </template>
            <template v-slot:after>
                <q-toolbar>
                    <q-btn color="blue-10" label="Nuevo" :to="{name:'opciones-new'}"></q-btn>                    
                    <!--<q-btn class="q-ml-xs" color="blue-10" label="Carga Masiva" :to="{name:'opciones-loader'}"></q-btn>-->
                    <q-btn class="q-ml-xs text-capitalize"  color="blue-10" flat dense icon="filter_alt" @click="WinFiltrarOpciones.open=true">Filtrar</q-btn>
                </q-toolbar>
                <TableListOpciones
                    :infiltros="TableListOpciones.filtros"
                    v-on:copiar="copiar_opcion"
                />  
            </template>                
        </q-splitter>
        <WinFiltrarOpciones 
            v-model="WinFiltrarOpciones.open"        
            v-on:btn-aceptar-click="filtrar_lista_opciones"
        />
    </div>
</template>
<script>
//import PanelMantOpciones from "@/components/MantOpciones/PanelMantOpciones.vue"
import TableListOpciones from "@/components/MantOpciones/TableListOpciones.vue"
import WinFiltrarOpciones from "@/components/MantOpciones/WinFiltrarOpciones.vue"
export default {
    name:"MainMantOpciones",

    props:{
        action:{
            type:String,
            default:""
        }
    },
    components:{
        //PanelMantOpciones,
        TableListOpciones,
        WinFiltrarOpciones
    },
    data: () => {
        return {
            WinFiltrarOpciones:{
                open:false
            },
            TableListOpciones:{
                filtros:{}
            },
            datos_opcion:{},
            visible:0,
        }
    },
    mounted:function(){
        this.reset()
    },
    watch:{
        $route:function(){
            this.reset()    
        }
    },
    methods:{
        reset:function(){                      
            if(this.$route.name=="opciones"){
                this.visible=0
            }else{
                this.visible=30
            }
        },
        test:function(){
            console.log(this.action)
        },
        actualizar_lista_opciones:function(){
            console.log('ola k ase')
        },
        filtrar_lista_opciones:function(filtros){
            this.TableListOpciones.filtros = filtros
        },
        copiar_opcion:function(datos_opcion){            
            if (this.$route.name=="opciones-new"){
                this.datos_opcion = datos_opcion
            }else{
                this.$router.push({name:"opciones-new", params:{in_datos_opcion:datos_opcion}})
            }            
        }
    }/*,
    beforeRouteEnter (to, from, next) {
        console.log(to)
        console.log(next)
        console.log(from)
        next()
    },
    beforeRouteUpdate (to, from,next) {
    // just use `this`
        console.log(to)
        console.log(from)
        console.log(next)        
        next()
    }*/
}
</script>