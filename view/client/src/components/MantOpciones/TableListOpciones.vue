<template>
    <div>
        <q-table
            :columns="columns"
            :data="data"
            row-key="id"
            dense
            :pagination="pagination"
            separator="vertical"
        >
            <template v-slot:body="props">
                <q-tr :props="props">
                    <q-menu
                    touch-position
                    context-menu
                    >
                        <q-list dense>
                            <q-item clickable v-close-popup class="bg-green text-white" @click="copiar(props.row)">
                                <q-item-section >Copiar Opcion</q-item-section>
                            </q-item>
                        </q-list>
                    </q-menu>
                    <q-td key="moneda_id" :props="props">
                        {{ props.row.moneda_id }}
                    </q-td>
                    <q-td key="symbol" :props="props">
                        {{ props.row.symbol }}
                    </q-td>
                    <q-td key="descripcion" :props="props">
                        {{ props.row.descripcion }}
                    </q-td>
                    <q-td key="subyacente" :props="props">
                        {{ props.row.subyacente }}
                    </q-td>
                    <q-td key="lado" :props="props">
                        {{ props.row.lado }}
                    </q-td>
                    <q-td key="strike" :props="props">
                        {{ props.row.strike }}
                    </q-td>
                    <q-td key="fch_expiracion" :props="props">
                        {{ props.row.fch_expiracion }}
                    </q-td>
                </q-tr>                                
            </template>
        </q-table>
        <MessageBox :config="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue'
import date from 'date-and-time'
import {CLIENT_DATE_FORMAT, ISO_DATE_FORMAT} from '@/common/constants.js'
import {postconfig} from '@/common/request.js'

export default {
    name:"TableListOpciones",
    components:{
        MessageBox
    },
    props:{
        infiltros:{
            type:Object,
            default:() => {}
        }
    },
    data(){
        return {
            columns:[{
                label:"moneda_id",
                align:"left",
                field:"moneda_id",
                name:"moneda_id",
                style:"width:50px;"
            },{
                label:"Symbol",
                align:"left",
                field:"symbol",
                name:"symbol",
                style:"width:100px;"
            },
            {
                label:"descripcion",
                align:"left",
                field:"descripcion",
                name:"descripcion",
                style:"width:250px;"
            },{
                label:"subyacente",
                align:"left",
                field:"subyacente",
                name:"subyacente",
                style:"width:50px;"
            },{
                label:"C/P",
                align:"left",
                field:"lado",
                name:"lado",
                style:"width:50px;"
            },{
                label:"Strike",
                align:"right",
                field:"strike",
                name:"strike",
                style:"width:50px;"
            },{
                label:"Fch. Expiración",
                align:"left",
                field:"fch_expiracion",
                name:"fch_expiracion",
                style:"width:50px;"
            },{
                label:"",
                align:"left",
                field:"",
                name:""
            }],
            data:[],
            pagination:{
                rowsPerPage:20
            },
            caller:this.$options._componentTag,
            msgbox:{},
            filtros:{
                cod_symbol:"",
                sentidos:[],
                fch_expiracion:"",
                imp_ejercicio:0
            }
        }
    },
    watch:{
        infiltros:function(newval){
            this.id_contrato_opcion = newval.id_contrato_opcion
            this.cod_symbol = newval.cod_symbol
            this.sentidos = newval.sentidos
            this.fch_expiracion = newval.fch_expiracion
            this.imp_ejercicio = newval.imp_ejercicio

            //
            this.get_list_contratos()
        }
    },
    mounted:function(){
        this.get_list_contratos()
    },
    methods:{
        copiar:function(row){
            this.$emit('copiar',row)
        },
        get_list_contratos:function(){      

            //console.log("xxx")      
            this.$http.post(
                '/OpcionesContrato/OpcionesContratoManager/get_contratos',
                {
                    id_contrato_opcion: this.id_contrato_opcion,
                    cod_symbol: this.cod_symbol,
                    sentidos: this.sentidos,
                    fch_expiracion: this.fch_expiracion,
                    imp_ejercicio: this.imp_ejercicio
                },
                postconfig()
            ).then(
                httpresp => {
                    let appresp = httpresp.data                    
                    this.msgbox = {
                        httpresp:httpresp,
                        onerror:true,
                        caller:this.caller
                    }

                    if (appresp.success == false){
                        return
                    }

                    this.data = []
                    appresp.data.forEach(element => {                        
                        element.descripcion = element.description
                        element.lado = element.side
                        element.subyacente = element.underlying
                        element.fch_expiracion = date.transform(element.expiration_date,ISO_DATE_FORMAT, CLIENT_DATE_FORMAT)
                        this.data.push(
                            element
                        )
                    })
                }
            )
        }
    }
}
</script>