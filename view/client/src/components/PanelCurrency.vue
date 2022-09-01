<template>
    <div>
        <q-card flat style="min-height: 40vh;">
            <q-card-section>
                <div class="text-bold text-primary text-h6">Moneda</div>
            </q-card-section>
            <q-card-section>
                <div class="row">
                    <q-input stack-label :disable="edit_disable" v-model="codigo_iso" label="ISO" class="col-2 text-uppercase" label-color="indigo"/>
                    <q-input stack-label v-model="simbolo" label="Simbolo" class="col-2 q-pl-xs" @change="symbol_update_handler"/>                                    
                    <q-input stack-label v-model="nombre" label="Nombre" class="col-8 q-pl-xs" @change="symbol_update_handler"/>
                </div>                
                <q-input stack-label v-model="descripcion" label="Descripción"/>                
            </q-card-section>
            <!--<q-card-actions align="right">
                <q-btn color="primary" @click="btn_save_click_handler">Guardar</q-btn>
                <q-btn color="orange">Cancelar</q-btn>                
            </q-card-actions>-->
        </q-card>
        <MessageBox ref="msgbox"/>  
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue'

export default {
    name:"PanelCurrency",
    components:{
        MessageBox
    },
    props:{
        in_data:{
            type:Object,
            default: () => {}
        },
        in_moneda_id:{
            type:String,
            default:""
        }
    },
    data: () => {
        return {
            moneda_id:"",
            codigo_iso:"",
            simbolo:"",
            nombre:"",
            descripcion:"",
            fec_registro:"",
            fec_audit:""
        }
    },
    watch:{
        in_moneda_id:function(new_value){    
            this.moneda_id = new_value            
        },
        moneda_id:function(newval){
            if (newval == ""){
                this.ini_campos()
            }else{
                this.cargar_datos_cliente(newval)
            }            
        }
    },
    computed:{
        edit_disable:function(){
            if(this.moneda_id == ""){
                return false
            }else{
                return true
            }
        }
    },
    mounted:function(){
        this.moneda_id = this.in_moneda_id        
    },
    methods:{
        cargar_datos_cliente:function(moneda_id){
            console.log(moneda_id)
            this.$http.post(
                'CurrencyManager/CurrencyFinder/get_data',{
                    "moneda_id":moneda_id
                }
            ).then(httpresp => {
                let appdata = httpresp.data
                if (appdata.success == false){
                    this.$refs.msgbox.httpresp(httpresp)
                }else{
                    //setting the data
                    let data = appdata.data
                    this.moneda_id = data.moneda_id
                    this.codigo_iso = data.codigo_iso
                    this.simbolo = data.simbolo
                    this.nombre = data.nombre
                    this.descripcion = data.descripcion
                }                
            })
        }, 
        ini_campos:function(){
            this.codigo_iso = ""
            this.simbolo = ""
            this.nombre = ""
            this.descripcion = ""
        },    
        symbol_update_handler:function(){            
            this.$emit("symbol-changed", {"new":this.symbol})
        },
        btn_save_click_handler:function(){
            this.$emit("btn-save-click")
        }
    },
    beforeDestroy:function(){
        this.$emit('panel-close',this.$data)
    },
    created:function(){
        /*if (Object.keys(this.in_data).length != 0){            
            this.currency_id = this.in_data.currency_id
            this.symbol = this.in_data.symbol
            this.currency_name = this.in_data.currency_name
        }*/
    }
}
</script>