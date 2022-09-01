<template>
    <div>    
        <q-dialog v-model="visible" >            
            <q-card style="width:400px;">
                <q-card-section class="q-pb-none">
                    <div class="text-h6 text-primary">Seleccion de Fechas</div>
                </q-card-section>
                <q-card-section class="row">
                    <div class="row">
                        <SelectAnyosOrden
                            class="col-4"
                            v-bind:in_anyo="String(filter.anyo)"
                        />                        
                        <SelectMesesOrden
                            class="col-4 q-pl-xs"
                            v-bind:in_anyo="String(filter.anyo)"
                            v-bind:in_mes="String(filter.mes)"
                            v-on:httperror="msgbox"
                        />
                        <q-space/>
                        <div>
                            <q-btn label="Filtrar" color="positive"/>
                        </div>
                    </div>                    
                </q-card-section>
                <q-card-section class="q-pa-none">
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
import {CLIENT_DATE_FORMAT,ISO_DATE_FORMAT} from '@/common/constants.js'
import date from 'date-and-time';
import MessageBox from '@/components/MessageBox.vue'
import SelectAnyosOrden from '@/components/helpers/SelectAnyosOrden.vue'
import SelectMesesOrden from '@/components/helpers/SelectMesesOrden.vue'
export default {
    name:"HelperFechasOrden",    
    props:{
        anyo:{
            type:String,
            default:""            
        },
        mes:{
            type:String,
            default:""
        },
        close_on_select:{
            type:Boolean,
            default:true
        }
    },
    components:{
        MessageBox,
        SelectAnyosOrden,
        SelectMesesOrden
    },
    data: () => {
        return {
            filter:{
                anyo:"",
                mes:""
            },
            visible:false,
            columns:[
                {
                    label:"Fch. Orden",
                    align:"left",
                    name:"order_date",
                    field:"order_date",
                    style:"width:100px;"
                },{
                    label:"Num. Ordenes",
                    align:"right",
                    name:"num_ordenes",
                    field:"num_ordenes",
                    style:"width:50px;"
                },{
                    label:"",
                    align:"left",
                    name:"",
                    field:""
                }
            ],
            data:[],
            pagination:{
                rowsPerPage:31
            }
        }
    },
    mounted:function(){     
        this.init()
            
        //cargar los años

        //cargar los meses
    },
    watch:{
        /*anyo:function(newval,oldval){                    
            console.log(newval)
            console.log(oldval)
            console.log(this.mes)
            if(newval!=""){
                this.get_meses(newval)
            }
            if(newval!="" && this.mes!=""){
                this.get_fechas(newval, this.mes)
            }            
        },
        mes:function(newval,oldval){                  
            console.log(newval)
            console.log(oldval)
            if(newval!="" && this.anyo!=""){
                this.get_fechas(this.anyo, newval)
            }
        }*/
    },
    methods:{        
        open:function(){
            this.visible=true
        },        
        init: async function(){  
            this.filter.anyo = this.anyo
            this.filter.mes = this.mes
            
            /*Si se han asignado como propiedad cargamos el mes y el año*/
            if(this.filter.anyo != "" && this.filter != ""){
                this.get_fechas(this.filter.anyo, this.filter.mes)
                return;
            }

            /*Si el año o el mes no se han seteado obtenemos la maxima fecha de*/
            let httpresp = await this.$http.post('/OrdenManager/Buscador/get_max_fch_orden')
            let appresp = httpresp.data
            if(appresp.success==false){
                this.$refs.msgbox.httpresp(httpresp)
                return
            }
            
            let data = appresp.data                    
            this.filter.anyo = data.anyo
            this.filter.mes = data.mes
            this.get_fechas(this.filter.anyo, this.filter.mes)            
        },
        get_fechas:function(anyo, mes){
            this.data=[]
            this.$http.post('/OrdenManager/Buscador/get_fechas',{
                anyo:anyo,
                mes:mes
            }).then(httpresp => {
                let appresp = httpresp.data
                if(appresp.success == false){
                    this.$refs.msgbox.httpresp(httpresp)
                }else{
                    appresp.data.forEach(element => {
                        element.order_date = date.transform(element.order_date,ISO_DATE_FORMAT,CLIENT_DATE_FORMAT)
                        this.data.push(element)
                    })                    
                }
            })
        },
        msgbox:function(httpresp){
            this.$refs.msgbox.httpresp(httpresp)
        },
        select:function(evt, row){
            this.$emit('select', row)
            this.visible = this.close_on_select==true?false:true;
        }        
    }
}
</script>