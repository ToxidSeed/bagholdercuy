<template>
    <div>
        <q-toolbar>
            <q-toolbar-title class="text-blue-10">Broker</q-toolbar-title>
        </q-toolbar>
        <div class="row q-col-gutter-xs">
            <div class="col-4" v-if="lpanel_visible==true">
                <router-view
                    v-on:reload-brokers="get_brokers"
                />
            </div>
            <div class="col">
                <q-toolbar>
                    <q-btn label="Nuevo" color="blue-10" class="text-capitalize" icon="add" :to="{name:'broker-new'}"/>
                </q-toolbar>
                <TableListaBrokers ref="TableListaBrokers"/>            
            </div>
        </div>
    </div>
</template>
<script>
import TableListaBrokers from '@/components/broker/TableListaBrokers.vue'
export default {
    name:"MainBroker",
    components:{
        TableListaBrokers
    },
    props:{
        action:{
            type:String,
            default:""
        }
    },
    data (){
        return {
            lpanel_visible:false
        }
    },
    watch:{
        $route: function(){
            this.habilitar()
        }
    },
    mounted:function(){
        this.habilitar()                
    },
    methods:{
        habilitar:function(){
            if (this.$route.name == "broker"){
                this.lpanel_visible = false
            }
            if (this.$route.name == "broker-new"){
                this.lpanel_visible = true
            }
            if (this.$route.name == "broker-ver"){
                this.lpanel_visible = true
            }
            if (this.$route.name == "broker-editar"){
                this.lpanel_visible = true
            }
        },
        get_brokers:function(){            
            this.$refs.TableListaBrokers.get_brokers()
        }
    }    
}
</script>