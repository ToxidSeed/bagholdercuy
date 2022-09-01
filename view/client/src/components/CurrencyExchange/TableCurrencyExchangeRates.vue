<template>
    <div>        
        <q-table
            :title="title"
            :data="data"
            :columns="columns"
            row-key="par_name"
            dense
            separator="vertical"
            :pagination="pagination"
            @row-dblclick="row_dblclick"
            :visible-columns="visiblecolumns"
        >
            <template v-slot:top>
                <div>
                    <div class="text-h6">{{title}}</div>
                    <div>
                        <q-btn label="Criterios de búsqueda" color="light-green" icon="search" @click="win_filtrar_open=true"/>
                    </div> 
                </div>               
            </template>
        </q-table>
        <q-dialog v-model="win_filtrar_open">
            <q-card style="min-width: 25vw">
                <q-card-section class="q-pb-none">                    
                    <div class="text-h6 text-primary">Filtros</div>
                </q-card-section>
                <q-card-section class="q-pt-none">
                    <div class="row">
                        <q-input class="col-4" label="Fch. Cambio" v-model="fch_cambio" mask="##/##/####" fill-mask=""/>
                    </div>
                    <q-input label="Par" v-model="par"/>
                </q-card-section>
                <q-card-actions>
                    <q-btn label="Buscar" color="primary"/>                    
                    <q-btn label="Cerrar" color="red" @click="win_filtrar_open=false"/>                    
                </q-card-actions>
            </q-card>
        </q-dialog>
    </div>
</template>
<script>
export default {
    name:"TableCurrencyExchangeRates",
    props:{
        selection:{
            type:Boolean,
            default:false
        },
        title:{
            type:String,
            default:"Historial de Tipos de Cambio"
        },
        visiblecolumns:{
            type: Array,
            default: () => [
                "fch_cambio","par_nombre","ind_activo","imp_compra","imp_venta",""
            ]
        }
    },
    data: () => {
        return {
            fch_cambio:"",
            par:"",
            win_filtrar_open:false,
            pagination:{
                rowsPerPage:25
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
                    label:"Ind. Activo",
                    align:"left",
                    field:"ind_activo",
                    name:"ind_activo",
                    style: 'width: 60px'
                },{
                    label:"Imp. Compra",
                    align:"right",
                    field:"imp_compra",
                    name:"imp_compra",
                    style: 'width: 60px'
                },{
                    label:"Imp. Venta",
                    align:"right",
                    field:"imp_venta",
                    name:"imp_venta",
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
        this.get_historic_rates()
    },
    methods:{
        get_historic_rates:function(){
            this.$http.post('CurrencyExchangeManager/CurrencyExchangeFinder/get_historic_rates',{

            }).then(httpresponse => {
                var appdata = httpresponse.data
                this.data = appdata.data
            })
        },
        row_dblclick:function(event, row){
            if(this.selection == true){
                this.$emit('select',row)
            }
        }
    }
}
</script>