<template>
    <q-dialog v-model="localValue">
        <q-card style="min-width:400px;">                        
            <q-toolbar>
                <q-icon name="contact_support" size="xs" color="deep-orange-10"/>
                <q-toolbar-title class="q-pt-xs text-subtitle1 text-deep-orange-10">{{ config.title }}</q-toolbar-title>           
                <q-btn icon="close" color="red" flat/>                     
            </q-toolbar>
            <q-separator/>
            <q-card-section class="row items-center">
            <!--<q-avatar icon="question_mark" text-color="blue-10"/>-->
            <span class="q-ml-sm text-subtitle2">{{config.msg}}</span>
            </q-card-section>
            <q-separator/>
            <q-card-actions align="right">
                <q-btn label="Si" color="primary" v-close-popup @click="btn_si_click_handler"/>
                <q-btn flat label="Cancel" color="red" v-close-popup />            
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>
<script>
export default {
    name:"Confirmar",
    props:{
        value:{
            required:true
        },
        msg:{
            type:String,
            default:""
        },
        callback:{
            type:String,
            default:"ok"
        },
        config:{
            type: Object,
            default: () => {
                return {
                    title:"",
                    msg:"",
                    callback:() => {}
                }
            }
        }
    },
    data(){
        return {
            localValue:this.value
        }
    },
    watch:{
        localValue:function(newval){
            this.$emit('input', newval)
        },
        value:function(newval){
            this.localValue = newval
        }
    },
    methods:{
        btn_si_click_handler:function(){            
            this.localValue = false
            //this.$emit(this.config.callback)
            this.$emit("ok")
        }
    }
}
</script>
<style scoped>
.q-toolbar {
    min-height: auto;
}
</style>