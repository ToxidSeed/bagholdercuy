<template>
    <div>
        <q-table
        title="Posiciones"
        :data="data"
        :columns="columns"
        row-key="name"
        separator="vertical"
        dense

        >
            <template v-slot:top>
                <q-btn color="blue-10" label="Buy" :to="{name:'holdings-trade'}"/>                
                <q-btn color="red-10 " label="Sell" @click="sell()" class="q-ml-xs" />                
                <q-btn color="green" label="Options Chain" to="/order" class="q-ml-xs" />                
            </template>
            <template v-slot:body-cell-symbol="props">
                <q-menu
                touch-position
                context-menu
                >
                <q-list dense style="min-width: 100px" >
                    <q-item style="padding: 0px 0px" clickable v-close-popup @click="buy(props.row)">
                        <q-item-section class="bg-primary text-white"><div class="q-pl-sm">Buy</div></q-item-section>                                    
                    </q-item>
                    <q-item style="padding: 0px 0px" clickable v-close-popup @click="sell(props.row)">
                        <q-item-section class="bg-red text-white"><div class="q-pl-sm">Sell</div></q-item-section>                                    
                    </q-item>
                </q-list>
                </q-menu>
                <q-td :props="props">                    
                    {{props.value}}
                </q-td>
            </template>
            <template v-slot:body-cell-total_change="props">
                <q-td :props="props">                    
                    <div v-bind:class="{'text-red':props.row.total_change < 0,'text-green':props.row.total_change >= 0}">
                        {{props.value}}%
                    </div>
                </q-td>                
            </template>
            <template v-slot:body-cell-total_pl="props">
                <q-td :props="props">
                    <div v-bind:class="{'text-red':props.row.total_change < 0,'text-green':props.row.total_change >= 0}">
                        {{props.value}}
                    </div>
                </q-td>                
            </template>                        
        </q-table>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue';
import {postconfig} from '@/common/request.js'
export default {
    name:"TableHoldings",
    components:{
        MessageBox
    },
    data: () => {        
        return {            
            columns:[
                {
                    label:"symbol",
                    align: 'left',
                    field:"symbol",
                    name:"symbol",
                    style:"width:150px;"                              
                },{
                    label:"holding since",
                    align:"left",
                    field:"holding_since",
                    name:"holding_since",
                    style:"width:100px;"
                },
                {
                    label:"P/L",
                    align:"right",
                    field:"total_change",
                    name:"total_change",
                    style:"width:100px;"                    
                },{
                    label:"P/L IMP",
                    align:"right",
                    field:"total_pl",
                    name:"total_pl",
                    style:"width:100px;"                    
                },{
                    label:"shares",
                    align:"right",
                    field:"sum_shares_balance",
                    name:"sum_shares_balance",
                    style:"width:100px;"
                },{
                    label:"avg. price per order",
                    align:"right",
                    field:"avg_buy_price",
                    name:"avg_buy_price",
                    style:"width:100px;"    
                },{
                    label:"last price",
                    align:"right",
                    field:"last_price",
                    name:"last_price",
                    style:"width:100px;"                    
                },{
                    label:"market value",
                    align:"right",
                    field:"market_value",
                    name:"market_value",
                    style:"width:100px;"
                },{
                    label:"",
                    align:"left",
                    field:"",
                    name:""
                }
            ],            
            data:[]
        }
    },
    mounted:function(){
        this.get_list()
    },
    methods:{
        get_list:function(){
            this.$http.post(
            'holdings/HoldingsManager/get_list',{
            },postconfig()).then(httpresp =>{
                this.data = []
                this.$refs.msgbox.http_resp_on_error(httpresp)

                var appresp = httpresp.data
                if(appresp.success){                    
                    appresp.data.forEach(elem => {
                        elem.total_change = elem.total_change.toFixed(2)
                        elem.total_pl = elem.total_pl.toFixed(2)
                        elem.last_price = elem.last_price.toFixed(2)
                        elem.avg_buy_price = elem.avg_buy_price.toFixed(2)
                        elem.market_value = elem.market_value.toFixed(2)
                        this.data.push(elem)
                    })
                }
            })
        }
    }
}
</script>
