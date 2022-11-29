<template>
    <div>
        <q-card no-shadow>
            <q-card-section class="q-pb-none q-pt-sm">
                <div class="row">
                    <div class="text-h6 text-blue-10">Reorganizar Fondos</div>
                    <q-space/>
                    <q-btn  flat dense rounded color="red" icon="close" :to="{name:'funds'}"/>
                </div>
            </q-card-section>
            <q-card-section class="q-pt-none">
                <q-btn label="Procesar" color="green" @click="procesar"/>
                <div class="row justify-between">
                    <div class="q-pt-md text-subtitle2 text-blue-10">Reorganizar fecha: 
                        <span class="text-h6 text-black">{{filter.fch_transaccion}}</span>                                                
                    </div>                    
                    <div>
                        <q-btn class="q-ml-xs" label="Buscar" no-caps color="secondary" @click="buscar"/>
                    </div>
                </div>
            </q-card-section>            
        </q-card>        
        <TableTransaccionesFondosFecha 
            ref="TableTransaccionesFondosFecha"
            v-bind:filter="filter"
        />
        <HelperFechasTransaccionesFondos 
            v-model="visible.helper_trans_fondos"
            v-on:select="select"
        />
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue';
import {headers} from '@/common/common.js';
import HelperFechasTransaccionesFondos from '@/components/helpers/HelperFechasTransaccionesFondos.vue';
import TableTransaccionesFondosFecha from '@/components/Funds/TableReorganizarFondos.vue';

export default {
    name:"PanelReorganizarFondos",
    components:{
        TableTransaccionesFondosFecha,
        HelperFechasTransaccionesFondos,
        MessageBox
    },
    data: () => {
        return {
            filter:{
                fch_transaccion:"No seleccionada"
            },            
            visible:{
                helper_trans_fondos:false
            }                    
        }
    },
    methods:{
        buscar:function(){            
            this.visible.helper_trans_fondos = true
        },
        select:function(row){                        
            this.filter = {
                fch_transaccion:row.fch_transaccion
            }
            console.log('cambiar-fecha')
            this.$emit('cambiar-fecha',row.fch_transaccion)   
        },
        procesar:function(){
            //console.log(this.$refs)
            let list_trans = this.$refs.TableTransaccionesFondosFecha.data
            let list_eliminar = this.$refs.TableTransaccionesFondosFecha.list_eliminar
            let data = {
                fch_transaccion: this.filter.fch_transaccion
            }

            this.$http.post(
                '/FundsManager/ReorganizarController/procesar',{
                    fch_reorganizar: this.filter.fch_transaccion,
                    list_trans: list_trans,
                    list_eli_trans: list_eliminar
                },
                {
                    headers:headers()
                }
            ).then(httpresp => {
                this.$refs.msgbox.http_resp(httpresp)
            }).finally(() => {                
                this.$refs.TableTransaccionesFondosFecha.get_transacciones_x_fecha(this.filter.fch_transaccion)
                this.$emit("procesar-fin",data)
            })            
        }
    }
}
</script>