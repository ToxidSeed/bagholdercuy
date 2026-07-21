<template>
    <q-dialog :value="value" @input="$emit('input', $event)">
        <PanelOptionsChain style="min-width:750px" v-bind:symbol="symbol" v-on:option-select="option_selected"
            v-on:close="$emit('input', false)" v-on:sel-contract="option_selected" />
    </q-dialog>
</template>
<script>
import PanelOptionsChain from '@/components/common/PanelOptionsChain.vue';
export default {
    name: "winBuscadorOpciones",
    components: {
        PanelOptionsChain
    },
    props: {
        value: {
            type: Boolean,
            default: false
        },
        symbol: {
            type: Object,
            default: () => ({})
        }
    },
    data() {
        return {
            open: false
        }
    },
    methods: {
        option_selected(contract) {
            this.$emit('option-select', contract);
            this.$emit('sel-contract', contract);
            this.$emit('input', false);
        }
    }
}
</script>