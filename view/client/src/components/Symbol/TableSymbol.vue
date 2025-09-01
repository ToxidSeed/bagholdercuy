<template>
    <div>
        <q-table :data="data" :columns="columns" row-key="symbol_id" dense :pagination="pagination" flat>
            <template v-slot:top>
                <!--
                <q-toolbar  class="text-blue-10">
                    <q-toolbar-title>Ticker symbols</q-toolbar-title>
                    <q-btn  flat dense icon="filter_alt" outline class="text-capitalize" @click="WinFiltrarSymbols.open = true">Filtros</q-btn>
                </q-toolbar>
                -->
                <div class="row">
                    <div class="col-12 q-pt-md text-h5 text-blue-10">Symbols</div>
                    <div class="col-12">
                        <q-bar class="bg-white">
                            <q-btn flat dense color="blue-10" icon="add" @click="btnNuevoClick">Nuevo</q-btn>
                            <q-btn flat dense color="blue-10" icon="keyboard_double_arrow_up" @click="btnCargaMultipleClick">Carga Multiple</q-btn>
                            <q-btn flat dense icon="search" outline @click="winFiltrarSymbols.open = true"
                                color="blue-10">Buscar</q-btn>
                        </q-bar>
                    </div>
                </div>
            </template>
        </q-table>
        <WinFiltrarSymbols v-model="winFiltrarSymbols.open" v-on:btn-aceptar-click="get_list" />
        <WinGestionSymbol 
            v-model="symbolStore.state.winGestionSymbol.open"
            :proceso="symbolStore.state.winGestionSymbol.proceso" 
        />
        <ConfirmCargaMultiple v-model="confirmCargaMultipleOpen" @ejecutar="ejecutarCargaMultiple"/>
    </div>
</template>
<script>
import {get_postconfig} from '@/common/request.js'
import WinFiltrarSymbols from '@/components/Symbol/WinFiltrarSymbols.vue';
import WinGestionSymbol from './WinGestionSymbol.vue';
import ConfirmCargaMultiple from './ConfirmCargaMultiple.vue';
import symbolStore from './symbol-store';

export default {
    name:"TableSymbol",
    components:{
        WinFiltrarSymbols,
        WinGestionSymbol,
        ConfirmCargaMultiple
    },
    data: () => {
        return {
            pagination:{
                rowsPerPage:20
            },
            symbolStore:symbolStore,
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
            winFiltrarSymbols:{
                open:false
            },
            confirmCargaMultipleOpen:false
        }
    },
    mounted:function(){        
        this.get_list({})
    },
    methods:{        
        get_list:function(filtros){            
            this.$http.post('SymbolManager/SymbolFinder/get_list',{
                id_symbol: filtros.id_symbol,
                cod_symbol: filtros.cod_symbol
            },get_postconfig()).then(httpresp => {                
                this.$store.commit("message", {"httpresp":httpresp,"mostrar_si_error":true})
                var appdata = httpresp.data
                this.data = appdata.data
            })
        },
        btnNuevoClick: function(){
            this.symbolStore.state.winGestionSymbol.open = true
            this.symbolStore.state.winGestionSymbol.proceso = "NUEVO"
        },
        btnCargaMultipleClick:function(){
            this.confirmCargaMultipleOpen = true            
        },
        ejecutarCargaMultiple:function(){
            this.loading=true
            this.$http.post('/SymbolManager/DataLoader/do')
            .then(httpresp => {                
                this.$refs.msgbox.httpresp(httpresp)
            }).catch(error => {
                console.log(error)
            }).then(() => {
                this.loading = false
            })
        }        
    }
}
</script>