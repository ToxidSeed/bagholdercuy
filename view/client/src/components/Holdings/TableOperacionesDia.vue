<template>
    <div>        
        <q-table
            title="Ordenes por día"
            :columns="columns"
            :data="data"
            row-key="num_orden"
            selection="single"
            :selected.sync="selected"
            :pagination="pagination"  
            separator="vertical"    
            dense 
        >
            <template v-slot:top>                                                                  
                <q-toolbar class="q-pl-none">     
                    <div class="q-gutter-xs">
                        <q-btn class="q-ml-md" color="green" dense icon="keyboard_arrow_down" @click="mover_abajo"/>                
                        <q-btn color="primary" dense icon="keyboard_arrow_up" @click="mover_arriba"/>
                    </div>
                </q-toolbar>
            </template>
        </q-table>
        <MessageBox ref="msgbox"/>
        <HelperFechasOrden ref="helperfechas"
        v-on:select="select_fch_orden"
        />
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue'
import HelperFechasOrden from '@/components/helpers/HelperFechasOrden.vue'

import date from 'date-and-time'
import {CLIENT_DATE_FORMAT, ISO_DATE_FORMAT}  from '@/common/constants.js'
import {get_postconfig} from '@/common/request.js'

export default {
    name:"TableOperacionesDia",
    components:{
        MessageBox,
        HelperFechasOrden
    },
    data: () => {
        return {
            fch_orden:"",
            filter:{
                fch_orden:""
            },
            flg_opcion:false,
            columns:[
                {
                    label:"N. Orden",
                    align:"left",
                    field:"num_orden",
                    name:"num_orden",
                    style:'width:60px;'
                },{
                    label:"Operacion",
                    align:"left",
                    field:"order_type",
                    name:"order_type",
                    style:'width:60px;'
                },{
                    label:"Symbol",
                    align:"left",
                    field:"symbol",
                    name:"symbol",
                    style:'width:60px;'
                },{
                    label:"Cantidad",
                    align:"left",
                    field:"quantity",
                    name:"quantity",
                    style:'width: 60px'
                },{
                    label:"Imp. Accion",
                    align:"left",
                    field:"price",
                    name:"price",
                    style:'width:60px;'
                },{
                    label:"",
                    align:"left",
                    field:"",
                    name:""
                }
            ],
            data:[],
            selected:[],
            pagination:{
                rowsPerPage:15
            }
        }
    },
    mounted:function(){
        //this.init()
    },
    watch:{
        /*fch_orden:function(newval){
            this.get_ordenes_x_fecha(newval)
        }*/
    },  
    methods:{
        init:async function(){
            let postconfig = get_postconfig()
            let httpresp = await this.$http.post('/OrdenManager/Buscador/get_max_fch_orden',{},postconfig)
            let appdata = httpresp.data
            if(appdata.success == false){
                this.$refs.msgbox.httpresp(httpresp)
            }else{
                let data = appdata.data
                this.filter.fch_orden = date.transform(data.fch_orden,ISO_DATE_FORMAT,CLIENT_DATE_FORMAT)
                this.fch_orden = this.filter.fch_orden
            }
            //
            this.get_ordenes_x_fecha(this.filter.fch_orden)    
        },
        get_ordenes_x_fecha:function(fch_orden){          
            let postconfig = get_postconfig()

            this.selected=[]            
            this.$http.post('/OrdenManager/Buscador/get_ordenes_x_fecha',{
                fch_orden:fch_orden
            },postconfig).then(httpresp => {
                let appresp = httpresp.data
                if(appresp.success == false){
                    this.$refs.msgbox.httpresp(httpresp)
                }else{
                    this.data = appresp.data
                }
            })
        },
        open_fechas_helper:function(){
            this.$refs.helperfechas.open()
        },
        select_fch_orden:function(row){        
            this.fch_orden=row.order_date
            this.filter.fch_orden = row.order_date    
            this.get_ordenes_x_fecha(this.filter.fch_orden)        
        },
        mover_arriba:function(){
            let selected = this.selected.shift()
            let num_orden = selected.num_orden
            let prev_num_orden = num_orden - 1            
            const prevrow = this.data.find(element => {
                return element.num_orden == prev_num_orden
            })
            prevrow.num_orden = num_orden
            selected.num_orden = prev_num_orden
            this.selected.push(selected)
            //ordenar
            this.ordenar()
        },
        mover_abajo:function(){
            let selected = this.selected.shift()
            let num_orden = selected.num_orden
            let sig_num_orden = num_orden + 1
            const sigrow = this.data.find(element => {
                return element.num_orden == sig_num_orden
            })
            sigrow.num_orden = num_orden
            selected.num_orden = sig_num_orden
            this.selected.push(selected)
            this.ordenar()
        },
        ordenar:function(){
            this.data.sort((a,b)=> {
                if(a.num_orden > b.num_orden){
                    return 1;
                }
                if(a.num_orden < b.num_orden){
                    return -1;
                }
                if(a.num_orden == b.num_orden){
                    return 0
                }
            })
        }
    }
}
</script>