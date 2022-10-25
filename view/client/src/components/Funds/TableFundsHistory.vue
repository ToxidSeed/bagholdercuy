<template>
    <div>
        <q-table
            title="Historial"
            :columns=columns
            :data=data
            row-key="id"
            dense
            selection="multiple"
            :selected.sync="selected"
            separator="vertical"
            :pagination="pagination"
        >
            <template v-slot:top>
                <div>                    
                    <q-btn label="Rec. Saldos" color="primary"/>                    
                </div>
            </template>
        </q-table>
        <MessageBox v-bind:config="msgboxconfig"/>
    </div>
</template>
<script>
/*import {CLIENT_DATE_FORMAT} from '@/common/constants.js'
import date from 'date-and-time'*/
import MessageBox from '../MessageBox.vue'
import {headers} from '@/common/common.js'

export default {
    name:"TableFundsHistory",
    components:{
        MessageBox
    },
    data: () => {
        return {
            columns:[
                {
                    label:"id",
                    name:"id",
                    field:"id",
                    style:"width:100px;"
                },
                {
                    label:"Fch. transacción",
                    name:"fch_transaccion",
                    field:"fch_transaccion",
                    style:"width:100px;"
                },{
                    label:"Tipo",
                    name:"tipo_trans_id",
                    field:"tipo_trans_id",
                    style:"width:100px;"
                },{
                    label:"Imp. Transaccion",
                    name:"imp_transaccion",
                    field:"imp_transaccion",
                    style:"width:100px;"
                },{
                    label:"Mon. Transaccion",
                    name:"mon_trans_id",
                    field:"mon_trans_id",
                    style:"width:100px;"
                },{
                    label:"Concepto",
                    align:"left",
                    name:"info_adicional",
                    field:"info_adicional"
                },{
                    label:"",
                    name:"",
                    field:""
                }
            ],
            data:[],
            selected:[],
            msgboxconfig:{},
            pagination:{
                rowsPerPage:25
            }
        }
    },
    mounted:function(){
        this.get_historial()
    },
    methods:{
        get_historial:function(){
            this.$http.post('FundsManager/Historial/get',{},{
                headers:headers()
            }).then(httpresp => {
                this.msgboxconfig = {
                    httpresp:httpresp,
                    open:"onerror"
                }

                var appresp = httpresp.data
                var data = appresp.data
                this.data = data
            })
        }
    }
}
</script>