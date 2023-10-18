<template>
    <div >
        <q-toolbar class="text-blue-10">
            <q-btn flat round dense icon="menu"></q-btn>
            <q-toolbar-title>
                Holdings
            </q-toolbar-title>
        </q-toolbar>
        <q-splitter
            v-model="first_panel_size"
            :limits="[0,100]"
            style="height:100hr"
            >
            <template v-slot:before>
                <router-view
                v-on:open="open_handler"
                v-on:btn-close-click="close"
                :order_type="order.order_type"
                >                                    
                </router-view>
            </template>
            <template v-slot:after >
                <q-toolbar>
                    <q-btn color="blue-10" label="Buy" @click="comprar()"/>                
                    <q-btn color="red-10 " label="Sell" @click="vender()" class="q-ml-xs" />                
                    <!--<q-btn color="green" label="Options Chain" to="/order" class="q-ml-xs" />-->
                    <q-btn flat outline color="blue-10" class="q-ml-xs text-capitalize" icon="upload"
                    @click="WinCargaMultiple.open=true">Carga multiple</q-btn>
                    <q-btn flat outline color="blue-10" label="Reprocesar Ordenes" class="q-ml-xs text-capitalize" icon="sync"
                    @click="WinReprocesarOrdenes.open=true"
                    ></q-btn>
                </q-toolbar>
                <TableHoldings
                    v-on:vender="table_btn_vender_click"
                    v-on:comprar="table_btn_comprar_click"
                />
                <TablePosicionesOpcion class="q-pt-xs q-pb-xs"/>
            </template>
            <q-inner-loading :showing="progress">
                <q-spinner-gears size="50px" color="primary" />
            </q-inner-loading>
        </q-splitter>
        <MessageBox :config="MsgBox"/>
        <WinCargaMultiple v-model="WinCargaMultiple.open"/>
        <WinReprocesarOrdenes v-model="WinReprocesarOrdenes.open"/>
        <Confirmar v-model="Confirmar.show" 
        :config="Confirmar.config"
        v-on:confirmar-reprocesar="reprocesar"
        />
    </div>
</template>
<script>
import TableHoldings from '@/components/Holdings/TableHoldings.vue';
import TablePosicionesOpcion from '@/components/Holdings/TablePosicionesOpcion.vue';
import WinCargaMultiple from '@/components/Holdings/WinCargaMultiple.vue';
import WinReprocesarOrdenes from '@/components/Holdings/WinReprocesarOrdenes.vue';
import MessageBox from '@/components/MessageBox.vue';
import Confirmar from '@/components/dialogs/Confirmar.vue'
import {get_postconfig} from '@/common/request.js'

export default {
    name:"MainPanelHoldings",
    components:{
        //PanelTrade,
        //-->PanelResumen,
        //PanelOptionsChain,
        TableHoldings,
        TablePosicionesOpcion,
        WinCargaMultiple,
        WinReprocesarOrdenes,
        MessageBox,
        Confirmar 
    },
    props:{
        in_first_panel_size:{
            type:Number,
            default:0
        }
    },
    data:() =>{
        return {
            first_panel_size:0,
            order:{
                symbol:"",
                asset_type:"",
                order_type:"",
                update:""
            },
            panel_trade:{
                visible:false
            },            
            open_panel_order:false,
            WinCargaMultiple:{
                open:false
            },
            WinReprocesarOrdenes:{
                open:false
            },
            Confirmar:{
                show:false,
                config:{
                    title:"",
                    msg:"",
                    callback:""
                }                
            },
            MsgBox:{},
            progress:false            
        }
    },
    watch:{
        in_first_panel_size:function(newval){
            this.first_panel_size = newval
        },
        $route:function(){
            this.reload()
        }
    },
    computed:{
        resumen_visible:function(){
            return true
        }
    },
    mounted:function(){
        
    },
    methods:{        
        reload:function(){
            if (this.$route.name == 'holdings'){
                this.first_panel_size = 0
            }else{
                this.first_panel_size = 30
            }
        },
        buy:function(row){     
            this.order.symbol = ""            
            this.open_panel_order = true
            this.order.order_type = "B"
            
            this.order.update = new Date()            
            if (row != undefined){
                this.order.symbol = row.symbol
                this.order.asset_type = row.asset_type
            }else{
                this.order.asset_type = "stock"
            }
        },
        sell:function(row){           
            this.order.symbol = "" 
            this.open_panel_order = true
            this.order.order_type = "S"
            
            this.order.update = new Date()
            if (row != undefined){
                this.order.symbol = row.symbol
                this.order.asset_type = row.asset_type
            }else{
                this.order.asset_type = "stock"
            }
        },
        close:function(){
            this.$router.push({name:'holdings'})
        },
        open_handler:function(size){
            this.first_panel_size = size
        },
        table_btn_vender_click:function(){            
            this.order.order_type = 'S'
        },
        table_btn_comprar_click:function(){
            this.order.order_type = 'B'
        },
        confirmar_reproceso:function(){
            this.Confirmar = {
                show:true,
                config:{
                    title:"Confirmar",
                    msg:"Se van a reprocesar todas las ordenes, desea continuar?",
                    callback:"confirmar-reprocesar"
                }
            }
        },
        reprocesar:function(){
            this.progress = true
            let postconfig = get_postconfig()
            this.$http.post(
                '/OrdenManager/ReprocesadorManager/ejecutar',{},
                postconfig
            ).then(httpresp => {
                this.MsgBox = {
                    httpresp:httpresp
                }
            }).finally(() => {
                this.progress = false
            })
        }
    }
}
</script>