<template>
    <div >
        <q-table
            title="Funds"
            :data = "data"
            :columns = "columns"
            row-key="name"
            dense
            separator="vertical"
        >
        </q-table>
        <MessageBox ref="msgbox"/>
    </div>
</template>
<script>
import MessageBox from '@/components/MessageBox.vue'
export default {
    name:"TableFunds",
    components:{
        MessageBox
    },
    data: () => {
        return {
            data:[],
            columns:[{
                label:"Moneda",
                align:"left",
                field:"moneda",
                name:"moneda",
                style:"width:100px;"
            },{
                label:"Importe",
                align:"right",
                field:"importe_fmt",
                name:"importe",
                style:"width:100px;"
            },{
                label:"",
                align:"left",
                field:"",
                name:""
            }]
        }
    },
    mounted:function(){
        this.get_funds()
    },
    methods:{
        get_funds:function(){
            this.data = []
            this.$http.post('FundsManager/FundsManager/get_funds',{
                symbol:""
            },{
                headers:{
                    'Authorization':localStorage.getItem('token')
                }
            }).then(httpresp => {
                var appresp = httpresp.data
                if (appresp.success == false){
                    this.$refs.msgbox.httpresp(httpresp)
                    if (appresp.expired == true){
                        this.$router.push({name:"login"})
                    }                    
                }else{
                    appresp.data.forEach(element => {
                        element.importe = element.importe.toFixed(2)
                        this.data.push(element)
                    });                                    
                }
            })
        }
    }
}
</script>