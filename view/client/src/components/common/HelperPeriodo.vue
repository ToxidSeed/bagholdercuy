<template>
    <div class="row q-col-gutter-xs">
        <q-select class="col-5" v-model="periodo" :options="opciones" label="Período" outlined dense clearable />
        <div class="col">
            <div class="row q-col-gutter-xs" v-if="periodo">
                <q-input class="col-6" v-model="fchDesde" label="Fch. Desde" outlined dense :rules="[
                    validarFechaFormato,
                    validarRangoDesde
                ]" placeholder="dd/mm/yyyy" mask="##/##/####" :disable="periodo !== 'Personalizado'" />
                <q-input class="col-6" v-model="fchHasta" label="Fch. Hasta" outlined dense :rules="[
                    validarFechaFormato,
                    validarRangoHasta
                ]" placeholder="dd/mm/yyyy" mask="##/##/####" :disable="periodo !== 'Personalizado'" />
            </div>
        </div>
    </div>
</template>
<script>
import date from "date-and-time"
export default {
    name: "HelperPeriodo",
    data() {
        return {
            visible: false,
            periodo: null,
            fchDesde: null,
            fchHasta: null,
            opciones: [
                'Ultimos 7 Dias',
                'Ultimos 30 Dias',
                'Ultimos 100 Dias',
                'Año en Curso',
                'Ultimos 365 Dias',
                'Personalizado'
            ]
        };
    },
    watch: {
        periodo(newVal) {
            if (!newVal || newVal === 'Personalizado') return;
            const hoy = new Date();
            let desde = new Date();

            if (newVal === 'Ultimos 7 Dias') desde.setDate(hoy.getDate() - 7);
            else if (newVal === 'Ultimos 30 Dias') desde.setDate(hoy.getDate() - 30);
            else if (newVal === 'Ultimos 100 Dias') desde.setDate(hoy.getDate() - 100);
            else if (newVal === 'Ultimos 365 Dias') desde.setDate(hoy.getDate() - 365);
            else if (newVal === 'Año en Curso') desde = new Date(hoy.getFullYear(), 0, 1);

            this.fchHasta = date.format(hoy, 'DD/MM/YYYY');
            this.fchDesde = date.format(desde, 'DD/MM/YYYY');
        }
    },
    methods: {
        validarFechaFormato(val) {
            if (!val) return true;
            return date.isValid(val, 'DD/MM/YYYY') || 'El formato debe ser dd/mm/yyyy';
        },
        validarRangoDesde(val) {
            if (!val || !this.fchHasta) return true;
            if (!date.isValid(val, 'DD/MM/YYYY') || !date.isValid(this.fchHasta, 'DD/MM/YYYY')) return true;
            const d1 = date.parse(val, 'DD/MM/YYYY');
            const d2 = date.parse(this.fchHasta, 'DD/MM/YYYY');
            return d1 <= d2 || 'Fch. Desde no puede ser mayor a Fch. Hasta';
        },
        validarRangoHasta(val) {
            if (!val || !this.fchDesde) return true;
            if (!date.isValid(val, 'DD/MM/YYYY') || !date.isValid(this.fchDesde, 'DD/MM/YYYY')) return true;
            const d1 = date.parse(this.fchDesde, 'DD/MM/YYYY');
            const d2 = date.parse(val, 'DD/MM/YYYY');
            return d1 <= d2 || 'Fch. Desde no puede ser mayor a Fch. Hasta';
        }
    }
};
</script>