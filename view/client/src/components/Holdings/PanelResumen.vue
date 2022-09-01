<template>
    <q-card style="height:100vh">
        <q-card-section class="q-pb-none">
            <div class="text-primary text-h6">Resumen</div>
        </q-card-section>
        <q-card-section class="q-gutter-none q-pt-none">
            <div class="row">
                <q-input class="col-4" borderless readonly label-color="blue-10 " v-model="text" label="Cash USD" />
                <q-input class="col-4" borderless readonly label-color="blue-10 " v-model="text" label="Cash PEN" />
                <q-input class="col-4" borderless readonly label-color="blue-10 " v-model="text" label="Cash EUR" />
            </div>
            <div class="row">
                <q-input class="col-4" borderless readonly label-color="blue-10 " v-model="text" label="Inversion USD" />
                <q-input class="col-4" borderless readonly label-color="blue-10 " v-model="text" label="Inversion PEN" />
                <q-input class="col-4" borderless readonly label-color="blue-10 " v-model="text" label="Inversion EUR" />
            </div>
            <div class="row">
                <q-input class="col-4" borderless readonly label-color="blue-10 " v-model="text" label="Net worth USD" />
                <q-input class="col-4" borderless readonly label-color="blue-10 " v-model="text" label="Net worth PEN" />
                <q-input class="col-4" borderless readonly label-color="blue-10 " v-model="text" label="Net worth EUR" />
            </div>
        </q-card-section>
    </q-card>
</template>
<script>
export default {
    name:"PanelResumen",
    data: () => {
        return {
            text:"192.63" 
        }
    }
}
</script>