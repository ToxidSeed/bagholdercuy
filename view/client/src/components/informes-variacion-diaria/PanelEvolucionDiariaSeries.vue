<template>
    <div class="bg-white">
        <q-card>
            <q-card-section>
                <div v-if="cod_symbol != ''">
                    <span class="text-blue-10 text-h6 q-pr-xs">{{ cod_symbol }}</span><span class="text-body1">{{ nom_symbol }}</span>
                </div>
                <div v-if="cod_symbol == ''">
                    <span class="text-body1 text-orange-10">Seleccionar instrumento financiero</span>
                </div>         
            </q-card-section>               
        </q-card>
        <div>
            <ChartOHLCSeriesDiaria/>
        </div>
    </div>
</template>
<script>
import ChartOHLCSeriesDiaria from "@/components/common/ChartOHLCSeriesDiaria.vue"
import _ from "lodash"
import SymbolApi from "@/api/symbol"
import {HttpResponseHandler} from "@/common/http-response-handler"
export default {
    name:"PanelEvolucionDiariaSeries",
    components:{
        ChartOHLCSeriesDiaria
    },
    data(){
        return {
            cod_symbol:"",
            nom_symbol:""
        }
    },
    
    watch:{
        $route: function(to){      
            console.log("route")      
            if (Object.keys(to.query).length > 0){                
                if (_.has(to.query,"cod_symbol")){
                    this.get_datos_symbol(to.query.cod_symbol)
                }
            }
        }
    },
    mounted:function(){
        this.init(this.$route.query)
    },
    methods:{
        init:function(query){
            if (_.has(query,"cod_symbol")){
                this.get_datos_symbol(query.cod_symbol)
            }            
        },
        get_datos_symbol: function(cod_symbol){
            const response = SymbolApi.get_symbol_x_codigo(cod_symbol)   
            response.then(httpresp => {
                HttpResponseHandler.showMessageIfError(httpresp)
                let appdata = httpresp.data
                let data = appdata.data
                this.cod_symbol = data.symbol
                this.nom_symbol = data.name
            })
        }
    }
}
</script>