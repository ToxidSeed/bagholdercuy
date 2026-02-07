<template>
    <q-page>
        <q-toolbar>         
            <q-btn icon="menu" flat color="blue-10">
                <q-menu>
                <q-list style="min-width: 100px" dense>
                    <q-item clickable v-close-popup to="/ciclos">
                        <q-item-section>Duración de Ciclos</q-item-section>
                    </q-item>
                    <q-item clickable v-close-popup to="/ciclos/variacion">
                        <q-item-section>Variación en Ciclos</q-item-section>
                    </q-item>                
                </q-list>
                </q-menu>
            </q-btn>   
            <q-toolbar-title shrink class="text-blue-10">Ciclos</q-toolbar-title>            
        </q-toolbar>        
        <router-view></router-view>         
    </q-page>
</template>
<script>
import ciclos_store from "./ciclos-store"

export default {
    name:"PageCiclos",
    components:{

    },
    data(){
        return {
            localstore: ciclos_store
        }
    },
    watch:{
        
    },
    mounted:function(){        

    },
    methods:{
        btn_buscar_click:function(){

        }            
    }
}
</script>