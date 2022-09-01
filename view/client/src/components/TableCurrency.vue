<template>
    <div>
        <q-table
            title="Monedas"
            :data= "data"
            :columns = "columns"
            row-key="symbol"
            dense
            separator="vertical"
            :visible-columns="visible_columns"
            @row-dblclick="row_dblclick"
            :pagination=pagination
        >
            <template v-slot:top>       
                <div class="column">             
                  <div class="col-2 q-table__title text-primary">Monedas</div>                                                        
                  <div>
                      <q-btn color="primary" label="Nuevo" @click="btn_nuevo_click"/>                  
                  </div>
                </div>
            </template>
        </q-table>
    </div>
</template>
<script>
export default {
    name:"TableCurrency",
    data: () => {
        return {
            columns:[
                {
                    label:"Id",
                    align:"left",
                    field:"moneda_id",
                    name:"moneda_id"
                },
                {
                    label:"ISO",
                    align:"left",
                    field:"codigo_iso",
                    name:"codigo_iso"
                },{
                    label:"Nombre",
                    align:"left",
                    field:"nombre",
                    name:"nombre"
                },{
                    label:"Fch. Registro",
                    align:"left",
                    field:"fec_registro",
                    name:"fec_registro"
                },{
                    label:"",
                    align:"left",
                    field:"",
                    name:""
                }
            ],
            visible_columns:["codigo_iso","nombre","fec_registro",""],
            pagination:{
                rowsPerPage:30
            },
            data:[]
        }
    },
    mounted:function(){
        this.get_currency_list()
    },
    methods:{
        get_currency_list:function(){
            this.$http.post('CurrencyManager/CurrencyFinder/get_list',{

            }).then(httpresponse => {
                var appdata = httpresponse.data
                this.data = appdata.data
            })
        },
        row_dblclick:function(event, row){                 
            /*event = null
            this.$emit("row-dblclick",row)*/
            let moneda_id = row.moneda_id             
            this.$router.push("/currency/edit="+moneda_id)
        },
        btn_nuevo_click:function(){
            this.$router.push("/currency/new?ts="+Date.now())
        }
    }
}
</script>