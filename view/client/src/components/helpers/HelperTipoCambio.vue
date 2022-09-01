<template>
    <q-dialog v-model="visible">        
        <q-card style="max-width:350px;">
            <q-card-section class="q-pb-none row">
                <div class="text-h6 text-primary">Tipos de Cambio</div>
                <q-space/>
                <div>
                    <q-btn flat icon="close" @click="visible=false"/>
                </div>
            </q-card-section>
            <q-card-actions class="q-mt-none q-pt-none q-pb-none">
                <q-btn flat dense label="Criterios de búsqueda" @click="criterios=!criterios" icon="fa fa-arrow-down"/>
            </q-card-actions>
            <q-card-section v-show="criterios">
                <div class="row" style="max-width=100px;">
                    <div class="col-8">     
                        <div class="row">
                            <q-input class="col-6" dense label="Desde" v-model="fch_desde" mask="##/##/####" fill-mask=""/>
                            <q-input class="col-6 q-pl-xs" dense label="Hasta" v-model="fch_hasta" mask="##/##/####" fill-mask=""/>                        
                        </div>
                        <q-input dense stack-label label="Pares" v-model="pares" :readonly="input_pares_readonly"/>                                                
                    </div>                    
                    <div class="col-4 q-pl-md">
                        <q-btn color="teal" label="filtrar" @click="get_historic_rates"/>
                    </div>
                </div>
            </q-card-section>
            <q-separator />
            <q-table

                :data="data"
                :columns="columns"
                dense
                row-key="par_name"
                separator="vertical"
                :pagination="pagination"
                @row-dblclick="select"
            >
                
            </q-table>            
        </q-card>
    </q-dialog>
</template>
<script>
import date from 'date-and-time'
import {config} from '@/common/request.js'

export default {
    name:"HelperTipoCambio",
    components:{
        
    },
    props:{
        throwerror:{
            type:Boolean,
            default:true
        },
        in_fch_desde:{
            type:String,
            default:""
        },
        in_fch_hasta:{
            type:String,
            default:""
        },
        in_pares:{
            type:String,
            default:""
        },
        input_pares_readonly:{
            type:Boolean,
            default:false
        },
        close_on_select:{
            type:Boolean,
            default:true
        }
    },
    data: () => {
        return {
            visiblecolumns:["fch_cambio","par_nombre","imp_compra",""],
            visible:false,
            criterios:true,
            fch_desde:"",
            fch_hasta:"",
            pares:"",
            pagination:{
                rowsPerPage:10
            },
            columns:[
                {
                    label:"Fecha Cambio",
                    align:"left",
                    field:"fch_cambio",
                    name:"fch_cambio",
                    style: 'width: 40px'
                },{
                    label: "Par",
                    align:"left",
                    field:"par_nombre",
                    name:"par_nombre",
                    style: 'width: 60px'
                },{
                    label:"Imp. Compra",
                    align:"right",
                    field:"imp_compra",
                    name:"imp_compra",
                    style: 'width: 60px'
                },{
                    label:"",
                    align:"left",
                    field:"",
                    name:""
                }
            ],
            data:[]
        }
    },
    mounted:function(){
        this.fch_desde = this.in_fch_desde
        this.fch_hasta = this.in_fch_hasta
        this.pares = this.in_pares
        this.get_historic_rates(this.pares)
    },
    watch:{
        visible:function(newval){
            if(newval==true){
                this.fch_desde = this.in_fch_desde
                this.fch_hasta = this.in_fch_hasta
                this.pares = this.in_pares  
            }
        }
    },
    methods:{        
        get_historic_rates:function(pares){            
            if(pares == ""){
                return
            }

            this.data = []
            this.$http.post('CurrencyExchangeManager/CurrencyExchangeFinder/get_historic_rates',{

            }, config()).then(httpresponse => {
                var appdata = httpresponse.data
                if(appdata.success == false){
                    if (this.throwerror == true){
                        this.$emit('httperror', httpresponse)
                    }
                }else{
                    appdata.data.forEach(element => {
                        element.fch_cambio = date.transform(element.fch_cambio,"YYYY-MM-DD","DD/MM/YYYY")
                        this.data.push(element  )
                    });            
                }                                
            })
        },
        select:function(evt,row){                     
            this.$emit('select',row)
            this.visible = this.close_on_select==true?false:true;
        },
        open:function(){
            this.visible = true
            this.get_historic_rates(this.in_pares)
        }
    }
}
</script>