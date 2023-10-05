<template>
    <div>
        <q-toolbar>
            <q-toolbar-title class="text-blue-10">
                Reorganizar Ordenes
            </q-toolbar-title>
        </q-toolbar>        
        <q-card flat>            
            <q-toolbar>
                <div class="q-gutter-xs">
                    <q-btn label="Reorganizar" color="blue-10" />                                        
                </div>
            </q-toolbar>            
            
            <q-card-section class="q-pb-none q-pt-none">
                <div class="q-gutter-xs">
                    <q-radio v-model="flg_opcion" :val="false" label="Otros Activos" color="blue-10"/>
                    <q-radio v-model="flg_opcion" :val="true" label="Opciones" color="blue-10"/>
                </div>
            </q-card-section>                        
            <q-card-section v-if="flg_opcion==false" class="row q-pt-none">
                <div class="col-4">
                    <SelectSymbol v-on:select-symbol="sel_symbol"/>
                    <div class="q-pt-xs text-bold">{{ cod_symbol }}</div>
                    <div>{{ nom_symbol }}</div>
                </div>
            </q-card-section>            
            <q-card-section v-if="flg_opcion==true" class="row q-pt-none">
                <div class="q-col-gutter-xs col-4 row">
                    <q-input label="Codigo de opcion" stack-label color="blue-10" class="col-9"/>
                    <div class=" q-mt-md">
                        <q-btn flat dense label="Buscar" icon="search" color="blue-10" class="text-capitalize" @click="get_ordenes_x_fecha(filter.fch_orden)"/>
                    </div>                        
                </div>                                        
            </q-card-section>                            
            <q-card-section class="row q-pt-none">
                <div class="col-2 q-col-gutter-xs row">
                    <div class="col-6">
                        <q-input color="blue-10" label="Fch. Orden" stack-label hint="dd/mm/yyyy" mask="##/##/####"/>
                    </div>
                    <div class="col-6 q-pt-md">
                        <q-btn flat dense label="Ver fechas" icon="calendar_month" color="blue-10" class="text-capitalize" @click="open_fechas_helper"/>
                    </div>
                </div>
            </q-card-section>
        </q-card>                
        <TableOperacionesDia/>
    </div>
</template>
<script>
import TableOperacionesDia from '@/components/Holdings/TableOperacionesDia.vue'
import SelectSymbol from '@/components/SelectSymbol.vue';
export default {
    name:"PanelReorganizar",
    components:{
        TableOperacionesDia,
        SelectSymbol
    },
    data: () =>  {
        return {
            flg_opcion:false,
            cod_symbol:"",
            nom_symbol:""
        }
    },
    methods:{
        sel_symbol:function(item){
            this.cod_symbol = item.value
            this.nom_symbol = item.label
        }
    }
}
</script>