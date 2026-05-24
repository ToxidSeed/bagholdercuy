<template>
    <div>
        <q-separator/>
        <q-table
        :data="data"
        :columns="columns"
        row-key="id"
        separator="cell"        
        dense
        flat
        @row-dblclick="onRowDblclick"
        >				                
        </q-table>
                
    </div>
</template>
<script>

import {postconfig} from '@/common/request.js';

import store from "@/store/store"

export default {
    name:"TableIbkrOperaciones",
    components:{
        
    },
    data: () => {        
        return {            
            columns:[
                { name: 'id_importacion', label: 'ID Importación', field: 'id_importacion', align: 'left', sortable: true },
                { name: 'cod_origen', label: 'Origen', field: 'cod_origen', align: 'left', sortable: true },
                { name: 'tipo_dataset', label: 'Tipo Dataset', field: 'tipo_dataset', align: 'left', sortable: true },
                { name: 'nombre_archivo', label: 'Archivo', field: 'nombre_archivo', align: 'left', sortable: true },
                { name: 'hash_archivo', label: 'Hash', field: 'hash_archivo', align: 'left', sortable: true },
                { name: 'total_registros', label: 'Total', field: 'total_registros', align: 'right', sortable: true },
                { name: 'registros_ok', label: 'OK', field: 'registros_ok', align: 'right', sortable: true },
                { name: 'registros_error', label: 'Error', field: 'registros_error', align: 'right', sortable: true },
                { name: 'estado', label: 'Estado', field: 'estado', align: 'center', sortable: true },
                { name: 'fch_importacion', label: 'Fecha Importación', field: 'fch_importacion', align: 'left', sortable: true },
                { name: 'fch_procesado', label: 'Fecha Procesado', field: 'fch_procesado', align: 'left', sortable: true }
            ],
            data:[]
        }
    },
    mounted:function(){        
        this.get_list()        
    },
    methods:{
        onRowDblclick: function(evt, row) {
            this.$router.push({ name: 'generar-transacciones-ibkr', query: { id_importacion: row.id_importacion } })
        },
        get_list:function(){
            this.$http.post(
            'operacion/IbkrLoaderController/get_ibkr_import_trades',{
                id_cuenta: localStorage.getItem("id_cuenta")
            },postconfig()).then(httpresp =>{                
                this.data = []                
                store.dispatch('incluir_httpresp_si_apperror', httpresp);

                var appresp = httpresp.data
                if(appresp.success){  
                    appresp.data.forEach(elem => {                        
                        this.data.push(elem)
                    })                        
                }                                
            }).catch(error => {
                console.error("Error cargando operaciones IBKR", error)
            })
        }
    }
}
</script>
<style scoped lang="scss">
.q-table__container{
    min-height: 80vh !important;
}
</style>