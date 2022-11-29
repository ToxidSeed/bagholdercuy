<template>    
        <div>        
            <q-splitter
            v-model="visible"
            :limits="[0,100]"
            style="height:100hr"
            >            
                <template v-slot:before>
                    <router-view                     
                    v-on:procesar-fin="procesar_fin_handler"
                    v-on:fch_transaccion-change="actualizar_tabla_fondos"
                    ></router-view>
                </template>
                <template v-slot:after >
                    <div>
                        <q-btn no-caps class="q-mb-xs" color="blue-10" label="Deposito" :to="{name:'funds-deposito'}"/>
                        <q-btn no-caps class="q-ml-xs q-mb-xs" color="blue-10" label="Retiro" :to="{name:'funds-retiro'}"/>
                        <q-btn no-caps class="q-ml-xs q-mb-xs" color="blue-10" label="Conversion" :to="{name:'funds-conversion'}"/>
                        <q-btn no-caps class="q-ml-xs q-mb-xs" color="blue-10" label="Recalcular" :to="{name:'funds-recalcular'}"/>
                        <q-btn no-caps class="q-ml-xs q-mb-xs" color="blue-10" label="Reorganizar" :to="{name:'funds-reorganizar'}"/>

                        <!--<q-btn no-caps class="q-ml-xs q-mb-xs" color="blue-10" label="test" @click="test" />-->
                    </div>
                    <TableTransaccionesFondosFecha ref="TableTransaccionesFondosFecha" v-bind:in_filter="filter" v-bind:init="true"/>
                </template>
            </q-splitter>        
    </div>
</template>
<script>
//import TableFunds from '@/components/Funds/TableFunds.vue'
import TableTransaccionesFondosFecha from '@/components/Funds/TableTransaccionesFondosFecha.vue'
//import {CLIENT_DATE_FORMAT} from '@/common/constants.js'
//import date from 'date-and-time';
    
export default {
    name:"PanelFunds",
    components:{        
        TableTransaccionesFondosFecha
    },
    props:{
        visible:{
            type:Number,
            default:0
        }        
    },    
    data:() => {
        return {
            filter:{
                updtime:Date.now()
            }
        }
    },
    mounted:function(){
        /*let fch_actual = date.format(new Date(),CLIENT_DATE_FORMAT)
        console.log(fch_actual)
        this.filter = {
            fch_transaccion: date.format(new Date(),CLIENT_DATE_FORMAT),
            updtime:Date.now()
        }*/
        //this.filter.fch_transaccion = this.fch_actual
        //this.filter.updtime = Date.now()        
        //this.actualizar_tabla_fondos()
    },
    methods:{
        procesar_fin_handler:function(data){
            console.log(data)
            let fch_transaccion = data.fch_transaccion
            this.actualizar_tabla_fondos(fch_transaccion)
            this.$emit('procesar-fin')
        },
        actualizar_tabla_fondos:function(fch_transaccion=null){                      
            /*console.log(fch_transaccion)*/
            this.filter = {
                fch_transaccion: fch_transaccion,
                updtime:Date.now()
            }            
            /*this.$refs.TableTransaccionesFondosFecha.get_transacciones_x_fecha()*/
        }
    }
}
</script>