<template>
    <!--<div v-if="asset_type=='options'">-->
    <div>           
        <div class="row q-pa-sm">
            <div class="col-12">
                <q-input style="max-width:350px;" stack-label label="Contrato"
                    v-model="filter.contract"
                    @input="get_options_chain"
                >
                </q-input>
            </div>
            <div class="col-12 row">
                <div class="col-6" style="max-width:350px;">
                    <SelectSymbol 
                        v-on:select-symbol="select_symbol"                        
                    />
                    <div class="text-h6 text-weight-bold">{{filter.symbol.value}}</div>
                    <div>{{filter.symbol.name}}</div>
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
                            <q-icon name="arrow_drop_down" class="cursor-pointer">
                                <q-popup-proxy :offset=[150,15] v-model="show_sel_exp">                         
                                    <q-list bodered separator dense>
                                        <q-item v-for="elem in exp_dates" :key="elem" clickable v-ripple:purple style="width:150px;" @click="sel_exp_date(elem)">
                                            <q-item-section>{{elem}}</q-item-section>
                                        </q-item>
                                    </q-list>                        
                                </q-popup-proxy>
                            </q-icon>
                        </template>                                                                        
                    </q-input>                                
                </div>            
                <q-input class="col-3 q-pl-xs"
                label="Strike"
                v-model="filter.strike"                  
                mask="#####"
                input-class="text-right"
                debounce="500"
                @input="get_options_chain"            
                >
                    <template v-slot:after>
                        <q-icon name="arrow_drop_down" class="cursor-pointer">
                            <q-popup-proxy :offset=[150,15] v-model="show_sel_strikes">
                                <q-list bordered separator dense>
                                    <q-item v-for="elem in strikes" :key="elem" clickable style="width:150px;" @click="sel_strike(elem)">
                                        <q-item-section>{{elem}}</q-item-section>
                                    </q-item>
                                </q-list>
                            </q-popup-proxy>
                        </q-icon>
                    </template>
                </q-input>
            </div> 
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
                        <q-tr :props="props" @dblclick="sel_contract(props.row.symbol)" class="cursor-pointer">
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
                    <q-tr :props="props"  @dblclick="sel_contract(props.row.symbol)" class="cursor-pointer">
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
import date from '@/common/date.js'

export default {
    name:"PanelOptionsChain",
    props:{
        asset_type:{
            type:String,
            default:""
        },
        symbol_val:{
            type:String,
            default:""
        },
        contract:{
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
                symbol:{
                    value:"",
                    name:""
                },
                expiration_date:"",
                strike:"",
                contract:""
            },
            calls:[],
            puts:[],
            exp_dates:[],
            strikes:[],
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
            show_sel_exp:false,
            show_sel_strikes:false
        }        
    },
    mounted:function(){
        let search = false
        if (this.symbol_val != ""){
            this.filter.symbol.value = this.symbol_val
            search = true
            this.get_datos_symbol(this.symbol_val)
        }
        /*if (this.contract != ""){
            this.filter.contract = this.contract
            search = true
        }*/
        if (search == true){
            this.get_options_chain()
        }
    },
    methods:{        
        select_symbol:function(selected){     
            console.log(this.filter.symbol)
            console.log(selected)       
            this.filter.symbol.value = selected.value
            this.filter.symbol.name = selected.label
            //refresh data
            
            this.get_options_chain();
        },
        sel_exp_date:function(selected){            
            this.show_sel_exp = false
            this.filter.expiration_date = date.iso_to_format(selected,"DD/MM/YYYY")     
            this.get_options_chain()  
        },
        sel_strike:function(selected){
            this.show_sel_strikes = false
            this.filter.strike = selected
            this.get_options_chain()
        },
        sel_contract:function(symbol){
            this.$emit('sel-contract',symbol)
        },
        input_expiration_date:function(){
            console.log(this.filter.expiration_date)
            if (this.filter.symbol ==""){
                return
            }
            var iexdate = new Date(date.format_to_iso(this.filter.expiration_date,"DD/MM/YYYY"))
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
            console.log("xxx")
            console.log(this.filter)
            /*console.log('get_options_chain') 
            console.log(this.filter)       */
            if (this.filter.symbol.value == "" && this.filter.contract == ""){
                console.log(this.filter)
                return;
            }

            let exp_date = ""
            if (this.filter.expiration_date != ""){
                 exp_date = date.format_to_iso(this.filter.expiration_date,"DD/MM/YYYY")
            }    
            
            this.$http.post("OpcionesContratoManager/OpcionesContratoManager/get_options_chain",{
                contract: this.filter.contract,
                symbol:this.filter.symbol.value,
                expiration_date:exp_date,
                strike:this.filter.strike
            }).then(httpresponse => {
                var appresponse = httpresponse.data
                var appdata = appresponse.data
                this.calls = appdata["calls"]
                this.puts = appdata["puts"]
                this.exp_dates = appdata["exp_dates"]
                this.strikes = appdata["strikes"]
            })
        },
        get_datos_symbol:function(symbol){
            this.$http.post('SymbolManager/SymbolFinder/get_datos_symbol',{
                symbol:symbol
            }).then(httpresp => {
                let appresp = httpresp.data
                let appdata = appresp.data
                console.log(appdata)
                this.filter.symbol.value = appdata.symbol
                this.filter.symbol.name = appdata.name
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