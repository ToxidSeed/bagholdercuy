<template>
    <!--<div v-if="asset_type=='options'">-->
    <div>           
        <div class="row q-pa-sm">
            <div class="col-6" style="max-width:350px;">
                <SelectSymbol v-on:select-symbol="select_symbol"/>
            </div>
            <div class="col-3 q-pl-xs">
                <q-input class="col-6"
                v-model="filter.expiration_date"                  
                stack-label label="expiration date" 
                mask="##/##/####" 
                fill-mask="#" 
                hint="format: dd/mm/yyyy"
                debounce="1000"                 
                @input="input_expiration_date"                
                >
                    <template v-slot:after>
                        <q-icon name="arrow_drop_down" class="cursor-pointer" v-on:click="show_sel_exp=true"/>
                    </template>                    
                    <q-popup-proxy v-model="show_sel_exp">                        
                        <q-list bodered separator dense>
                            <q-item v-for="elem in exp_dates" :key="elem" clickable v-ripple style="width:150px;">
                                <q-item-section>{{elem}}</q-item-section>
                            </q-item>
                        </q-list>                        
                    </q-popup-proxy>                    
                </q-input>
            </div>
            <q-input class="col-3 q-pl-xs"
            label="Strike"
            v-model="filter.strike"                  
            type="number"
            input-class="text-right"
            debounce="500"
            @input="input_strike"            
            >
            </q-input> 
        </div>
        <div class="row">
            <div class="col-6">
                <q-table
                dense
                title="CALLS"
                :data="calls"
                :columns="call_columns"
                row-key="name"
                :pagination="pagination"  
                separator="vertical"              
                >
                    <template v-slot:body="props">                        
                        <q-tr :props="props">
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
                            <q-td key="symbol" :props="props" style="width:30px">
                            {{props.row.symbol}}
                            </q-td>
                            <q-td style="width:30px">
                                {{props.row.strike}}
                            </q-td>
                            <q-td style="width:30px">
                                {{props.row.expiration_date}}
                            </q-td>
                            <q-td>
                            </q-td>
                        </q-tr>
                    </template>
                </q-table>
            </div>
            <div class="col-6">
                <q-table
                dense
                title="PUTS"
                :data="puts"
                :columns="put_columns"
                row-key="name"
                :pagination="pagination"
                separator="vertical"
                >
                    <template v-slot:body="props">
                    <q-tr :props="props">
                        <q-menu
                        touch-position
                        context-menu
                        >
                        <q-list dense style="min-width: 100px">
                            <q-item clickable v-close-popup @click="buy(props.row)">
                                <q-item-section>Buy</q-item-section>                                    
                            </q-item>
                            <q-item clickable v-close-popup @click="sell(props.row)">
                                <q-item-section>Sell</q-item-section>                                    
                            </q-item>
                        </q-list>
                        </q-menu>
                        <q-td key="symbol" :props="props" style="width:30px">
                        {{props.row.symbol}}
                        </q-td>
                        <q-td style="width:30px">
                            {{props.row.strike}}
                        </q-td>
                        <q-td style="width:30px">
                            {{props.row.expiration_date}}
                        </q-td>
                        <q-td>
                        </q-td>
                    </q-tr>
                    </template>
                </q-table>
            </div>
        </div>        
    </div>
</template>
<script>
import SelectSymbol from './SelectSymbol.vue'

export default {
    name:"PanelOptionsChain",
    props:{
        asset_type:{
            type:String,
            default:""
        }
    },
    components:{
        SelectSymbol
    },
    data:() => {
        return {
            filter:{
                symbol:"",
                expiration_date:"",
                strike:""
            },
            calls:[],
            puts:[],
            exp_dates:[],
            call_columns:[{
                align:"left",
                name:"symbol",
                label:"symbol",
                field:"symbol"
            },{
                align:"left",
                name:"strike",
                label:"strike",
                field:"strike"
            },{
                align:"left",
                name:"expiration",
                label:"expiration date",
                field:"expiration_date"
            }],
            put_columns:[{
                align:"left",
                name:"symbol",
                label:"symbol",
                field:"symbol"
            },{
                align:"left",
                name:"strike",
                label:"strike",
                field:"strike"
            },{
                align:"left",
                name:"expiration",
                label:"expiration date",
                field:"expiration_date"
            }],
            pagination:{
                rowsPerPage:20
            },
            show_sel_exp:false
        }        
    },
    mounted:function(){
        if (this.filter.symbol != ""){
            this.get_options_chain()
        }        
    },
    methods:{
        select_symbol:function(selected){            
            this.filter.symbol = selected.value

            //refresh data
            this.get_options_chain();
        },
        sel_exp_date:function(selected){
            this.show_sel_exp = false
            this.filter.expiration_date = selected            
        },
        input_expiration_date:function(){
            console.log(this.filter.expiration_date)
            if (this.filter.symbol ==""){
                return
            }
            var iexdate = new Date(this.filter.expiration_date)
            if (iexdate == "Invalid Date")
                return

            this.get_options_chain()
        },
        input_strike:function(){
            if (this.filter.symbol ==""){
                return
            }
            this.get_options_chain()
        },
        get_options_chain:function(){            
            if (this.filter.symbol == ""){
                return;
            }
            
            this.$http.post("OpcionesContratoManager/OpcionesContratoManager/get_options_chain",{
                symbol:this.filter.symbol,
                expiration_date:this.filter.expiration_date,
                strike:this.filter.strike
            }).then(httpresponse => {
                var appresponse = httpresponse.data
                var appdata = appresponse.data
                this.calls = appdata["calls"]
                this.puts = appdata["puts"]
                this.exp_dates = appdata["exp_dates"]
            })
        },
        buy:function(data){    
            data["trade_type"] = "B"
            this.$emit("option-select",data)
        },
        sell:function(data){   
            console.log(data) 
            data["trade_type"] = "S"
            this.$emit("option-select",data)
        }
    }
}
</script>