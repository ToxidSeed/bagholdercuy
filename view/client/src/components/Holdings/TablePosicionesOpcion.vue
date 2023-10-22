<template>
    <div>        
        <q-table
            title="Opciones"
            :data="data"
            :columns="columns"
            :visible-columns="visible_columns"
            row-key="name"
            separator="vertical"
            dense            
            :pagination="pagination"
        >        
            <template v-slot:top>
                <q-toolbar  class="text-blue-10">
                    <!--<q-btn flat round dense icon="menu"></q-btn>-->
                    <q-toolbar-title>Opciones</q-toolbar-title>
                    <q-btn  flat dense icon="filter_alt" outline class="text-capitalize" @click="WinFiltrosPosicionOpciones.open = true">Filtros</q-btn>
                </q-toolbar>
                <!--<div class="text-h6">Opciones</div>-->
            </template>
        </q-table>
        <MessageBox :config="msgbox"/>
        <WinFiltrosPosicionOpciones v-model="WinFiltrosPosicionOpciones.open"
        v-on:filtrar-posiciones-opcion="filtrar"
        />
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue';
import WinFiltrosPosicionOpciones from '@/components/Holdings/WinFiltrosPosicionOpciones.vue';
import {postconfig} from '@/common/request.js';
import date from 'date-and-time'

