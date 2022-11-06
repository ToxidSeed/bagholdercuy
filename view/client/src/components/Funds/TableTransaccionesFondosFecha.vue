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
                <q-btn color="green" icon="refresh" flat dense @click="get_transacciones_x_fecha(filter.fch_transaccion)"/>
                <q-btn color="blue-10" icon="arrow_upward" flat dense @click="subir"/>
                <q-btn color="blue-10" icon="arrow_downward" flat dense @click="bajar"/>
                <q-btn color="red" icon="delete" flat dense @click="eliminar"/>
                <q-btn color="blue-10" icon="format_list_numbered_rtl" flat dense @click="reenumerar"/>
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
            selected:[],
            list_eliminar:[]
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
        eliminar:function(){
            let selected = this.selected.shift()

            const index = this.data.findIndex(element => {
                return element.num_transaccion == selected.num_transaccion
            })

            this.data.splice(index,1)
            this.list_eliminar.push(selected)
            this.reenumerar()
            console.log(this.list_eliminar)

        },  
        reenumerar: function(){
            let num_transaccion = 0
            this.data.forEach(element => {
                num_transaccion++ 
                element.num_transaccion = num_transaccion
            })
        },
        subir:function(){            
            if(this.selected.length == 0){
                return;
            }
            let selected = this.selected.shift()
            let prev_num_trans = selected.num_transaccion - 1
            const prevrow = this.data.find(element => {
                return element.num_transaccion == prev_num_trans
            })

            prevrow.num_transaccion = selected.num_transaccion
            selected.num_transaccion = prev_num_trans
            this.selected.push(selected)
            this.ordenar()
        },
        bajar:function(){
            let selected = this.selected.shift()
            let num_transaccion = selected.num_transaccion
            let sig_num_transaccion = num_transaccion + 1
            const sigrow = this.data.find(element => {
                return element.num_transaccion == sig_num_transaccion
            })
            sigrow.num_transaccion = num_transaccion
            selected.num_transaccion = sig_num_transaccion
            this.selected.push(selected)
            this.ordenar()
        },
        ordenar:function(){
            this.data.sort((a,b)=> {
                if(a.num_transaccion > b.num_transaccion){
                    return 1;
                }
                if(a.num_transaccion < b.num_transaccion){
                    return -1;
                }
                if(a.num_transaccion == b.num_transaccion){
                    return 0
                }
            })
        },
        get_transacciones_x_fecha:function(fch_transaccion){            
            this.data = []
            this.selected=[]
            this.list_eliminar=[]

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
                    elem.imp_transaccion = elem.imp_transaccion.toFixed(2)
                    this.data.push(elem)
                })
            })
        }
    }
}
</script>