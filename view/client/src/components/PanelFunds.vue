<template>
    <div>
        <div>
            <q-btn color="green" label="Deposit" @click="deposit"/>
            <q-btn color="red" label="Withdraw" @click="withdraw"/>
            <q-btn color="primary" label="Convert" @click="convert"/>
        </div>
        <div class="row" >
            <div v-if="panel_show==true" class="col-3">                
                <PanelDeposit v-if="deposit_show == true" v-on:deposit-cancel="deposit_cancel" />
                <PanelWithdraw v-if="withdraw_show == true" v-on:withdraw-cancel="withdraw_cancel"/>
                <PanelConversionMoneda v-if="convert_show==true" v-on:conversion-moneda-cancel="convert_cancel"/>
            </div>
            <div class="col-4">
                <TableFunds/>
            </div>    
        </div>
    </div>
</template>
<script>
import PanelDeposit from './PanelDeposit.vue'
import PanelWithdraw from './PanelWithdraw.vue'
import PanelConversionMoneda from './PanelConversionMoneda.vue'
import TableFunds from './TableFunds.vue'
    
export default {
    name:"PanelFunds",
    components:{
        PanelDeposit,
        PanelWithdraw,
        PanelConversionMoneda,
        TableFunds
    },
    data:() => {
        return {
            panel_show:false,
            deposit_show:false,
            withdraw_show:false,
            convert_show:false
        }
    },
    methods:{
        deposit:function(){                        
            this.panel_show = true
            this.deposit_show = true
            this.withdraw_show = false
            this.convert_show = false
        },
        withdraw:function(){
            this.panel_show = true
            this.deposit_show = false
            this.withdraw_show = true
            this.convert_show = false
        },
        convert:function(){
            this.panel_show = true
            this.deposit_show = false
            this.withdraw_show = false
            this.convert_show = true
        },
        deposit_cancel:function(){
            this.panel_show = false
            this.deposit_show = false            
        },
        withdraw_cancel:function(){        
            this.panel_show = false
            this.withdraw_show = false
        },
        convert_cancel:function(){
            this.panel_show = false
            this.convert_show = false
        }
    }
}
</script>