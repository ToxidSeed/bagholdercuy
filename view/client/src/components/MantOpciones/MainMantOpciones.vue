<template>
    <div>      
        <div class="text-primary q-pl-md text-h6">Contratos de Opciones</div>
        <q-splitter
            v-model="visible"
            :limits="[0, 100]"    
            style="height: 100hr"    
        >                
            <template v-slot:before>
                <router-view
                v-on:procesar-completado="actualizar_lista_opciones"
                ></router-view>
            </template>

            <template v-slot:after>
                <q-toolbar>
                    <q-btn color="primary" label="Nuevo" :to="{name:'opciones-new'}"></q-btn>                    
                    <q-btn class="q-ml-xs" color="primary" label="Carga Masiva" :to="{name:'opciones-loader'}"></q-btn>
                </q-toolbar>
                <TableListOpciones/>  
            </template>                
        </q-splitter>
    </div>
</template>
<script>
//import PanelMantOpciones from "@/components/MantOpciones/PanelMantOpciones.vue"
import TableListOpciones from "@/components/MantOpciones/TableListOpciones.vue"
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
        TableListOpciones
    },
    data: () => {
        return {
            visible:0
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
        }
    },
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
    }
}
</script>