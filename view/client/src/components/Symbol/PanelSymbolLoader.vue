<template>
    <div>
        <q-card>
            <q-toolbar class="text-primary">      
                <q-toolbar-title>
                    Symbols Loader
                </q-toolbar-title>      
            </q-toolbar>
            <q-card-section>
                <div>
                    <q-checkbox v-model="selection" val="symbols" label="Symbols" color="teal" />
                    <q-checkbox v-model="selection" val="etf_symbols" label="ETFs" color="teal" />                    
                </div>
            </q-card-section>  
            <q-card-actions>
                <q-btn label="aceptar" color="primary" @click="save"/>
                <q-btn label="cancelar"/>
            </q-card-actions>
        </q-card>
    </div>
</template>
<script>
export default {
    name:"PanelSymbolLoader",
    data: () => {
        return {
            selection:[]
        }
    },
    methods:{
        load:function(){
            this.$https.post('',{

            })
        }
    }
}
</script>