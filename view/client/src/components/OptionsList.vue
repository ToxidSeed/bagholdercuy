<template>
    <div>
        <q-list dense>
            <q-item 
            active-class="my-menu-link"
            to="/funds">
                <q-item-section>Funds</q-item-section>
            </q-item>   
            <q-item 
            active-class="my-menu-link"
            :to="{name:'currencyexchange',params:{inFirstPanelSize:0}}">
                <q-item-section>Currency exchange rates</q-item-section>
            </q-item>            
            <q-item 
            active-class="my-menu-link"
            to="/">
                <q-item-section>Simulation</q-item-section>
            </q-item>
            <q-expansion-item
                expand-separator            
                label="Holdings"                
                dense
            >
                <q-list dense>
                    <q-item 
                    active-class="my-menu-link"
                    to="/holdings">
                        <q-item-section>Posiciones</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    to="/historial_operaciones">
                        <q-item-section>Historial Operaciones</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    to="/historial_ordenes">
                        <q-item-section>Historial Ordenes</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    to="/reorganizarorden">
                        <q-item-section>Reorganizar</q-item-section>
                    </q-item>
                </q-list>
            </q-expansion-item>
            <q-item 
            active-class="my-menu-link"
            to="/stats">
                <q-item-section>Stats</q-item-section>
            </q-item>
            <q-expansion-item
                expand-separator  
                default-opened          
                label="Informes"                
                dense
            >
                <q-list dense>
                    <q-item 
                    active-class="my-menu-link"
                    to="/variacionmensual">
                        <q-item-section>Variación Mensual</q-item-section>
                    </q-item>   
                    <q-item 
                    active-class="my-menu-link"
                    to="/variacionsemanal">
                        <q-item-section>Variación Semanal</q-item-section>
                    </q-item>                    
                </q-list>
            </q-expansion-item>
            <q-expansion-item
                expand-separator  
                default-opened          
                label="Configuración"                
                dense
            >
                <q-list dense>
                    <q-item 
                    active-class="my-menu-link"
                    to="/dataloader">
                        <q-item-section>Data Loader</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    to="/series">
                        <q-item-section>Series</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    to="/currency">
                        <q-item-section>Currency</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    to="/symbols">
                        <q-item-section>Symbols</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    :to="{name:'opciones'}">
                        <q-item-section>Opciones</q-item-section>
                    </q-item>
                </q-list>
            </q-expansion-item>
        </q-list>
    </div>
</template>
<script>
export default {
    name:"OptionsList",
    data:()=>{
        return {

        }
    }
}
</script>
<style lang="sass">
.my-menu-link
  
</style>