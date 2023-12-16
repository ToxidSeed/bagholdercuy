<template>
    <div>
        <q-table
            :data="data"
            row-key="valor"
            dense
            separator="vertical"
        >
            <template v-slot:header>
                <q-tr>
                    <q-th class="text-left">valor</q-th>
                    <q-th class="text-center">{{headers.fch_lunes}}</q-th>
                    <q-th class="text-center">{{headers.fch_martes}}</q-th>
                    <q-th class="text-center">{{headers.fch_miercoles}}</q-th>
                    <q-th class="text-center">{{headers.fch_jueves}}</q-th>
                    <q-th class="text-center">{{headers.fch_viernes}}</q-th>
                </q-tr>
            </template>
            <template v-slot:body="props">
                <q-tr :props="props">
                    <q-td key="valor">
                        {{props.row.valor}}
                    </q-td>
                    <q-td key="imp_lunes" :class="{'text-right':true,'bg-green':props.row.dia_max == 1, 'bg-red':props.row.dia_min == 1,'text-white': props.row.dia_max == 1 ||  props.row.dia_min == 1}">
                        {{ props.row.imp_lunes }}
                    </q-td>
                    <q-td key="imp_martes" :class="{'text-right':true,'bg-green':props.row.dia_max == 2, 'bg-red':props.row.dia_min == 2,'text-white': props.row.dia_max == 2 ||  props.row.dia_min == 2}">
                        {{ props.row.imp_martes }}
                    </q-td>
                    <q-td key="imp_miercoles" :class="{'text-right':true,'bg-green':props.row.dia_max == 3, 'bg-red':props.row.dia_min == 3,'text-white': props.row.dia_max == 3 ||  props.row.dia_min == 3}">
                        {{ props.row.imp_miercoles }}
                    </q-td>
                    <q-td key="imp_jueves" :class="{'text-right':true,'bg-green':props.row.dia_max == 4, 'bg-red':props.row.dia_min == 4,'text-white': props.row.dia_max == 4 ||  props.row.dia_min == 4}">
                        {{ props.row.imp_jueves }}
                    </q-td>
                    <q-td key="imp_viernes" :class="{'text-right':true,'bg-green':props.row.dia_max == 5, 'bg-red':props.row.dia_min == 5,'text-white': props.row.dia_max == 5 ||  props.row.dia_min == 5}">
                        {{ props.row.imp_viernes }}
                    </q-td>
                </q-tr>
            </template>
        </q-table>
        <MessageBox :config="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue';
import {postconfig} from '@/common/request.js';

export default {
    name:"TableEvolucionSemanal",
    components:{
        MessageBox
    },
    props:{
        infiltros:{

        }
    },
    data(){
        return {
            data:[],
            headers:{},
            msgbox:{},
            filtros:{
                symbol:"",
                anyo:"",
                semana:""
            }
        }
    },
    mounted:function(){
        this.init()
    },
    watch:{
        $route: function(to){
            console.log(to)
            if (Object.keys(to.query).length > 0){         
                this.filtrar(to.query)
            }
        }
    },
    methods:{
        init:function(){
            this.filtrar(this.$route.query)
        },
        filtrar:function(params){
            this.data = []
            this.headers = {}

            this.$http.post('/reportes/EvolucionSemanalSeries/build',{
                symbol: params.cod_symbol,
                anyo: params.anyo,
                semana: params.semana
            },
            postconfig()
            ).then(httpresp => {                
                this.msgbox = {
                    httpresp: httpresp,
                    onerror:true
                }

                let appdata = httpresp.data.data 
                this.headers = appdata.semana
                            
                appdata.series.forEach(element => {
                    element.imp_lunes = element.imp_lunes.toFixed(2)
                    element.imp_martes = element.imp_martes.toFixed(2)
                    element.imp_miercoles = element.imp_miercoles.toFixed(2)
                    element.imp_jueves = element.imp_jueves.toFixed(2)
                    element.imp_viernes = element.imp_viernes.toFixed(2)
                    this.data.push(element)
                })
            })
        }
    }
}
</script>