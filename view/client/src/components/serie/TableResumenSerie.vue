<template>
    <div>
        <q-table
            :columns="columns"
            :data="store.state.t_resumen.data"
            :pagination="pagination"
            row-key="symbol_id"
            separator="vertical"
            dense
            class="no-shadow"
            wrap-cells
        >
            <template v-slot:body-cell-menu="props">
                <q-td :props="props">
                    <q-btn
                    flat
                    dense
                    icon="more_vert"                    
                    >
                        <q-menu>
                            <q-list dense class="text-body1">
                                <q-item clickable v-close-popup @click="store.table_resumen_serie.actualizar_serie(props.row)">
                                    <q-item-section><span><q-icon name="update" color="green" class="q-pr-xs"></q-icon>Actualizar</span></q-item-section>
                                </q-item>
                                <q-item clickable v-close-popup @click="store.abrir_w_reprocesar(props.row.cod_symbol)">
                                    <q-item-section><span><q-icon name="construction" color="green" class="q-pr-xs"></q-icon>Reprocesar</span></q-item-section>
                                </q-item>
                            </q-list>
                        </q-menu>    
                    </q-btn>
                </q-td>
            </template>
            <template v-slot:body-cell-estado="props">
                <q-td :props="props">
                    <q-chip size="12px" :color="determinar_color_chip_estado_general(props.row.estado)" :class="determinar_color_estado_general(props.row.estado)">{{ props.row.estado }}</q-chip>
                </q-td>
            </template>
            <template v-slot:body-cell-est_serie_diaria="props">
                <q-td :props="props">
                    <q-chip size="12px" 
                    :color="determinar_color_chip(props.row.serie_diaria_integridad.dsc_estado)" 
                    :class="determinar_color(props.row.serie_diaria_integridad.dsc_estado)">{{ props.row.serie_diaria_integridad.dsc_estado}}
                    </q-chip>
                    <q-popup-proxy context-menu>
                        <div class="q-pl-xs q-pt-xs text-subtitle1 text-blue-10">Detalles</div>
                        <q-banner style="width:250px">                            
                            <div class="row">
                                <div class="col-9">Splits</div>
                                <div :class="determinar_color(props.row.serie_diaria_integridad.dsc_estado_split)">
                                    {{props.row.serie_diaria_integridad.dsc_estado_split}}
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-9">N. Dias de separacion</div>
                                <div :class="determinar_color(props.row.serie_diaria_integridad.dsc_est_num_dias_separacion)">
                                    {{props.row.serie_diaria_integridad.dsc_est_num_dias_separacion}}
                                </div>
                            </div>
                        </q-banner>                        
                    </q-popup-proxy>
                </q-td>
            </template>
            <template v-slot:body-cell-est_var_diaria="props">
                <q-td :props="props">                                        
                    <q-chip 
                    :color="determinar_color_chip(props.row.est_var_diaria)" 
                    size="12px" 
                    :class="determinar_color(props.row.est_var_diaria)">
                        <q-icon :name="determinar_icono(props.row.est_var_diaria)" class="q-pr-xs"/>{{ props.row.est_var_diaria }}
                    </q-chip>                                    
                </q-td>
            </template>
            <template v-slot:body-cell-est_serie_semanal="props">
                <q-td :props="props">                                        
                    <q-chip :color="determinar_color_chip(props.row.est_serie_semanal)" size="12px" 
                    :class="determinar_color(props.row.est_serie_semanal)">
                        <q-icon :name="determinar_icono(props.row.est_serie_semanal)" class="q-pr-xs"/>{{ props.row.est_serie_semanal }}
                    </q-chip>                                    
                </q-td>
            </template>
            <template v-slot:body-cell-est_var_semanal="props">
                <q-td :props="props">                                        
                    <q-chip :color="determinar_color_chip(props.row.est_var_semanal)" size="12px" 
                    :class="determinar_color(props.row.est_var_semanal)">
                        <q-icon :name="determinar_icono(props.row.est_var_semanal)" class="q-pr-xs"/>{{ props.row.est_var_semanal }}
                    </q-chip>                                    
                </q-td>
            </template>
            <template v-slot:body-cell-est_serie_mensual="props">
                <q-td :props="props">                                        
                    <q-chip :color="determinar_color_chip(props.row.est_serie_mensual)" size="12px" 
                    :class="determinar_color(props.row.est_serie_mensual)">
                        <q-icon :name="determinar_icono(props.row.est_serie_mensual)" class="q-pr-xs"/>{{ props.row.est_serie_mensual }}
                    </q-chip>                                    
                </q-td>
            </template>
            <template v-slot:body-cell-est_var_mensual="props">
                <q-td :props="props">                                        
                    <q-chip :color="determinar_color_chip(props.row.est_var_mensual)" size="12px" 
                    :class="determinar_color(props.row.est_var_mensual)">
                        <q-icon :name="determinar_icono(props.row.est_var_mensual)" class="q-pr-xs"/>{{ props.row.est_var_mensual }}
                    </q-chip>                                    
                </q-td>
            </template>
        </q-table>
        <q-dialog v-model="confirm_reparar" persistent>
            <q-card>
                <q-card-section class="row items-center">
                    <q-avatar icon="thumb_up_alt" color="primary" text-color="white" />
                    <span class="q-ml-sm">Deseas reparar el symbol <span class="text-primary text-bold">{{ cod_symbol_reparar }}</span>?</span>
                </q-card-section>
                <q-card-actions align="right">
                    <q-btn flat label="Cancel" color="primary" v-close-popup />
                    <q-btn label="Aceptar" color="primary" v-close-popup @click="reparar(cod_symbol_reparar)"/>
                </q-card-actions>
            </q-card>
        </q-dialog>
        <WinReprocesarSeries v-model="store.state.w_reprocesar.open"/>
    </div>    
