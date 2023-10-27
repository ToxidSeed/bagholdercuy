<template>
    <div>
        <q-table
            :data="data"
            :columns="columns"
            row-key="symbol_id"
            dense     
            :pagination="pagination"       
        >
        <template v-slot:top>
                <q-toolbar  class="text-blue-10">
                    <!--<q-btn flat round dense icon="menu"></q-btn>-->
                    <q-toolbar-title>Ticker symbols</q-toolbar-title>
                    <q-btn  flat dense icon="filter_alt" outline class="text-capitalize" @click="WinFiltrarSymbols.open = true">Filtros</q-btn>
                </q-toolbar>
                <!--<div class="text-h6">Opciones</div>-->
        </template>   
        </q-table>
        <WinFiltrarSymbols v-model="WinFiltrarSymbols.open" v-on:btn-aceptar-click="get_list"/>
    </div>
</template>
<script>
import {get_postconfig} from '@/common/request.js'
import WinFiltrarSymbols from '@/components/Symbol/WinFiltrarSymbols.vue';
export default {
    name:"TableSymbol",
    components:{
        WinFiltrarSymbols
    },
    data: () => {
        return {
            pagination:{
                rowsPerPage:20
            },
            columns:[{
                label:"ID",
                aling:"left",
                field:"id",
                name:"id"
            },{
                label:"Symbol",
                align:"left",
                name:"symbol",
                field:"symbol"
            },{
                label:"Name",
                align:"left",
                name:"name",
                field:"name"
            },{
                label:"Region",
                align:"left",
                name:"region",
                field:"region"
            },{
                label:"Exchange",
                align:"left",
                name:"exchange",
                field:"exchange"
            },{
                label:"Asset Type",
                align:"left",
                name:"asset_type",
                field:"asset_type"
            }],
            data:[],
            WinFiltrarSymbols:{
                open:false
            }
        }
    },
    mounted:function(){        
        this.get_list({})
    },
    methods:{        
        get_list:function(filtros){
            this.$http.post('SymbolManager/SymbolFinder/get_list',{
                id_symbol: filtros.id_symbol
            },get_postconfig()).then(httpresponsse => {
                var appdata = httpresponsse.data
                this.data = appdata.data
            })
        }
    }
}
</script>