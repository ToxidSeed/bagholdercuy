<template>
    <div>
        <q-table :data="data" :columns="columns" row-key="id_symbol" dense :pagination="pagination" flat :loading="loading">
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
            <template v-slot:body-cell-conid="props">
                <q-td :props="props">
                    <div v-if="props.row.conid" class="row items-center justify-center no-wrap">
                        <q-chip
                            dense
                            outline
                            color="blue-10"
                            text-color="blue-10"
                            icon="verified"
                            class="text-weight-medium q-ma-none"
                        >
                            {{ props.row.conid }}
                            <q-tooltip v-if="props.row.ibkr_exchange">
                                Exchange IBKR: {{ props.row.ibkr_exchange }}
                            </q-tooltip>
                        </q-chip>
                        <q-btn
                            flat
                            round
                            dense
                            size="xs"
                            icon="sync"
                            color="grey-6"
                            class="q-ml-xs"
                            :loading="props.row._loading_ibkr === true"
                            @click.stop="sincronizar_ibkr(props.row)"
                        >
                            <q-tooltip>Re-sincronizar con IBKR</q-tooltip>
                        </q-btn>
                    </div>
                    <q-btn
                        v-else
                        flat
                        dense
                        size="sm"
                        no-caps
                        color="blue-10"
                        icon="sync"
                        label="Sincronizar"
                        :loading="props.row._loading_ibkr === true"
                        @click.stop="sincronizar_ibkr(props.row)"
                    >
                        <q-tooltip>Buscar y vincular contrato en Interactive Brokers</q-tooltip>
                    </q-btn>
                </q-td>
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
import Ibkr from '@/api/ibkr.js';

export default {
    name:"TableSymbol",
    components:{
        WinFiltrarSymbols,
        WinGestionSymbol,
        ConfirmCargaMultiple
    },
    data: () => {
        return {
            loading: false,
            pagination:{
                rowsPerPage:20
            },
            symbolStore:symbolStore,
            columns:[{
                label:"ID",
                align:"left",
                field:"id_symbol",
                name:"id_symbol",
                sortable: true
            },{
                label:"Symbol",
                align:"left",
                name:"symbol",
                field:"symbol",
                sortable: true
            },{
                label:"Name",
                align:"left",
                name:"name",
                field:"name",
                sortable: true
            },{
                label:"Region",
                align:"left",
                name:"region",
                field:"region",
                sortable: true
            },{
                label:"Exchange",
                align:"left",
                name:"exchange",
                field:"exchange",
                sortable: true
            },{
                label:"Asset Type",
                align:"left",
                name:"asset_type",
                field:"asset_type",
                sortable: true
            },{
                label:"IBKR ConID",
                align:"center",
                name:"conid",
                field:"conid",
                sortable: true
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
        get_list:function(filtros = {}){            
            this.loading = true
            this.$http.post('SymbolManager/SymbolFinder/get_list',{
                id_symbol: filtros.id_symbol,
                cod_symbol: filtros.cod_symbol,
                name: filtros.name
            },get_postconfig()).then(httpresp => {                
                this.$store.commit("message", {"httpresp":httpresp,"mostrar_si_error":true})
                var appdata = httpresp.data
                this.data = appdata.data
            }).catch(error => {
                console.error("Error al consultar symbols:", error)
            }).then(() => {
                this.loading = false
            })
        },
        sincronizar_ibkr: function(row) {
            this.$set(row, '_loading_ibkr', true)
            Ibkr.sync_contract({
                id_symbol: row.id_symbol,
                cod_symbol: row.symbol,
                exchange: row.exchange
            }).then(httpresp => {
                const res = httpresp.data
                const data = (res && res.data) ? res.data : res
                if (data && data.conid) {
                    this.$set(row, 'conid', data.conid)
                    this.$set(row, 'ibkr_exchange', data.exchange)
                    this.$q.notify({
                        type: 'positive',
                        message: `${row.symbol}: Contrato vinculado con éxito (ConID ${data.conid})`,
                        timeout: 3000
                    })
                } else {
                    this.$q.notify({
                        type: 'warning',
                        message: (res && res.message) || `No se pudo obtener el contrato para ${row.symbol}`,
                        timeout: 3500
                    })
                }
            }).catch(error => {
                console.error("Error al sincronizar contrato IBKR:", error)
                const msg = error.response && error.response.data && error.response.data.message
                    ? error.response.data.message
                    : (error.message || "Error al conectar con Interactive Brokers")
                this.$q.notify({
                    type: 'negative',
                    message: msg,
                    timeout: 4000
                })
            }).finally(() => {
                this.$set(row, '_loading_ibkr', false)
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