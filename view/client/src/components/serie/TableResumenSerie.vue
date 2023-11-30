<template>
    <div>
        <q-table
            :columns="columns"
            :data="data"
            :pagination="pagination"
            row-key="symbol_id"
            separator="vertical"
            dense
        >
            <template v-slot:body-cell-estado="props">
                <q-td :props="props">
                    {{ props.row.estado }}
                    <q-menu
                    touch-position
                    context-menu
                    >
                        <q-list dense>
                            <q-item clickable v-close-popup>
                                <q-item-section><span><q-icon name="update" color="green" style="font-size: 1.4em;" class="q-pr-xs"></q-icon>Actualizar</span></q-item-section>
                            </q-item>
                        </q-list>
                    </q-menu>                    
                </q-td>
            </template>
        </q-table>

    </div>
</template>
<script>
import {postconfig} from '@/common/request.js'


export default {
    name:"TableResumenSerie",
    components:{
        
    },
    data: () => {
        return {
            columns:[{
                label:"Symbol",
                align:"left",   
                name:"cod_symbol",
                style:"width:100px",
                field:"cod_symbol"
            },{
                label:"Fch. ultima serie",
                align:"left",
                name:"fch_serie",
                style:"width:100px",
                field:"fch_serie"
            },{
                label:"Num. dias desde ultima serie",
                align:"right",
                name:"num_dias_desde_ultima_serie",
                style:"width:100px",
                field:"num_dias_desde_ultima_serie"
            },{
                label:"Estado",
                align:"left",
                name:"estado",
                style:"width:100px",
                field:"estado",
                classes: row => {
                    if (row.estado == 'Desactualizado'){
                        return 'text-red'
                    }else{
                        return 'text-green'
                    }                    
                }
            },{
                label:"",
                align:"",
                name:"",
                field:""
            }],
            data:[],
            pagination:{
                rowsPerPage:20
            }
        }
    },
    mounted:function(){
        this.get_lista_fechas_maximas_x_symbol()
    },
    methods:{
        get_lista_fechas_maximas_x_symbol:function(){
            this.$http.post(
                "/SerieManager/SerieController/get_lista_fechas_maximas_x_symbol",{},
                postconfig()
            ).then(httpresp => {
                this.$store.commit("messagebox",{"httpresp":httpresp,"mostrar_si_error":true}) 
                let appdata = httpresp.data
                this.data = appdata.data
            })
        },
        actualizar_series:function(row){
            this.$http.post("/",{
                id_symbol: row.id_symbol
            },postconfig()
            ).then(httpresp => {
                this.$store.commit("messagebox",{"httpresp":httpresp}) 
                this.get_lista_fechas_maximas_x_symbol()
            })
        }
    }
}
</script>