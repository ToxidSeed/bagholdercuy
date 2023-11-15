<template>
    <div>
        <q-table
            :data="data"
            title="Monitoreo"
            title-class="text-blue-10"
            :columns="columns"
            row-key="name"            
            dense
            hide-header            
            separator="vertical"
            :pagination="pagination"
        >            
        
            <template v-slot:body="props">                
                <q-tr>                    
                    <q-td colspan="3" @click="get_alertas">
                        <div class="row">
                            <div class="text-blue-10 col-11" >
                                {{ props.row.cod_symbol }}
                            </div>
                            <div>                                
                                <q-btn icon="notifications" flat color="orange" dense round @click="btn_alerta_click(props.row.id_monitoreo)"/>
                            </div>
                            <div class="col-12">
                                {{ props.row.nom_symbol }}
                            </div>
                        </div>                        
                        <div class="row q-gutter-md">
                            <div class="col3">
                                <div>Imp. cierre anterior</div>
                                <div class="text-right">{{ props.row.imp_cierre_anterior }}</div>
                            </div>
                            <div class="col3">
                                <div>Imp. actual</div>
                                <div class="text-right">{{ props.row.imp_actual }}</div>
                            </div>
                        </div>      
                        <q-separator/>                  
                    </q-td>
                </q-tr>                                                                    
            </template>
        </q-table>            
    </div>
</template>
<script>
import {postconfig} from "@/common/request.js"

export default {
    name:"TableMonitoreo",
    components:{
    },
    data(){
        return {
            data:[{
                id_monitoreo:1,
                id_symbol: 1,
                cod_symbol: 'SOXL',
                nom_symbol: 'DIREXION DAILY SEMIS',
                imp_cierre_anterior: 22.5,
                imp_actual:0,
                imp_variacion:-22.5,
                pct_variacion: 100
            }],
            columns:[{
                name:'id_monitoreo',
                label:'ID',
                align:'left',
                field:'id_monitoreo'
            },{
                name:'id_symbol',
                label:'Id Symbol',
                align:'left',
                field:'id_symbol'
            },{
                name:'cod_symbol',
                label:'Cod. Symbol',
                align:'left',
                field:'cod_symbol'
            },{
                name:'Nombre',
                label:'Nom. symbol',
                align:'left',
                field:'nom_symbol'
            },{
                name:'imp_cierre_anterior',
                label:'Imp. cierre anterior',
                align:'left',
                field:'imp_cierre_anterior'
            },{
                name:'imp_actual',
                label:'Imp. actual',
                align:'left',
                field:'imp_actual'
            },{
                name:'imp_variacion',
                label:'Imp. variacion',
                align:'left',
                field:'imp_variacion'
            },{
                name:'pct_variacion',
                label:'Pct. variacion',
                align:'left',
                field:'pct_variacion'
            }],
            pagination:{
                rowsPerPage:15
            },
            WinManagerFuturaOperacion:{
                open:false
            }
        }
    },
    mounted:function(){
        this.init()
    },
    methods:{
        init:function(){
            this.get_list()
        },        
        get_list:async function(){
            let monitoreo_activo_data = await this.get_monitoreo_activo()
            this.data = monitoreo_activo_data

            await Promise.all(this.data.map(async (element) => {
                let cotizacion = await this.get_cotizacion(element.cod_symbol)                
                this.$set(element, "imp_actual", cotizacion.imp_cierre)
                this.$set(element, "imp_cierre_anterior", cotizacion.imp_cierre_anterior)
            }))
        },
        get_monitoreo_activo:async function(){            
            let httpresp = await this.$http.post(
                "/monitoreo/MonitoreoController/get_monitoreo_activo",{
                    id_cuenta: localStorage.getItem("id_cuenta")
                },postconfig()
            )

            this.$store.commit("message",{"httpresp":httpresp, "mostrar_si_error":true})
            return httpresp.data.data
        },
        get_cotizacion:async function(cod_symbol){            
            const httpresp = await this.$http.post(
                "/cotizacion/CotizacionManager/get_cotizacion",{
                    cod_symbol: cod_symbol
                },
                postconfig()
            )
            
            this.$store.commit("message",{"httpresp":httpresp,"mostrar_si_error":true})
            return httpresp.data.data
        },
        get_alertas:function(){
            console.log("alertas")
        },
        btn_alerta_click:function(id_monitoreo){
            console.log(id_monitoreo)

            this.$emit("btn-alerta-click",{
                id_monitoreo:id_monitoreo
            })
        }
    }
}
</script>