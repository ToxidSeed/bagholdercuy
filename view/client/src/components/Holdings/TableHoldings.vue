<template>
    <div>
        <q-table
        title="Acciones"
        :data="data"
        :columns="columns"
        row-key="name"
        separator="vertical"
        dense

        >
            <!--<template v-slot:top>
                <q-btn color="blue-10" label="Buy" @click="comprar()"/>                
                <q-btn color="red-10 " label="Sell" @click="vender()" class="q-ml-xs" />                
                <q-btn color="green" label="Options Chain" to="/order" class="q-ml-xs" />                
            </template>-->
            <template v-slot:body-cell-cod_symbol="props">                
                <q-td :props="props">                    
                    <q-menu
                    touch-position
                    context-menu
                    >
                    <q-list dense style="min-width: 100px" >
                        <q-item style="padding: 0px 0px" clickable v-close-popup @click="buy(props.row)">
                            <q-item-section class="bg-primary text-white"><div class="q-pl-sm">Buy</div></q-item-section>                                    
                        </q-item>
                        <q-item style="padding: 0px 0px" clickable v-close-popup @click="sell(props.row)">
                            <q-item-section class="bg-red text-white"><div class="q-pl-sm">Sell</div></q-item-section>                                    
                        </q-item>
                    </q-list>
                    </q-menu>
                    {{props.value}}
                </q-td>
            </template>
            <template v-slot:body-cell-total_change="props">
                <q-td :props="props">                    
                    <div v-bind:class="{'text-red':props.row.total_change < 0,'text-green':props.row.total_change >= 0}">
                        {{props.value}}%
                    </div>
                </q-td>                
            </template>
            <template v-slot:body-cell-total_pl="props">
                <q-td :props="props">
                    <div v-bind:class="{'text-red':props.row.total_change < 0,'text-green':props.row.total_change >= 0}">
                        {{props.value}}
                    </div>
                </q-td>                
            </template>                        
        </q-table>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue';
import {postconfig} from '@/common/request.js';
import date from 'date-and-time';

