<template>
    <div>
        <q-card>            
            <q-banner rounded class="bg-green text-white">
                <div class="row">
                    <q-icon color="white" name="add" style="font-size: 2em;"/>
                    <div class="text-subtitle1 q-mt-xs">Registro de un nuevo contrato</div>
                </div>
            </q-banner>
            <q-toolbar>                                             
                <q-btn label="Guardar" color="primary" @click="btn_guardar_click"/>
                <q-space />
                <q-btn flat round dense icon="close" to="/opciones" />
            </q-toolbar>
            <q-card-section>
                <div class="row">
                    <q-input class="col-3"
                        label="ID"
                        readonly
                        stack-label
                        v-model="opcion_id"
                    />
                    <q-input class="col-9 q-pl-xs" stack-label label="Symbol" v-model="symbol"                    
                    />
                </div>
                <div class="row">
                    <q-select class="col-3" stack-label label="Side" v-model="side" :options="lista_sides"/>
                    <SelectSymbol class="col-9 q-pl-xs" label="Seleccionar Subyacente"/>
                </div>
                <div class="row">
                    <q-input stack-label label="Fch. exp" v-model="fch_exp"
                    mask="##/##/####"
                    class="col-3"
                    fill-mask=""                    
                    />
                    <q-input stack-label label="Strike" v-model="strike"
                    class="col-2 q-pl-xs"                    
                    input-class="text-right"
                    />
                    <q-input stack-label label="Tamaño" v-model="tamano"
                    class="col-2 q-pl-xs"
                    input-class="text-right"
                    />                
                    <SelectMoneda class="col-5 q-pl-xs"/>         
                </div>
                       
            </q-card-section>
            <q-card-actions>
                                
            </q-card-actions>
        </q-card>
    </div>
</template>
<script>
import SelectSymbol from '@/components/SelectSymbol.vue'
import SelectMoneda from '@/components/SelectMoneda.vue'
export default {
    name:"PanelMantOpciones",
    components:{
        SelectSymbol,
        SelectMoneda
    },
    props:{
        action:{
            type:String,
            default:""
        },
        test:{
            type:String,
            default:""
        }
    },
    data: () => {
        return {
            title:"",            
            opcion_id:"",
            symbol:"",
            subyacente:"",
            fch_exp:"",
            strike:"",
            side:"",
            lista_sides:[
                "call",
                "put"
            ]
        }
    },
    mounted:function(){
        this.reset(this.action)
    },
    watch:{
        action:function(newval){
            this.reset(newval)
        }
    },
    methods:{
        btn_guardar_click:function(){
            console.log(this.action)
            console.log(this.test)
        },
        reset:function(action){
            if(action=="new"){
                this.title = "Nuevo contrato"
            }
        }

    }
}
</script>