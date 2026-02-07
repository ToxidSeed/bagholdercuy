<template>
    <div>
        
    </div>
</template>
<script>
import MessageBox from '../MessageBox.vue'
import {postconfig} from '@/common/request.js'

export default {
    name:"PanelSymbol",
    components:{
        MessageBox
    },
    data: () => {
        return {
            loading:false,
            confirm:false,
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
            this.loading=true
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
            }).catch(error => {
                console.log(error)
            }).then(()=>{
                this.loading=false
            })
        },
        load:function(){
            this.loading=true
            this.$http.post('/SymbolManager/DataLoader/do',{},postconfig())
            .then(httpresp => {                
                this.$refs.msgbox.httpresp(httpresp)
            }).catch(error => {
                console.log(error)
            }).then(() => {
                this.loading = false
            })
        }
    }
}
</script>