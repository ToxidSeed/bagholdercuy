<template>
    <div>
        <q-card flat>
            <q-toolbar class="text-blue-10 q-pb-none p-mb-none">
                <q-btn class="q-ml-xs" color="blue-10" dense icon="menu" flat>
                    <q-menu>
                        <q-list dense>
                            <!--
                            <q-item clickable v-close-popup :to="{name:'variacion-diaria-series-evolucion'}">
                                <q-item-section class="text-subtitle1  text-blue-10">
                                    <div>Candle Stick series diarias</div>                                    
                                </q-item-section>                            
                            </q-item>
                            <q-item clickable v-close-popup :to="{path:'/variaciondiaria'}">
                                <q-item-section class="text-subtitle1 text-blue-10">
                                    <div>Variacion Diaria</div>                                    
                                </q-item-section>                            
                            </q-item>
                            -->
                            <q-item v-for="item in routes" :key="item" :to="get_target(item)">
                                <q-item-section class="text-subtitle1  text-blue-10">
                                {{ item.label }}
                                </q-item-section>
                            </q-item>
                        </q-list>
                    </q-menu>
                </q-btn>
                <span class="text-h6 q-pr-md">
                    Variacion Diaria
                </span>      
                <q-btn flat round dense icon="search" @click="win_filtros_variacion_diaria.open=true"></q-btn>                          
            </q-toolbar>
        </q-card>
        <!--
        <q-card flat>
            <TableVariacionDiaria :indata="data"
            :symbol_value="symbol_value"
            :symbol_nombre="symbol_text"        
            >        
            </TableVariacionDiaria>
            <q-inner-loading :showing="loading">
                <q-spinner-gears size="50px" color="blue-10" />
            </q-inner-loading>
        </q-card>
        -->
        <router-view></router-view>
        <WinFiltrosVariacionDiaria
        v-model="win_filtros_variacion_diaria.open"
        v-on:btn-aceptar-click="filtrar"
        />
        <MessageBox v-bind:config="msgbox"/>
    </div>
</template>
<script>
//import TableVariacionDiaria from '@/components/informes/TableVariacionDiaria.vue'
import WinFiltrosVariacionDiaria from '@/components/informes/WinFiltrosVariacionDiaria.vue';
//import {postconfig} from '@/common/request.js';
import MessageBox from '../dialogs/MessageBox.vue';
import _ from "lodash"

export default {
    name:"PanelVariacionDiaria",
    components:{
        //TableVariacionDiaria,
        WinFiltrosVariacionDiaria,
        MessageBox
    },
    watch:{
        /*
        $route:function(newval){            
            if ( Object.keys(newval.query).length > 0){
                this.symbol_value = newval.query.cod_symbol
                this.get_variacion_diaria()
            }
        }
        */
    },
    mounted:function(){
        //this.init()
    },    
    data(){
        return {
            symbol_value:"",
            symbol_text:"",
            data:[],
            win_filtros_variacion_diaria:{
                open:false
            },
            msgbox:{},
            loading:false,
            routes:[
                {
                    name: 'variacion-diaria-series-evolucion',
                    label:'Candle Stick series diarias'
                },{
                    path: '/variaciondiaria',
                    label:'Variacion Diaria'
                }
            ]
        }
    },
    methods:{        
        get_target(route){
            if (_.has(route,"name")){
                return {name:route.name}
            }
            if (_.has(route,"path")){
                return {path:route.path}
            }
            return {}
        },
        get_label(route){
            return route.label
        },
        filtrar:function(filtros){            
            console.log(this.$router)
            this.symbol_value = filtros.symbol_value
            this.symbol_text = filtros.symbol_text                  
            console.log(this.$route)
            //this.$router.replace({name:"variacion-diaria", query:{cod_symbol:filtros.symbol_value, ts:new Date()}})
            this.$router.push({path:this.$route.path, query:{cod_symbol:filtros.symbol_value}})            
        }
    }
}
</script>