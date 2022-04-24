<template>
    <div>
        <q-card>
            <q-toolbar class="text-primary">      
                <q-toolbar-title>
                    Symbols
                </q-toolbar-title>      
            </q-toolbar>
            <q-card-section>                
                <div class="row">
                    <q-input label="ID" readonly v-model="symbol_id" class="col-5"/>
                    <q-input label="symbol" v-model="symbol" class="col-7 q-pl-xs"/>                    
                </div>
                <q-input label="Name" v-model="name" />
                <div class="row">
                    <q-input label="Region" v-model="region" class="col-5"/>
                    <q-input label="Exchange" v-model="exchange" class="col-7 q-pl-xs"/>
                </div>
                <div class="row">
                    <q-input readonly label="Fch. Registro" v-model="fec_registro" class="col-5 q-pl-xs"/>
                    <q-input readonly label="Fch. Audit" v-model="fec_audit" class="col-7 q-pl-xs"/>
                </div>
            </q-card-section>
            <q-card-actions>
                <q-btn label="aceptar" color="primary" @click="save"/>
                <q-btn label="cancelar"/>
            </q-card-actions>
        </q-card>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '../MessageBox.vue'
export default {
    name:"PanelSymbol",
    components:{
        MessageBox
    },
    data: () => {
        return {
            symbol_id:"#",
            symbol:"",
            name:"",
            region:"",
            exchange:"",
            fec_registro:"",
            fec_audit:""
        }
    },
    mounted:function(){
        
    },
    methods:{
        save:function(){
            this.$http.post('SymbolManager/SymbolManager/save',{
                symbol_id:this.symbol_id,
                symbol:this.symbol,
                symbol_name: this.name,
                region:this.region,
                exchange:this.exchange,
                asset_type:""
            }).then(httpresponse => {
                var appdata = httpresponse
                this.$refs.msgbox.new(appdata.data)
            })
        }
    }
}
</script>