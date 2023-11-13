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
        </q-table>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import {postconfig} from '@/common/request.js'
import MessageBox from '@/components/MessageBox.vue'

export default {
    name:"TableResumenSerie",
    components:{
        MessageBox
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
                this.$refs.msgbox.http_resp_on_error(httpresp)
                let appdata = httpresp.data
                this.data = appdata.data
            })
        }
    }
}
</script>