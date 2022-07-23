<template>
    <div class="row">
        <div class="col-3">
            <q-tabs
            v-model="tab"
            >
            </q-tabs>
            <q-tab-panels
            v-model="tab"
            >
                <q-tab-panel name="opciones">
                    <PanelMantOpciones/>
                </q-tab-panel>
                <q-tab-panel name="loader">
                    <TableOpciones/>
                </q-tab-panel>
            </q-tab-panels>
        </div>        
    </div>
</template>
<script>
import PanelMantOpciones from "@/components/MantOpciones/PanelMantOpciones.vue"
import TableOpciones from "@/components/MantOpciones/TableOpciones.vue"
export default {
    name:"MainMantOpciones",
    components:{
        PanelMantOpciones,
        TableOpciones
    },
    data: () => {
        return {
            tab:"opciones"
        }
    }
}
</script>