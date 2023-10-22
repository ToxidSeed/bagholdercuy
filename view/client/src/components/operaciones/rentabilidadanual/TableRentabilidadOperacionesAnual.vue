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
    name:"TableRentabilidadOperacionesAnual",
    components:{
        MessageBox
    },
    data(){
        return {            
            data:[],
            columns:[
                {
                    name: 'anyo_transaccion',                    
                    label: 'Anyo',
                    align: 'left',                    
                    field: "anyo_transaccion"
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
        this.get_rentabilidad_anual()
    },
    methods:{
        get_rentabilidad_anual:function(){
            this.$http.post(
                "/operacion/OperacionManager/get_rentabilidad_anual",{
                    id_cuenta: localStorage.getItem("id_cuenta"),
                    orden_resultados:"desc"
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