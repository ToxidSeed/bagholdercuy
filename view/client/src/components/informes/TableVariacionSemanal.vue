<template>
    <q-table
        :data="data"
        :columns="columns"        
        row-key="fch_serie"
        dense
        :pagination="pagination"       
        separator="vertical" 
    >
        <template v-slot:header>
            <q-tr>
                <q-th class="text-left" style="width:50px;">Año</q-th>
                <q-th class="text-left" style="width:50px;">Fecha</q-th>
                <q-th class="text-left" style="width:50px;">semana</q-th>
                <q-th class="text-right" style="width:50px;">open</q-th>
                <q-th class="text-right" style="width:50px;">high</q-th>
                <q-th class="text-right" style="width:50px;">low</q-th>
                <q-th class="text-right" style="width:50px;">close</q-th>
                <q-th class="text-right" style="width:50px;">% high</q-th>
                <q-th class="text-right" style="width:50px;">% low</q-th>
                <q-th class="text-right" style="width:50px;">% close</q-th>
                <q-th class="text-right" style="width:50px;">Var. high</q-th>
                <q-th class="text-right" style="width:50px;">Var. low</q-th>
                <q-th class="text-right" style="width:50px;">Var. high-low</q-th>
                <q-th class="text-right" style="width:50px;">Var. close</q-th>
                <q-th class="text-left"></q-th>
            </q-tr>
        </template>
        <template v-slot:body="props">            
            <q-tr :props="props">
                <q-td key="anyo"  class="text-left">
                    {{props.row.anyo}}
                </q-td>
                <q-td key="fch_semana"  class="text-left">
                    {{props.row.fch_semana}}
                </q-td>
                <q-td key="semana" class="text-left">
                    {{props.row.semana}}
                </q-td>
                <q-td key="open" class="text-right">
                    {{props.row.open}}
                </q-td>
                <q-td key="high" class="text-right">
                    {{props.row.high}}
                </q-td>
                <q-td key="low" class="text-right">
                    {{props.row.low}}
                </q-td>
                <q-td key="close" class="text-right">
                    {{props.row.close}}
                </q-td>
                <q-td key="pct_high" class="text-right">
                    {{props.row.pct_high}}
                </q-td>
                <q-td key="pct_low" class="text-right">
                    {{props.row.pct_low}}
                </q-td>
                <q-td key="pct_close" v-bind:class="{'text-red':props.row.pct_close < 0,'text-green':props.row.pct_close >= 0,'text-right':true}">                    
                    {{props.row.pct_close}}
                </q-td>
                <q-td key="var_high" class="text-right">
                    {{props.row.var_high}}
                </q-td>
                <q-td key="var_low" class="text-right">
                    {{props.row.var_low}}
                </q-td>
                <q-td key="high_low" class="text-right">
                    {{props.row.var_high_low}}
                </q-td>
                <q-td key="var_close"  v-bind:class="{'bg-red':props.row.var_close < 0,'bg-green':props.row.var_close >= 0,'text-right':true,'text-white':true}">
                    {{props.row.var_close}}
                </q-td>
                <q-td>                    
                </q-td>
            </q-tr>
        </template>
    </q-table>
</template>
<script>
import date from 'date-and-time'
import {CLIENT_DATE_FORMAT, ISO_DATE_FORMAT} from '@/common/constants.js'
export default {
    name:"TableVariacionSemanal",
    data: () => {
        return {
            filter:{
                symbol:"SOXL"
            },
            pagination:{
                rowsPerPage:24
            },
            data:[],            
            columns:[
                {
                    label:"Año",
                    align:"left",
                    field:"anyo",
                    name:"anyo",
                    style:"width:50px;"
                },{
                    label:"Semana",
                    align:"left",
                    field:"semana",
                    name:"semana",
                    style:"width:50px;"
                },{
                    label:"open",
                    align:"right",
                    field:"open",
                    name:"open",
                    style:"width:50px;"
                },{
                    label:"high",
                    align:"right",
                    field:"high",
                    name:"high",
                    style:"width:50px;"
                },{
                    label:"low",
                    align:"right",
                    field:"low",
                    name:"low",
                    style:"width:50px;"
                },{
                    label:"close",
                    align:"right",
                    field:"close",
                    name:"close",
                    style:"width:50px;"
                },{
                    label:"% high",
                    align:"right",
                    field:"pct_high",
                    name:"pct_high",
                    style:"width:50px;"
                },{
                    label:"% low",
                    align:"right",
                    field:"pct_low",
                    name:"pct_low",
                    style:"width:50px;"
                },{
                    label:"% close",
                    align:"right",
                    field:"pct_close",
                    name:"pct_close",
                    style:"width:50px;",
                    class:row => (row.pct_close > 0.00 ? 'bg-green' : 'bg-yellow')
                },{
                    label:"Var. High",
                    align:"right",
                    field:"var_high",
                    name:"var_high",
                    style:"width:50px;"
                },{
                    label:"Var. Low",
                    align:"right",
                    field:"var_low",
                    name:"var_low",
                    style:"width:50px;"
                },{
                    label:"Var. close",
                    align:"right",
                    field:"var_close",
                    name:"var_close",
                    style:"width:50px;"
                },{
                    label:"",
                    align:"",
                    field:"",
                    name:"",
                    style:""
                }
            ]
        }
    },
    mounted:function(){
        this.get_variacion_semanal()
    },
    methods:{
        get_variacion_semanal:function(){
            this.data = []
            this.$http.post('/informe/InformeStockController/get_variacion_semanal',{
                symbol:this.filter.symbol
            }).then(httpresp => {
                    let appresp = httpresp.data
                    console.log(appresp)
                    if(appresp.success==false){
                        return
                    }else{
                        let data = appresp.data
                        data.forEach(element => {
                            element.fch_semana = date.transform(element.fch_semana,ISO_DATE_FORMAT,CLIENT_DATE_FORMAT)
                            element.open = element.open.toFixed(2)
                            element.high = element.high.toFixed(2)
                            element.low = element.low.toFixed(2)
                            element.close = element.close.toFixed(2)                            
                            element.pct_high = element.pct_high.toFixed(2)
                            element.pct_low = element.pct_low.toFixed(2)
                            element.pct_close = element.pct_close.toFixed(2)
                            element.var_high = element.var_high.toFixed(2)
                            element.var_low = element.var_low.toFixed(2)
                            element.var_high_low = element.var_high_low.toFixed(2)
                            element.var_close = element.var_close.toFixed(2)
                            this.data.push(element)
                        }); 
                    }
                }
            )
        }
    }
}
</script>