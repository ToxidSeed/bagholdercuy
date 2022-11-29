<template>
    <div>
        <q-card>
            <q-card-section class="row q-pb-none q-pt-none">
                <div class="text-h6 text-blue-10">Recalcular</div>
                <q-space/>
                <q-btn  flat dense rounded icon="close" :to="{name:'funds'}"/>
            </q-card-section>
            <q-card-action class="q-pl-md q-pt-none">
                <q-btn no-caps label="Procesar" color="blue-10" @click="recalcular"/>                
            </q-card-action>
            <q-card-section>
                <div class="row">
                    <q-select stack-label class="col-8" v-model="tipo_reproceso" :options="options" label="Seleccionar tipo de reproceso" />
                    <!--<q-checkbox class="col-12" v-model="reprocesar_todo" label="Reprocesar Todo" />-->
                    <q-input class="col-4 q-pl-xs" stack-label label="Fecha desde:"
                    mask="##/##/####"
                    fill-mask="_"
                    hint="dd/mm/yyyy"
                    v-model="fch_desde"
                    :readonly="fch_desde_readonly"
                    />                    
                </div>
                <q-badge color="blue" outline multi-line class="q-mt-xs q-pt-xs">
                La fecha desde la que se van a recalcular todas las transacciones, si no se ingresa ninguna fecha se reprocesarán todas las transacciones.
                </q-badge>
            </q-card-section>
        </q-card>
        <Messagebox ref="msgbox" />
    </div>
</template>
<script>
import Messagebox from '@/components/MessageBox.vue'
import {config} from '@/common/request.js'
export default {
    name:"PanelRecalcularFondos",
    components:{
        Messagebox
    },
    data: () => {
        return {
            fch_desde:"",
            tipo_reproceso:{"value":"FCH_DESDE","label":"Reprocesar desde una fecha"},            
            options:[
                {"value":"FCH_DESDE","label":"Reprocesar desde una fecha"},
                {"value":"TODO","label":"Reprocesar todo"}               
            ]
        }
    },
    computed:{
        fch_desde_readonly:function(){
            if(this.tipo_reproceso.value !=1){
                return true
            }else{
                return false
            }
        }
    },
    methods:{
        recalcular:function(){
            this.$http.post('/FundsManager/ReprocesarController/procesar',{
                fch_desde: this.fch_desde,
                tipo_reproceso: this.tipo_reproceso.value
            },config()).then(httpresp => {
                this.$refs.msgbox.httpresp(httpresp)
            })
        }
    }
}
</script>