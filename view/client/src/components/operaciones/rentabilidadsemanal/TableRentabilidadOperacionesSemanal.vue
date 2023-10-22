<template>
    <div>
        <q-table        
            :data="data"
            :columns="columns"
            row-key="name"
            dense
            separator="vertical"
            :pagination="pagination"
        >
            
        </q-table>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import {postconfig} from '@/common/request.js';
import MessageBox from '@/components/MessageBox.vue';

export default {
    name:"TableRentabilidadOperacionesSemanal",
    components:{
        MessageBox
    },
    data(){
        return {            
            data:[],
            columns:[
                {
                    name: 'desc_semana_transaccion',                    
                    label: 'Semana transaccion',
                    align: 'left',                    
                    field: "desc_semana_transaccion"
                },
                {
                    name: 'imp_rentabilidad',                    
                    label: 'Imp. Rentabilidad',
                    align: 'right',                    
                    field: "imp_rentabilidad"
                }
            ],
            pagination:{
                rowsPerPage:16
            }
        }
    },
    mounted:function(){
        this.get_rentabilidad_semanal()
    },
    methods:{
        get_rentabilidad_semanal:function(){
            this.$http.post(
                "/operacion/OperacionManager/get_rentabilidad_semanal",{
                    id_cuenta: localStorage.getItem("id_cuenta"),
                    flg_ascendente: false
                },postconfig()
            ).then(httpresp => {
                this.$refs.msgbox.http_resp_on_error(httpresp)

                let records = httpresp.data.data
                this.data = []
                for (let element of records){           
                    element.imp_rentabilidad = element.imp_rentabilidad.toFixed(2)         
                    this.data.push(element)
                }                
            })
        }
    }
}
</script>