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
        <MessageBox :config="msgbox"/>
    </div>
</template>
<script>
import {postconfig} from '@/common/request.js';
import MessageBox from '@/components/MessageBox.vue';

export default {
    name:"TableRentabilidadOperacionesDiaria",
    components:{
        MessageBox
    },
    data(){
        return {
            msgbox:{},            
            data:[],
            columns:[
                {
                    name: 'fch_transaccion',                    
                    label: 'Fch. Transaccion',
                    align: 'left',                    
                    field: "fch_transaccion"
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
        this.get_rentabilidad_ult30dias()
    },
    methods:{
        get_rentabilidad_ult30dias:function(){
            this.$http.post(
                "/operacion/OperacionManager/get_rentabilidad_ult30dias",{},postconfig()
            ).then(httpresp => {
                this.msgbox = {
                    httpresp: httpresp,
                    onerror:true
                }

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