</template>
<script>

import store from "./store"
import WinReprocesarSeries from "./WinReprocesarSeries"
import SerieApi from "@/api/serie.js"
import {HttpResponseHandler} from "@/common/http-response-handler.js"

export default {
    name:"TableResumenSerie",
    components:{
        WinReprocesarSeries
    },
    data: () => {
        return {
            store: store,
            confirm_reparar:false,
            cod_symbol_reparar:"",
            columns:[{
                label:"",
                align:"left",
                name:"menu",
                style:"width:10px;",                
                field:"menu"
            },{
                label:"Symbol",
                align:"left",   
                name:"cod_symbol",
                style:"width:50px",
                field:"cod_symbol"
            },{
                label:"Fch. primera serie",
                align:"left",
                name:"min_fch_serie",
                style:"width:90px",
                field:"min_fch_serie"
            },{
                label:"Fch. ultima serie",
                align:"left",
                name:"max_fch_serie",
                style:"width:90px",
                field:"max_fch_serie"
            },{
                label:"N. Series",
                align:"left",
                name:"num_series",
                style:"width:90px",
                field:"num_series"
            },{
                label:"N. dias desde ultima serie",                
                name:"num_dias_desde_ultima_serie",                
                style:"width:50px",                
                headerStyle: 'min-width: 100px;text-align:center;',                
                field:"num_dias_desde_ultima_serie"
            },{
                label:"Estado",
                align:"center",
                name:"estado",
                style:"width:100px",
                field:"estado"
            },{
                label:"Estado Series diarias",
                align:"left",
                name:"est_serie_diaria",
                style:"width:80px;",
                field:"est_serie_diaria"
            },{
                label:"Estado Variaciones diarias",
                align:"left",
                name:"est_var_diaria",
                style:"width:80px;",
                field:"est_var_diaria"
            },{
                label:"Estado Series semanales",
                align:"left",
                name:"est_serie_semanal",
                style:"width:80px;",
                field:"est_serie_semanal"
            },{
                label:"Estado Variaciones semanales",
                align:"center",
                name:"est_var_semanal",
                style:"width:80px;",                
                field:"est_var_semanal"
            },{
                label:"Estado Series Mensuales",
                align:"left",
                name:"est_serie_mensual",
                style:"width:80px;",
                field:"est_serie_mensual"
            },{
                label:"Estado Variaciones Mensuales",
                align:"left",
                name:"est_var_mensual",
                style:"width:80px;",
                field:"est_var_mensual"
            },{
                label:"",
                align:"",
                name:"",
                field:""
            }],
            data:[],
            pagination:{
                rowsPerPage:20
            }
        }
    },
    mounted:function(){
        //this.get_lista_fechas_maximas_x_symbol()
        this.recargar_datos()
    },
    methods:{
        /*
        get_lista_fechas_maximas_x_symbol:function(){
            this.$http.post(
                "/SerieManager/SerieController/get_lista_fechas_maximas_x_symbol",{},
                postconfig()
            ).then(httpresp => {
                this.$store.commit("messagebox",{"httpresp":httpresp,"mostrar_si_error":true}) 
                let appdata = httpresp.data
                this.data = appdata.data
            })
        },
        */
        determinar_icono: function(estado){
            if (estado == 'Correcto'){
                return "check_circle_outline"
            }
            if (estado == 'Defectuoso'){
                return "error_outline"
            }
        },
        determinar_color_chip_estado_general: function(estado){
            if (estado == 'Actualizado'){
                return "teal-1"
            }
            if (estado == 'Defectuoso'){
                return "deep-purple-1"
            }
            if (estado == 'Desactualizado'){
                return "amber-1"
            }
        },
        determinar_color_estado_general: function(estado){
            if (estado == 'Actualizado'){
                return "text-teal-10"
            }
            if (estado == 'Defectuoso'){
                return "text-deep-purple-10"
            }
            if (estado == 'Desactualizado'){
                return "text-amber-10"
            }
        },
        determinar_color_chip: function(estado){
            if (estado == 'Correcto'){
                return "green-1"
            }
            if (estado == 'Defectuoso'){
                return "red-1"
            }
            if (estado == 'Desactualizado'){
                return "amber-1"
            }
        },
        determinar_color: function(estado){
            if (estado == 'Correcto'){
                return "text-green"
            }
            if (estado.toUpperCase() == 'OK'){
                return "text-green"
            }
            if (estado == 'Defectuoso'){
                return " text-red"
            }
            if (estado.toUpperCase() == 'ERROR'){
                return " text-red"
            }
            if (estado == 'Desactualizado'){
                return " text-amber-10"
            }
        }/*,
        preguntar_confirmar_reparar: function(cod_symbol){
            this.confirm_reparar = true
            this.cod_symbol_reparar = cod_symbol
        }*/,        
        reparar: function(cod_symbol){
            let data = {
                "cod_symbol": cod_symbol
            }
            let response = new SerieApi().reparar(data)
            response.then(httpresp => {
                HttpResponseHandler.showMessage(httpresp)
            })
            response.finally(() => {
                this.recargar_datos()
            })
        },
        recargar_datos: async function(){
            //let data = await new SerieApi().get_lista_fechas_maximas_x_symbol()
            //store.state.t_resumen_data = data
            store.get_resumen_serie()
        }
    }
}
</script>