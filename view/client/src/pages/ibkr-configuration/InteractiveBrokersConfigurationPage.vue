<template>
    <div>
        <q-toolbar>
            <q-btn class="q-ml-xs" color="blue-10" dense icon="menu" flat>
                <q-menu>
                    <q-list dense>
                        <q-item clickable v-close-popup :to="{ name: 'iexcloud-loader' }">
                            <q-item-section>
                                <q-item-label>Carga de series desde <span
                                        class="text-blue-10 text-bold">iexcloud</span></q-item-label>
                            </q-item-section>
                        </q-item>
                    </q-list>
                </q-menu>
            </q-btn>
            <q-toolbar-title class="text-blue-10">Interactive Brokers Configuración</q-toolbar-title>
        </q-toolbar>
        <router-view />
    </div>
</template>
<script>
export default {
    name: "InteractiveBrokersConfigurationPage",
    data() {
        return {
        };
    },
    methods: {
    },
    mounted() {
    }
};
</script>