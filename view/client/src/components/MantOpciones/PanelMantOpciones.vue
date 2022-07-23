<template>
    <div>
        <q-card>
            <q-toolbar>
                <q-toolbar-title class="text-primary">
                    Opciones
                </q-toolbar-title>
            </q-toolbar>
            <q-card-section>
                <div class="row">
                    <q-input class="col-3"
                        label="ID"
                        readonly
                        v-model="opcion_id"
                    />
                    <q-input class="col-9" label="Symbol" v-model="symbol"                    
                    />
                </div>
                <div class="row">
                    <q-select class="" dense label="Side" v-model="side" :options="lista_sides"/>
                    <q-input label="Subyacente" v-model="subyacente"/>
                </div>
                
                <q-input label="Fch. exp" v-model="fch_exp"/>
                <q-input label="Strike" v-model="strike"/>
                <q-input label="Tamaño" v-model="tamano"/>
                <q-input label="Moneda" v-model="moneda"/>
            </q-card-section>
            <q-card-actions>
                <q-btn label="Guardar" color="primary" @click="btn_guardar_click"/>                
            </q-card-actions>
        </q-card>
    </div>
</template>
<script>
export default {
    name:"PanelMantOpciones",
    data: () => {
        return {
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
    methods:{
        btn_guardar_click:function(){

        }
    }
}
</script>