export default {
    name:"TablePosicionesOpcion",
    props:{
        infiltros:{
            type:Object,
            default: () => {}
        }
    },
    components:{
        MessageBox,
        WinFiltrosPosicionOpciones
    },    
    data: () => {
        return {
            data:[],
            pagination:{
                rowsPerPage:100
            },
            columns:[
                {                    
                    label:"Contrato",
                    align:"left",
                    field:"symbol",
                    name:"symbol",
                    style:"width:100px;"      
                },{                    
                    label:"Subyacente",
                    align:"left",
                    field:"cod_symbol_subyacente",
                    name:"cod_symbol_subyacente",
                    style:"width:100px;"      
                },{                    
                    label:"Expiracion",
                    align:"left",
                    field:"fch_expiracion",
                    name:"fch_expiracion",
                    style:"width:100px;"      
                },{                    
                    label:"Tipo opcion",
                    align:"left",
                    field:"cod_tipo_opcion",
                    name:"cod_tipo_opcion",
                    headerStyle:"white-space:normal !important;",
                    style:"width:20px;"                          
                },{                    
                    label:"Imp. ejercicio",
                    align:"right",
                    field:"imp_ejercicio",
                    name:"imp_ejercicio",                    
                    style:"width:20px;"     /*,
                    classes: row => (
                        (row.cod_tipo_opcion == 'C' && row.ctd_saldo_posicion >= 0 && row.imp_valor_subyacente >= row.imp_ejercicio) || 
                        (row.cod_tipo_opcion == 'C' && row.ctd_saldo_posicion < 0 && row.imp_valor_subyacente < row.imp_ejercicio) || 
                        (row.cod_tipo_opcion == 'P' && row.ctd_saldo_posicion >= 0 && row.imp_valor_subyacente < row.imp_ejercicio) || 
                        (row.cod_tipo_opcion == 'P' && row.ctd_saldo_posicion < 0 && row.imp_valor_subyacente > row.imp_ejercicio)
                        ?'bg-green text-white':'bg-red text-white'
                    ) */
                }/*,{
                    label:"Rentable en ejercicio",
                    align:"right",
                    field:"imp_rentable",
                    name:"imp_rentable",
                    headerStyle:"white-space:normal !important;",
                    style:"width:90px;",
                    classes: row => (
                        (row.cod_tipo_opcion == 'C' && row.ctd_saldo_posicion >= 0 && row.imp_valor_subyacente >= row.imp_rentable) || 
                        (row.cod_tipo_opcion == 'C' && row.ctd_saldo_posicion < 0 && row.imp_valor_subyacente < row.imp_rentable) || 
                        (row.cod_tipo_opcion == 'P' && row.ctd_saldo_posicion >= 0 && row.imp_valor_subyacente < row.imp_rentable) || 
                        (row.cod_tipo_opcion == 'P' && row.ctd_saldo_posicion < 0 && row.imp_valor_subyacente > row.imp_rentable)
                        ?'bg-green text-white':'bg-red text-white'
                    ) 
                }*/,{
                    label:"En cartera desde",
                    align:"right",
                    field:"fch_primera_posicion",
                    name:"fch_primera_posicion",
                    style:"width:100px;"      
                },{
                    label:"Cantidad",
                    align:"right",
                    field:"ctd_saldo_posicion",
                    name:"ctd_saldo_posicion",
                    style:"width:60px;"      
                },{
                    label:"imp. valor inicial posicion",
                    align:"right",
                    field:"imp_posicion_incial",
                    name:"imp_posicion_incial",
                    headerStyle:"white-space:normal !important;",
                    style:"width:100px;"      
                },{
                    label:"Imp. valor minimo",
                    align:"right",
                    field:"imp_min_accion",
                    name:"imp_min_accion",
                    style:"width:100px;"      
                },{
                    label:"Imp. valor promedio",
                    align:"right",
                    field:"imp_prom_accion",
                    name:"imp_prom_accion",
                    style:"width:100px;"      
                },{
                    label:"Imp. valor maximo",
                    align:"right",
                    field:"imp_max_accion",
                    name:"imp_max_accion",
                    style:"width:100px;"      
                }/*,{
                    label:"Valor subyacente",
                    align:"right",
                    field:"imp_valor_subyacente",
                    name:"imp_valor_subyacente",       
                    headerStyle:"white-space:normal !important;",             
                    style:"width:50px;"                          
                }*/,{
                    label:"",
                    align:"left",
                    field:"",
                    name:""
                }
            ],
            msgbox:{},
            cotizacion:{},
            WinFiltrosPosicionOpciones:{
                open:false
            },
            filtros:{
                cod_subyacente:"",
                cod_opcion:"",
                anyo_expiracion:"",
                mes_expiracion:"",
                dia_expiracion:"",
                flg_call:true,
                flg_put:true
            }
        }
    },
    computed:{
        visible_columns:function(){
            let visible = []
            let columnas_ocultas = ["xx"]
            for (let column of this.columns){
                if (columnas_ocultas.includes(column.name) == true){
                    continue;
                }

                visible.push(column.name)
            }
            return visible
        }
    },
    mounted:function(){
        this.get_posiciones_opcion()
    },
    methods:{     
        filtrar:function(filtros){
            this.filtros = filtros            
            this.get_posiciones_opcion()
        },
        get_posiciones_opcion:function(){            
            this.$http.post(
                '/posicion/PosicionManager/get_posiciones_contratos_opciones',{
                    id_cuenta:localStorage.getItem("id_cuenta")
                },
                postconfig()
            ).then(httpresp => {
                this.msgbox = {
                    httpresp: httpresp,
                    onerror: true
                }
                let appdata = httpresp.data
                this.data = []

                for (let elem of appdata.data){                    
                    this.cotizacion[elem.cod_subyacente] = null                    
                    let row = Object.assign({}, elem);
                    row.fch_expiracion = date.transform(elem.fch_expiracion,"YYYY-MM-DD","DD/MM/YYYY")
                    row.fch_primera_posicion = date.transform(elem.fch_primera_posicion,"YYYY-MM-DD","DD/MM/YYYY")
                    row["imp_ejercicio"] = elem["imp_ejercicio"].toFixed(2)
                    row["imp_posicion_incial"] = elem["imp_posicion_incial"].toFixed(2)
                    row["imp_min_accion"] = elem["imp_min_accion"].toFixed(2)
                    row["imp_prom_accion"] = elem["imp_prom_accion"].toFixed(2)
                    row["imp_max_accion"] = elem["imp_max_accion"].toFixed(2)
                    row["imp_valor_subyacente"] = 0                    
                    /*row["imp_valor_posicion"] = elem["imp_valor_posicion"].toFixed(2)
                    row["imp_rentabilidad"] = elem["imp_rentabilidad"].toFixed(2)         
                    if (elem.cod_tipo_opcion == "C"){
                        row["imp_rentable"] = (parseFloat(elem.imp_ejercicio) + parseFloat(elem.imp_prom_accion)).toFixed(2)                                                            
                    }else{
                        row["imp_rentable"] = (parseFloat(elem.imp_ejercicio) - parseFloat(elem.imp_prom_accion)).toFixed(2)                                                            
                    }*/
                    
                    this.data.push(row) 
                }
                    
                //this.iniciar_intervalo_cotizaciones()
            })
        },
        iniciar_intervalo_cotizaciones: function(){            
            let symbols = []
            for (let prop in this.cotizacion){
                symbols.push(prop)
            }
            //console.log(symbols)

            var self = this
            const promises = symbols.map(symbol => self.get_cotizacion_subyacente(symbol).then(res => res.data.data))

            Promise.all(promises).then(records => {
                for (let row of records){
                    self.cotizacion[row.cod_symbol] = row.imp_cierre                    
                }                       
                for (let elem of self.data){                                    
                    elem.imp_valor_subyacente = self.cotizacion[elem.cod_subyacente]                           
                }
            })
        
        },
        get_cotizacion_subyacente: async function(cod_symbol){                        
            return this.$http.post(
                'cotizacion/CotizacionManager/get_cotizacion',{
                    cod_symbol:cod_symbol
                },
                postconfig()
            )                        
            
        }
    } 
}
</script>