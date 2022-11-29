<template>
    <div>
        <q-dialog v-model="visible">            
            <q-card class="no-shadow" style="width:450px;">
                <q-toolbar class="text-blue-10">    
                    <q-toolbar-title>
                        Buscar transacciones por:
                    </q-toolbar-title>    
                    <q-btn icon="close" flat color="red" @click="visible=false"/>  
                </q-toolbar>
                <q-card-section class="row q-pt-none">
                    <!--<div class="q-pt-xs text-subtitle1 text-blue-10">Buscar transacciones por:</div>-->
                    <div class="row q-gutter-xs">                         
                        <q-input class="col-4" label="Desde" stack-label
                        mask="##/##/####" v-model.lazy="filter.fch_inicio"
                        type="text"                        
                        hint="dd/mm/yyyy"                    
                        />
                        <q-input class="col-4" label="Hasta" stack-label
                        mask="##/##/####" v-model.lazy="filter.fch_fin"                        
                        hint="dd/mm/yyyy"                    
                        />
                        <q-space/>
                        <div>
                            <q-btn class="q-ml-xs" label="Buscar" color="secondary" @click="get_count_transacciones"/>                                        
                            <!--<q-btn class="q-ml-xs" label="Ver fechas" color="secondary" @click="open_fechas_helper"/>-->
                        </div>                
                    </div>                
                </q-card-section>            
                <q-card-section
                class="q-pl-none q-pb-none q-pr-none"
                >
                    <q-table
                    dense                    
                    :columns="columns"
                    :data="data"
                    row-key="fch_orden"
                    separator="vertical"
                    :pagination="pagination"    
                    @row-dblclick="select"                
                    >
                    </q-table>
                </q-card-section>
            </q-card>            
        </q-dialog>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '../MessageBox.vue'
import date from 'date-and-time'
import {headers} from '@/common/common.js'
export default {
    name:"HelperTransaccionesFondos",
    props:["value"],
    components:{
        MessageBox
    },
    data () {
        return {
            visible:this.value,
            filter:{
                fch_inicio:"",
                fch_fin: date.format(new Date(),'DD/MM/YYYY')
            },
            columns:[{
                label:"#",
                align:"right",
                field:"rownum",
                name:"rownum",
                style:"width:30px;",
                headerClasses: 'bg-grey-3',
                classes:"rownum"
            },{
                label:"Fecha",
                align:"left",
                field:"fch_transaccion",
                name:"fch_transaccion",
                style:"width:100px;"
            },{
                label:"N. Transacciones",
                align:"right",
                field:"num_transacciones",
                name:"num_transacciones",
                style:"width:100px;"
            },{
                label:"",
                field:"",
                name:""
            }],
            data:[],
            pagination:{
                rowsPerPage:25
            }            
        }
    },
    watch:{
        value:function(newval){
            this.visible = newval
            if(newval == true){
                this.get_count_transacciones()
            }
        },
        visible:function(newval){
            if(newval == false){
                this.$emit('input', newval)
            }
        }
    },
    mounted:function(){
        console.log('mounted helper transacciones fondos mounted')
    },
    methods:{
        select:function(evt,row){            
            this.$emit("select",row)
            this.visible=false
        },
        get_count_transacciones:function(){
            this.data = []
            this.$http.post("/FundsManager/FundsManager/get_count_transacciones",{
                fch_desde:this.filter.fch_inicio,
                fch_hasta:this.filter.fch_fin
            },{
                headers:headers()
            }).then(httpresp => {
                this.$refs.msgbox.http_resp_on_error(httpresp)
                let appresp = httpresp.data
                //let data = appresp.data
                //this.data = data
                let rownum = 0
                appresp.data.forEach(element => {                    
                    rownum += 1
                    element.rownum = rownum
                    element.fch_transaccion = date.transform(element.fch_transaccion, 'YYYY-MM-DD','DD/MM/YYYY')
                    this.data.push(element)
                })
            })
        }
    }
}
</script>
<style lang="sass">
@import '~quasar/src/css/variables'
.rownum
    background-color: $grey-3 !important    
</style>