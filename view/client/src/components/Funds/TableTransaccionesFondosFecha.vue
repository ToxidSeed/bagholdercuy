<template>
    <div>        
        <q-table class="no-shadow"
            :columns="columns"
            :data="data"
            row-key="num_transaccion"                        
            :pagination="pagination"
            separator="vertical"
            dense
        >            
            <template v-slot:top >
                <q-btn color="blue-10" icon="menu" flat dense >
                    <q-menu>
                          <q-list style="min-width: 100px">
                            <q-item clickable v-close-popup>
                                <q-item-section @click.native="get_ultima_fecha_con_datos()">Última fecha con datos</q-item-section>
                            </q-item>                         
                        </q-list>
                    </q-menu>
                </q-btn>                
                <q-btn color="green" icon="refresh" flat dense @click="get_transacciones_x_fecha()"/>                
                <q-toolbar-title>
                    Transacciones de la fecha <span class="text-blue-10">{{filter.fch_transaccion}}</span>
                </q-toolbar-title>
                <!--
                <q-btn color="blue-10" icon="arrow_upward" flat dense @click="subir"/>
                <q-btn color="blue-10" icon="arrow_downward" flat dense @click="bajar"/>
                <q-btn color="red" icon="delete" flat dense @click="eliminar"/>
                <q-btn color="blue-10" icon="format_list_numbered_rtl" flat dense @click="reenumerar"/>
                -->
            </template>
        </q-table>   
        <MessageBox ref="msgbox"/>     
    </div>
</template>
<script>
import MessageBox from '../MessageBox.vue';
import {postconfig} from '@/common/request.js';
import {CLIENT_DATE_FORMAT} from '@/common/constants.js'
import date from 'date-and-time';
import {cdate} from '@/common/custom-date.js';

export default {
    name:"TableTransaccionesFondosFecha",    
    components:{
        MessageBox
    },
    props:{
        in_filter:{
            type:Object,
            default: () => {
                return {
                    fch_transaccion:"",
                    updtime: Date.now()
                }   
            }            
        },
        init:{
            type:Boolean,
            default:false            
        }        
    },    
    data: () => {
        return {      
            filter:{
                fch_transaccion:""
            },      
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
                name:"tipo_trans_id",
                style:"width:30px;"
            },{
                label:"Moneda",
                align:"left",
                field:"mon_trans_id",
                name:"mon_trans_id",
                style:"width:30px;"
            },{
                label:"Importe",
                align:"right",
                field:"imp_transaccion",
                name:"imp_transaccion",
                style:"width:30px;"
            },{
                label:"Info",
                align:"left",
                field:"info_adicional",
                name:"info_adicional",
                style:"width:100px;"
            },{
                label:"",
                name:""
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
        if (this.init){
            this.init_table()
        }
        
        //this.get_transacciones_x_fecha(this.filter.fch_transaccion)        
        //console.log(this.filter)
    },
    watch:{        
        "in_filter.updtime":function(newval){    
            console.log('updtime'+newval)

            this.filter.fch_transaccion = this.in_filter.fch_transaccion
            console.log(this.filter)
            this.get_transacciones_x_fecha()                       
        }
    },
    methods:{             
        init_table:function(){            
            if (this.in_filter.updtime == undefined){
                return;
            }
            if (this.in_filter.updtime == ""){
                return;
            }                 
            if (this.in_filter.fch_transaccion != ""){
                this.filter.fch_transaccion = this.in_filter.fch_transaccion
            }
            if (this.in_filter.fch_transaccion == "" || this.in_filter.fch_transaccion == undefined || this.in_filter.fch_transaccion == null){
                this.filter.fch_transaccion = date.format(new Date(),CLIENT_DATE_FORMAT)
            }

            this.get_transacciones_x_fecha()            
        },
        get_transacciones_x_fecha:function(){                            
            if (this.filter.fch_transaccion == null){
                return;
            }    

            this.data = []
            this.selected=[]
            this.list_eliminar=[]                                
            
            //console.log(postconfig)

            this.$http.post('/FundsManager/FundsManager/get_transacciones_x_fecha',{
                fch_transaccion: this.filter.fch_transaccion
            },postconfig()).then(httpresp => {                
                this.$refs.msgbox.http_resp_on_error(httpresp)
                let appresp = httpresp.data
                if (appresp.success){
                    let rownum = 0
                    appresp.data.forEach(elem => {
                        rownum += 1
                        elem.rownum = rownum
                        elem.imp_transaccion = elem.imp_transaccion.toFixed(2)
                        this.data.push(elem)
                    })
                }                
            })
        },
        get_ultima_fecha_con_datos:function(){
            this.data = []
            this.$http.post('/FundsManager/FundsManager/get_ult_fecha_con_datos',{
            },postconfig()).then(httpresp => {
                this.$refs.msgbox.http_resp_on_error(httpresp)
                let appresp = httpresp.data
                if(appresp.success){
                    let rownum = 0
                    appresp.data.forEach(elem => {
                        rownum += 1
                        elem.rownum = rownum
                        elem.imp_transaccion = elem.imp_transaccion.toFixed(2)
                        this.data.push(elem)   
                    })
                    this.filter.fch_transaccion = cdate.iso_to_client(appresp.extradata.max_fch_transaccion)
                }
            })
        }
    }
}
</script>