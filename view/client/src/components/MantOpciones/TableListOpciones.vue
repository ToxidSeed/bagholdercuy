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
        </q-table>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue'
import date from 'date-and-time'
import {CLIENT_DATE_FORMAT, ISO_DATE_FORMAT} from '@/common/constants.js'

export default {
    name:"TableListOpciones",
    components:{
        MessageBox
    },
    props:{
        throwerror:{
            type:Boolean,
            default:false
        }
    },
    data: () => {
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
            }            
        }
    },
    mounted:function(){
        this.get_list_contratos()
    },
    methods:{
        get_list_contratos:function(){
            this.$http.post('/OpcionesContrato/OpcionesContratoManager/get_list_contratos').then(
                httpresp => {
                    let appresp = httpresp.data
                    if(appresp.success == false){
                        if(this.throwerror == true){
                            this.$emit('httperror',httpresp)
                        }else{                            
                            this.$refs.msgbox.httpresp(httpresp)
                        }
                        return
                    }                    
                    this.data = []
                    appresp.data.forEach(element => {
                        element.fch_expiracion = date.transform(element.fch_expiracion,ISO_DATE_FORMAT, CLIENT_DATE_FORMAT)
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