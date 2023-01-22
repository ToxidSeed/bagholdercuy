<template>
    <div>
        <q-card>
            <q-card-section class="row q-pa-xs">
                <div class="text-h6">Cargar Series</div>    
                <q-space/>
                <q-btn flat rounded icon="close"/>                          
            </q-card-section>
            <q-card-actions class="q-pt-none q-pl-xs">
                <q-btn color="primary" label="Procesar" class="q-mt-xs" @click="procesar"/>
                <!--<q-btn color="primary" label="Reset" class="q-mt-xs q-ml-xs" @click="load"/>
                -->
            </q-card-actions>
            <q-card-section class="q-pa-xs">
                <SelectSymbol
                    v-bind:label="'Seleccionar Symbol'"
                    v-on:select-symbol="sel_symbol"
                />
                <div class="text-h6 text-weight-bold">{{symbol.value}}</div>
                <div>{{symbol.name}}</div>
            </q-card-section>
            <q-card-section class="q-pa-xs">                                          
                <div class="row">
                    <q-select 
                    class="col-6"
                    v-model="profundidad" 
                    :options="profundidad_list" 
                    label="Seleccionar Profundidad" 
                    stack-label
                    />                    
                </div>                    
            </q-card-section>       
            <q-inner-loading :showing="loading">
                <q-spinner-gears size="50px" color="primary" />
            </q-inner-loading>      
        </q-card >
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import SelectSymbol from "@/components/SelectSymbol.vue"
import MessageBox from "@/components/MessageBox.vue"
import {headers} from '@/common/common.js'

export default {
    name:"PanelSerieLoader",
    components:{
        SelectSymbol,
        MessageBox
    },
    data: () => {
        return {
            loading:false,
            symbol:{
                value:"",
                name:""
            },
            profundidad:{
                value:"",
                label:""
            },
            profundidad_list:[
            {
                value:"MESACTUAL",
                label:"MES ACTUAL"
            },{
                value:"YTD",
                label:"ANYO EN CURSO"
            },
            {
                value:"ULT3MESES",
                label:"ULTIMOS 3 MESES"
            },
            {
                value:"ULT6MESES",
                label:"ULTIMOS 6 MESES"
            },{
                value:"MAX",
                label:"MAXIMO POSIBLE"
            }]
        }
    },
    methods:{
        sel_symbol:function(selected){
            this.symbol.value = selected.value
            this.symbol.name = selected.label
        },
        procesar:function(){
            this.loading = true
            this.$http.post(
            '/SerieManager/SerieManagerLoader/procesar',{
                profundidad: this.profundidad.value,
                symbol: this.symbol.value
            },{
                headers:headers()
            }).then(httpresponse => {                
                this.$refs.msgbox.httpresp(httpresponse)
            }).catch(error => {
                console.log(error)
            }).then(() => {
                this.loading = false
                this.$emit('carga-serie-completada')
            })
        }
    }
}
</script>
