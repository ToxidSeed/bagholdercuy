<template>
    <div>        
        <q-table
            title="Historial de Tipos de Cambio"
            :data="data"
            :columns="columns"
            row-key="par_name"
            dense
            :pagination="pagination"
        >
            <template v-slot:top>
                <div>
                    <div class="text-h6">Historial de Tipos de Cambio</div>
                    <div>
                        <q-btn color="light-green" icon="search" @click="win_filtrar_open=true"/>
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
                        <q-input class="col-4" label="Fch. Cambio" v-model="fch_cambio" mask="##/##/####" fill-mask="#"/>
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
    data: () => {
        return {
            fch_cambio:"",
            par:"",
            win_filtrar_open:false,
            pagination:{
                rowsPerPage:20
            },
            columns:[
                {
                    label:"Fecha Cambio",
                    align:"left",
                    field:"fecha_cambio",
                    name:"fecha_cambio"
                },{
                    label: "Par",
                    align:"left",
                    field:"par_name",
                    name:"par_name"
                },{
                    label:"Ind. Activo",
                    align:"left",
                    field:"ind_activo",
                    name:"ind_activo"
                },{
                    label:"Imp. Compra",
                    align:"right",
                    field:"importe_compra",
                    name:"importe_compra"
                },{
                    label:"Imp. Venta",
                    align:"right",
                    field:"importe_venta",
                    name:"importe_venta"
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
        }
    }
}
</script>