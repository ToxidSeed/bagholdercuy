<template>
    <div>
        <q-select
            ref="select"
            :label="label"
            v-model="selected"
            use-input    
            hide-selected                  
            stack-label            
            input-debounce="500"
            @filter="filter_fn"
            @input="sel_item"
            :options="list"            
            options-dense            
            color="blue-10"
        >
            <template v-slot:before-options>
                <q-item clickable dense class="text-red" @click="select_no_opcion">
                    <q-item-section >
                        Sin seleccion
                    </q-item-section>
                </q-item>
            </template>
        </q-select>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import {postconfig} from '@/common/request.js';
import MessageBox from '@/components/MessageBox.vue';

export default {
    name:"SelectCuenta",
    props:{
        flg_activo:{
            type:Number,
            default:1
        },
        label:{
            type:String,
            default:"Seleccionar Cuenta"
        },
        id_usuario:{
            type:String,
            default:""
        },
        ocultar_sel:{
            type:Boolean,
            default:false
        }
    },
    data() {
        return {
            selected:"",
            list:[]
        }
    },
    components:{
        MessageBox
    },
    methods:{
        sel_item:function(selected){            
            if (selected == null){
                console.log("xx")
                this.$emit('deselect')                
            }else{                
                /*if (this.ocultar_sel == false){                    
                    this.selected = selected
                }else{
                    this.selected = ""
                }   */              
                this.selected = ""               
                this.$emit('select',selected)            
            }
        },
        filter_fn:function(val, update){            
            this.$http.post('/cuenta/CuentaManager/get_cuentas_x_usuario',{
                text:val,
                id_usuario: this.id_usuario
            },postconfig()).then(httpresponse => {
                this.$refs.msgbox.http_resp_on_error(httpresponse)

                var appdata = httpresponse.data
                var options = []
                for (let elem of appdata.data){
                    options.push({
                        "value":elem["id_cuenta"],
                        "label":elem["cod_cuenta"] + " - " + elem["nom_cuenta"]
                    })
                }
                
                update(() =>{
                    this.list = options
                })
            })
        },
        select_no_opcion:function(){
            this.$refs.select.hidePopup () 
            this.$emit('select',{
                "value":"",
                "label":""
            })
        }
    }
}
</script>