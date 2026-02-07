<template>
    <div>
        <q-dialog v-model="open">
            <PanelTrade @btn-close-click="close"/>
        </q-dialog>        
    </div>
</template>
<script>
//import {get_postconfig} from "@/common/request.js"
import PanelTrade from './PanelTrade.vue';

export default {
    name:"WinTrade",
    props:{
        value:{
            required:true
        }
    },
    components:{        
        PanelTrade
    },
    watch:{
        open:function(newval){
            this.$emit('input',newval)
        },  
        value:function(newval){
            this.open = newval
        }
    },    
    data(){
        return {
            open: this.value,
        }
    },
    methods:{
        close:function(){            
            this.open = false
        }
    }
}

</script>