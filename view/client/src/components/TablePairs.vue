<template>
    <div>        
        <q-table
            title="Pares"
            :data = "data"
            :columns = "columns"
            row-key = "pair_name"
            dense
            selection="multiple"
            :selected.sync="selected"
        >
             <template v-slot:top>                 
                 <q-btn color="red" label="remove selected" @click="remove_selected" />                 
            </template>
        </q-table>
    </div>
</template>
<script>
export default {
    name:"TablePairs",
    props:{
        in_data:{
            type:Object,
            default: () => {}
        },
        moneda_id:{
            type:String,
            default:""
        }
    },        
    data:() => {
        return {
            selected:[],
            columns:[
                {
                    label:"ID",
                    align:"left",
                    field:"par_id",
                    name:"par_id"
                },
                {
                    label:"Par",
                    align:"left",
                    field:"nombre",
                    name:"nombre"
                },
                {
                    label:"Operacion",
                    align:"left",
                    field:"operacion",
                    name:"operacion"
                }
                ],
            data:[],
            deleted_records:[]
        }
    },
    watch:{
        moneda_id:function(newval){
            if (newval == ""){
                this.data = []
            }else{
                this.actualizar_lista()
            }
        }
    },
    methods:{       
        actualizar_lista:function(){
            this.$http.post(
                '/CurrencyManager/ParFinder/get_list_x_mon',{
                    moneda_id:this.moneda_id
                }
            ).then(httpresp => {
                let appresp = httpresp.data
                this.data = appresp.data
                if (appresp.success == false){
                    this.$refs.msgbox.httpresp(httpresp)
                }
            })
        },
        remove_pairs:function(){
            this.data = []
        },     
        remove_selected:function(){             
            var ref_list_to_del = []
            this.selected.forEach(element => {
                //
                ref_list_to_del.push(element.ref)

                //
                if (element.pair_id != "#"){
                    this.deleted_records.push(element)
                }
            })            
            //eliminamos la lista de errores
            this.data = this.data.filter(element => {                
                return ref_list_to_del.indexOf(element.ref) == -1
            })
        }
    },
    created:function(){
        var table_data = this.in_data.data
        var deleted_records = this.in_data.deleted_records

        if (table_data != undefined){
            this.data = table_data
        }

        if (deleted_records != undefined){
            this.deleted_records = deleted_records
        }
    },
    beforeDestroy:function(){
        this.$emit('panel-close',this.$data)
    }
}
</script>