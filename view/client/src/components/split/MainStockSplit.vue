<template>
    <div>
        <q-toolbar>
            <q-btn class="q-ml-xs" color="blue-10" dense icon="menu" flat>
                <q-menu>
                    <q-list dense>
                        <q-item clickable v-close-popup :to="{name:'stocksplit-loader'}">
                            <q-item-section class="text-subtitle1">
                                <div>Carga de splits desde <span class="text-blue-10 text-bold">FMP</span></div>
                            </q-item-section>                            
                        </q-item>                        
                    </q-list>
                </q-menu>
            </q-btn>
            <q-toolbar-title class="text-blue-10">Stock Splits</q-toolbar-title>
        </q-toolbar>
        <div class="row q-col-gutter-xs q-pl-xs">
            <div class="col-4"  v-if="lpanel_visible==true">
                <router-view/>
            </div>
            <div class="col">
                <!--
                <q-toolbar>
                    <q-btn label="Nuevo" color="blue-10" class="text-capitalize" icon="add" :to="{name:'usuario-nuevo'}"/>
                </q-toolbar>
                -->
                <TableListStockSplit/>
            </div>
        </div>
    </div>
</template>
<script>
import split_store from "./split-store";

import TableListStockSplit from './TableListStockSplit.vue';

export default {
    name:"MainStockSplit",
    components:{
        TableListStockSplit
    },
    props:{

    },
    data () {
        return {
            lpanel_visible: false,
            split_store:split_store
        }
    },
    watch:{
        $route: function(){
            this.habilitar()
        }
    },
    mounted: function(){
        this.habilitar()
    },
    methods: {
        init: function(){
            this.habilitar()
            //this.st_table_list_stock_split.get_data()
        },
        habilitar: function(){
            if (this.$route.name == "stocksplit"){
                this.lpanel_visible = false
            }
            if (this.$route.name == "stocksplit-loader"){
                this.lpanel_visible = true
            }
            if (this.$route.name == "stocksplit-nuevo"){
                this.lpanel_visible = true
            }
            if (this.$route.name == "stocksplit-ver"){
                this.lpanel_visible = true
            }
            if (this.$route.name == "stocksplit-config"){
                this.lpanel_visible = true
            }
        }
    }
}
</script>