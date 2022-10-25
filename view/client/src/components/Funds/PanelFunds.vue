<template>
    <div>        
        <q-splitter
        v-model="visible"
        :limits="[0,100]"
        style="height:100hr"
        >            
            <template v-slot:before>
                <router-view 
                v-on:deposito-fin="actualizar_tabla_fondos"
                v-on:retiro-fin="actualizar_tabla_fondos"
                v-on:conversion-fin="actualizar_tabla_fondos"
                ></router-view>
            </template>
            <template v-slot:after >
                <div>
                    <q-btn no-caps class="q-mb-xs" color="blue-10" label="Deposito" :to="{name:'funds-deposito'}"/>
                    <q-btn no-caps class="q-ml-xs q-mb-xs" color="blue-10" label="Retiro" :to="{name:'funds-retiro'}"/>
                    <q-btn no-caps class="q-ml-xs q-mb-xs" color="blue-10" label="Conversion" :to="{name:'funds-conversion'}"/>
                    <q-btn no-caps class="q-ml-xs q-mb-xs" color="blue-10" label="Recalcular" :to="{name:'funds-recalcular'}"/>
                    <q-btn no-caps class="q-ml-xs q-mb-xs" color="blue-10" label="Reorganizar" :to="{name:'funds-reorganizar'}"/>
                </div>
                <TableFunds ref="table_funds"/>
            </template>
        </q-splitter>
    </div>
</template>
<script>
import TableFunds from '@/components/Funds/TableFunds.vue'

    
export default {
    name:"PanelFunds",
    components:{        
        TableFunds
    },
    props:{
        visible:{
            type:Number,
            default:0
        }        
    }
    ,    
    data:() => {
        return {
            
        }
    },
    methods:{
         actualizar_tabla_fondos:function(){
             this.$refs.table_funds.get_funds()
         }
    }
}
</script>