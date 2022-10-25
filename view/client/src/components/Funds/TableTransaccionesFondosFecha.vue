<template>
    <div>        
        <q-table class="no-shadow"
            :columns="columns"
            :data="data"
            row-key="num_transaccion"
            selection="single"
            :selected.sync="selected"
            :pagination="pagination"
            separator="vertical"
            dense
        >            
            <template v-slot:top >
                <q-btn color="green" icon="refresh" flat dense/>
                <q-btn color="blue-10" icon="arrow_upward" flat dense/>
                <q-btn color="blue-10" icon="arrow_downward" flat dense/>
                <q-btn color="red" icon="delete" flat dense/>
                <q-btn color="blue-10" icon="format_list_numbered_rtl" flat dense/>
            </template>
        </q-table>   
        <MessageBox ref="msgbox"/>     
    </div>
</template>
<script>
import MessageBox from '../MessageBox.vue'
import {headers} from '@/common/common.js'
export default {
    name:"TableTransaccionesFondosFecha",    
    components:{
        MessageBox
    },
    props:{
        filter:{
            type:Object,
            default: () => {}
        }        
    },
    data: () => {
        return {            
            columns:[{
                label:"N. Transaccion",
                align:"left",
                field:"num_transaccion",
                name:"num_transaccion",
                style:"width:30px;"
            },{
                label:"Operacion",
                align:"left",
                field:"tipo_trans_id",
                name:"tipo_trans_id"
            },{
                label:"Moneda",
                align:"left",
                field:"mon_trans_id",
                name:"mon_trans_id"
            },{
                label:"Importe",
                align:"right",
                field:"imp_transaccion",
                name:"imp_transaccion"
            }],
            data:[],
            pagination:{
                rowsPerPage:15
            },
            selected:[]
        }
    },
    mounted:function(){
        //this.get_transacciones_x_fecha(this.filter.fch_transaccion)
    },
    watch:{
        filter:function(newval){            
            let fch_transaccion = newval.fch_transaccion
            this.get_transacciones_x_fecha(fch_transaccion)
        }
    },
    methods:{        
        get_transacciones_x_fecha:function(fch_transaccion){            
            this.data = []

            this.$http.post('/FundsManager/FundsManager/get_transacciones_x_fecha',{
                fch_transaccion: fch_transaccion
            },{
                headers:headers()
            }            
            ).then(httpresp => {                
                this.$refs.msgbox.open({
                    httpresp:httpresp,
                    open:"onerror"
                })
                let appresp = httpresp.data
                let rownum = 0
                appresp.data.forEach(elem => {
                    rownum += 1
                    elem.rownum = rownum
                    this.data.push(elem)
                })
            })
        }
    }
}
</script>