export default {
    name:"TableHoldings",
    components:{
        MessageBox
    },
    data: () => {        
        return {            
            columns:[
                {
                    label:"Instrumento",
                    align: 'left',
                    field:"cod_symbol",
                    name:"cod_symbol",
                    style:"width:150px;"                              
                },{
                    label:"En cartera desde",
                    align:"left",
                    field:"fch_primera_posicion",
                    name:"fch_primera_posicion",
                    style:"width:100px;"
                },{
                    label:"Cantidad",
                    align:"left",
                    field:"ctd_saldo_posicion",
                    name:"ctd_saldo_posicion",
                    style:"width:100px;"
                },
                {
                    label:"Imp. valor inicial posicion",
                    align:"right",
                    field:"imp_posicion_incial",
                    name:"imp_posicion_incial",
                    style:"width:100px;"                    
                },{
                    label:"Imp. valor minimo ",
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
                },{
                    label:"Imp. valor actual x accion",
                    align:"right",
                    field:"imp_valor_actual",
                    name:"imp_valor_actual",
                    style:"width:100px;"                    
                },{
                    label:"Imp. valor actual x posicion",
                    align:"right",
                    field:"imp_valor_actual_posicion",
                    name:"imp_valor_actual_posicion",
                    style:"width:100px;"                    
                },{
                    label:"Ganancia/Perdida",
                    align:"right",
                    field:"imp_ganancia",
                    name:"imp_ganancia",
                    style:"width:100px;"
                },{
                    label:"",
                    align:"left",
                    field:"",
                    name:""
                }
            ],            
            data:[],
            interval_id:null,      
            timeout_para_iniciar_id:null,      
            timeout_para_cerrar_id:null,            
            flg_usa_mercado_cerrado:'N'
        }
    },
    mounted:function(){        
        
        let fhr_dia = new Date()
        let fch_dia = date.format(fhr_dia,'YYYY/MM/DD')

        this.init(fch_dia)        
    },
    beforeDestroy:function(){       
        clearTimeout(this.timeout_para_cerrar_id)
        clearTimeout(this.timeout_para_iniciar_id)
        clearInterval(this.interval_id)
    },
    methods:{
        get_list:function(){
            if (this.interval_id != null){
                    clearInterval(this.interval_id)
            }

            this.$http.post(
            'holdings/PosicionAccionesReporter/get_posiciones',{
            },postconfig()).then(httpresp =>{                
                this.data = []
                this.$refs.msgbox.http_resp_on_error(httpresp)

                var appresp = httpresp.data
                if(appresp.success){                    
                    appresp.data.forEach(elem => {
                        elem.ctd_saldo_posicion = elem.ctd_saldo_posicion.toFixed(2)
                        elem.imp_posicion_incial = elem.imp_posicion_incial.toFixed(2)
                        elem.imp_min_accion = elem.imp_min_accion.toFixed(2)
                        elem.imp_max_accion = elem.imp_max_accion.toFixed(2)
                        elem.imp_posicion = elem.imp_posicion.toFixed(2)
                        elem.imp_prom_accion = elem.imp_prom_accion.toFixed(2)
                        elem.imp_valor_actual = "0.00"
                        elem.imp_valor_actual_posicion = "0.00"
                        elem.imp_ganancia = "0.00"
                        this.data.push(elem)
                    })                    
                    
                    //obtenemos las cotizaciones
                    this.get_cotizaciones()

                    this.iniciar_intervalo_ejecucion()
                }                                
            })
        },
        vender:function(){
            this.$emit('vender')
            
            let rname = this.$route.name
            if (rname != 'holdings-trade'){
                this.$router.push({name:'holdings-trade'})
            }            
        },
        comprar:function(){
            this.$emit('comprar')

            let rname = this.$route.name
            if (rname != 'holdings-trade'){
                this.$router.push({name:'holdings-trade'})
            }            
        },
        iniciar_intervalo_ejecucion: function(){                                   
            var self = this         
            
            clearTimeout(this.timeout_para_cerrar_id)
            clearTimeout(this.timeout_para_iniciar_id)
            clearInterval(this.interval_id)
            
            if (this.flg_usa_mercado_cerrado == "S"){
                return
            }

            let fchr_dia = new Date()
            let fch_dia = date.format(fchr_dia,"YYYY-MM-DD")
            let hr_apertura_mercado = "08:30:00"
            let hr_cierre_mercado = "15:00:00"

            let fchr_apertura_mercado = date.parse(fch_dia+" "+hr_apertura_mercado, "YYYY-MM-DD HH:mm:ss")
            let fchr_cierre_mercado = date.parse(fch_dia+" "+hr_cierre_mercado, "YYYY-MM-DD HH:mm:ss")

            let tiempo_para_iniciar = fchr_apertura_mercado - fchr_dia
            let tiempo_para_cerrar = fchr_cierre_mercado - fchr_dia

            /*
            Si el tiempo para cerrar es positivo, entonces programamos la eliminacion del intervalo
            */            
            if (tiempo_para_cerrar >= 0){
                self.timeout_para_cerrar_id =  setTimeout(() => {      
                    console.log("tiempo para cerrar")              
                    clearInterval(this.interval_id)
                },
                tiempo_para_cerrar
                )
            }

            //Si el tiempo para cerrar es negativo, quiere decir que el mercado ya cerró
            if (tiempo_para_cerrar < 0){
                return
            }

            /*
            Si tiempo para iniciar es mayor a 0
            */
            if (tiempo_para_iniciar >= 0){
                self.timeout_para_iniciar_id =  setTimeout(() => {
                    self.interval_id = setInterval(
                        self.get_cotizaciones(),
                        15000
                    )
                },
                tiempo_para_iniciar
                )                
            }
            
            /*
            Si el tiempo para inicar es menor a 0 es que ya no se debe esperar para iniciar
            */
           if (tiempo_para_iniciar < 0){                
                self.interval_id = setInterval(() => {   
                    //console.log(new Date())                 
                    self.get_cotizaciones()
                },15000
                )
           }            
        },
        get_cotizaciones: function(){           
            this.data.forEach( async(elem) => {                                
                let res = await this.$http.post(
                'cotizacion/CotizacionManager/get_cotizacion',{
                    cod_symbol:elem.cod_symbol
                },
                postconfig()
                )
                let appdata = res.data.data            
                elem.imp_valor_actual = appdata.imp_cierre.toFixed(3)   
                elem.imp_valor_actual_posicion = (appdata.imp_cierre * elem.ctd_saldo_posicion).toFixed(2)
                elem.imp_ganancia = (elem.imp_valor_actual_posicion - elem.imp_posicion_incial).toFixed(2)
                     
            })                                                     
        },
        init:async function(fch_dia){

            let resp = await this.$http.post(
                'calendariodiario/CalendarioDiarioManager/get_datos_fecha',{
                    fch_dia: fch_dia
                },
                postconfig()
            )
            
            let datos_dia = resp.data.data            
            this.flg_usa_mercado_cerrado = datos_dia.flg_usa_mercado_cerrado    



            this.get_list()
        }
    }
}
</script>
