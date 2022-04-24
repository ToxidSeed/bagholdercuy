<template>
    <div>
        <q-card>
            <q-card-section class="q-pb-none">
                <div class="text-h7 text-indigo">Datos de Carga</div>
            </q-card-section>
            <q-card-section class="row">
                <div class="col-6">
                    <q-input label="Desde" mask="##/##/####" fill-mask="__/__/____"/>
                </div>
            </q-card-section>
            <q-separator/>
            <q-card-actions align="right">
                <q-btn label="acepar" color="primary"/>
                <q-btn label="cancelar" />
            </q-card-actions>
        </q-card>
    </div>
</template>
<script>
export default {
    name:"PanelCurrencyExchangeRateHistLoader",
    data: () => {
        return {
            date_since:""
        }
    }
}
</script>