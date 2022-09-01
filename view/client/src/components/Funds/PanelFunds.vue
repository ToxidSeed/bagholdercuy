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
                    <q-btn no-caps class="q-mb-xs" color="green" label="Deposit" :to="{name:'funds-deposito'}"/>
                    <q-btn no-caps class="q-ml-xs q-mb-xs" color="red" label="Withdraw" :to="{name:'funds-retiro'}"/>
                    <q-btn no-caps class="q-ml-xs q-mb-xs" color="primary" label="Convert" :to="{name:'funds-conversion'}"/>
                </div>
                <TableFunds ref="table_funds"/>
            </template>
        </q-splitter>
        <!--<div class="row" >
            <div v-if="panel_show==true" class="col-4">                
                <PanelDeposit v-if="deposit_show == true" 
                v-on:deposit-cancel="deposit_cancel" 
                v-on:save-end="actualizar_tabla_fondos"/>
                <PanelWithdraw v-if="withdraw_show == true" 
                v-on:withdraw-cancel="withdraw_cancel"
                v-on:save.end="actualizar_tabla_fondos"/>
                <PanelCurrencyConversion v-if="convert_show==true"/>
            </div>
            <div class="col-4">
                <TableFunds ref="table_funds"/>
            </div>    
        </div>-->
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