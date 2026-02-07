<template>
<div>
    <q-card>
        <q-card-section class="text-subtitle1 text-blue-10 q-pb-xs q-pt-xs">
            Symbols
        </q-card-section>
        <q-separator/>
        <q-card-section class="q-pa-none">
        <q-list separator>
            <q-item clickable v-ripple v-for="item in data" :key="item">
                <q-item-section>
                <q-item-label class="text-blue-10 text-bold">{{ item.cod_symbol }}</q-item-label>
                <q-item-label caption>{{ item.nom_symbol }}</q-item-label>
                </q-item-section>
            </q-item>
        </q-list>
        </q-card-section>
    </q-card>    
</div>
</template>
<script>
export default {
    name:"ListaSymbolsAlertas",
    data() {
        return {
            data:[
                {cod_symbol:"SOXL",nom_symbol:"DIREXTION DAILY"},
                {cod_symbol:"LRCX",nom_symbol:"LAM RESEARCH"}
            ]
        }
    }
}
</script>