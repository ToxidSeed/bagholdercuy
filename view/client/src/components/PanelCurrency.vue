<template>
    <div>
        <q-card>
            <q-card-section>
                <div class="text-h6">Currency</div>
            </q-card-section>
            <q-card-section>
                <div class="row">
                    <q-input v-model="currency_id" readonly label="ID" class="col-4" label-color="indigo"/>
                    <q-input v-model="symbol" label="Symbol" class="col-8"/>
                </div>
                <q-input v-model="currency_name" label="Nombre"/>                
            </q-card-section>
            <q-card-actions align="right">
                <q-btn color="primary">Guardar</q-btn>
                <q-btn color="orange">Cancelar</q-btn>
                <!--<q-btn flat>Action 2</q-btn>-->
            </q-card-actions>
        </q-card>
    </div>
</template>
<script>

export default {
    name:"PanelCurrency",
    props:{
        in_data:{
            type:Object,
            default: () => {}
        }
    },
    data: () => {
        return {
            currency_id:"Nuevo",
            symbol: "",
            currency_name:"",
            fec_registro:""
        }
    },
    beforeDestroy:function(){
        this.$emit('panel-removed',this.$data)
    },
    created:function(){
        if (Object.keys(this.in_data).length != 0){            
            this.currency_id = this.in_data.currency_id
            this.symbol = this.in_data.symbol
            this.currency_name = this.in_data.currency_name
        }
    }
}
</script>