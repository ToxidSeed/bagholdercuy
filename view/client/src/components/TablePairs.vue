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
        in_currency_base_symbol:{
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
                    field:"pair_id",
                    name:"pair_id"
                },
                {
                    label:"Par",
                    align:"left",
                    field:"pair_name",
                    name:"pair_name"
                }],
            data:[],
            deleted_records:[]
        }
    },
    methods:{
        add_pair:function(data){            
            var in_ref_symbol = data["ref"]
            var in_base_symbol = data["base"]
            var dupplicate_ref = false
            var response = ""

            const found = this.data.find(element => element.ref == in_ref_symbol)
            if (found != undefined){
                dupplicate_ref = true
            }
                        
            if (dupplicate_ref == true){
                response = "La moneda referencia "+in_ref_symbol+" ya esta agregada a la lista"
                this.$emit('add-pair-error', response)
                return;
            }
            if (in_base_symbol == ""){
                response = "La moneda base está vacía"
                this.$emit('add-pair-error', response)
                return;
            }

            //if no errors add pair
            var pair_name = data["base"]+"/"+data["ref"]
            this.data.push({
                "pair_id":"#",
                "pair_name":pair_name,
                "base":in_base_symbol,
                "ref":in_ref_symbol
            })
        },        
        get_pairs_data:function(){
            return this.$data
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