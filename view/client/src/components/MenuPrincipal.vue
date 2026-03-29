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
            <!--<q-item 
            active-class="my-menu-link"
            to="/">
                <q-item-section>Simulation</q-item-section>
            </q-item>-->
            <q-expansion-item
                expand-separator            
                label="Holdings"                
                default-opened
                header-class="text-bold"        
                dense
            >
                <q-list dense>
                    <q-item 
                    active-class="my-menu-link"
                    to="/holdings">
                        <q-item-section avatar>
                            <q-icon color="primary" name="keyboard_arrow_right" />
                        </q-item-section>
                        <q-item-section>Posiciones</q-item-section>
                    </q-item>
                    <!--
                    <q-item 
                    active-class="my-menu-link"
                    to="/operacion">
                        <q-item-section>Operaciones</q-item-section>
                    </q-item>
                    -->
                    <!--<q-item 
                    active-class="my-menu-link"
                    to="/orden">
                        <q-item-section>Ordenes</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    to="/orden">
                        <q-item-section>Transferencias</q-item-section>
                    </q-item>-->
                    <q-item 
                    active-class="my-menu-link"
                    to="/reorganizarorden">
                    <q-item-section avatar>
                        <q-icon color="primary" name="keyboard_arrow_right" />
                    </q-item-section>
                        <q-item-section>Reorganizar</q-item-section>
                    </q-item>
                </q-list>
            </q-expansion-item>
            <q-expansion-item
                expand-separator  
                default-opened                          
                label="Carga de Operaciones"      
                header-class="text-bold"        
                dense
            >
            <q-list dense>
                <q-item 
                active-class="my-menu-link"
                to="/carga-operaciones/ibkr">
                    <q-item-section avatar>
                        <q-icon color="primary" name="keyboard_arrow_right" />
                    </q-item-section>
                    <q-item-section>Interactive Brokers</q-item-section>
                </q-item>
                <q-item 
                active-class="my-menu-link"
                to="/hapi-trades">
                <q-item-section avatar>
                        <q-icon color="primary" name="keyboard_arrow_right" />
                    </q-item-section>
                    <q-item-section>HAPI</q-item-section>
                </q-item>
                <q-item 
                active-class="my-menu-link"
                to="/sura-trades">
                <q-item-section avatar>
                        <q-icon color="primary" name="keyboard_arrow_right" />
                    </q-item-section>
                    <q-item-section>SURA</q-item-section>
                </q-item>
            </q-list>
            </q-expansion-item>
            <q-item 
            active-class="my-menu-link"
            to="/watchlist">
                <q-item-section>Watchlist</q-item-section>
            </q-item>
            <q-expansion-item
                expand-separator
                label="Simulacion"
                dense
                default-opened
            >
                <q-item
                active-class="my-menu-link"
                to="/simulacion-rentabilidad"
                dense
                >
                    <q-item-section avatar>
                        <q-icon color="primary" name="keyboard_arrow_right" />
                    </q-item-section>
                    <q-item-section>Rentabilidad</q-item-section>
                </q-item>
            </q-expansion-item>            
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
                    <q-item-section avatar>
                        <q-icon color="primary" name="keyboard_arrow_right" />
                    </q-item-section>
                        <q-item-section>Analitica Mensual</q-item-section>
                    </q-item>   
                    <q-item 
                    active-class="my-menu-link"
                    to="/variacionsemanal">
                    <q-item-section avatar>
                        <q-icon color="primary" name="keyboard_arrow_right" />
                    </q-item-section>
                        <q-item-section>Analitica Semanal</q-item-section>
                    </q-item>                    
                    <q-item 
                    active-class="my-menu-link"
                    to="/variaciondiaria">
                    <q-item-section avatar>
                        <q-icon color="primary" name="keyboard_arrow_right" />
                    </q-item-section>
                        <q-item-section>Analitica Diaria</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    to="/rentabilidadoperaciones">
                    <q-item-section avatar>
                        <q-icon color="primary" name="keyboard_arrow_right" />
                    </q-item-section>
                        <q-item-section>Rentabilidad Operaciones</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    to="/stats">
                    <q-item-section avatar>
                        <q-icon color="primary" name="keyboard_arrow_right" />
                    </q-item-section>
                        <q-item-section>Stats</q-item-section>
                    </q-item>
                    <q-item
                    active-class="my-menu-link"
                    to="/metricas"            
                    dense
                    >
                        <q-item-section avatar>
                            <q-icon color="primary" name="keyboard_arrow_right" />
                        </q-item-section>
                        <q-item-section>Metricas</q-item-section>
                    </q-item>
                    <q-item
                    active-class="my-menu-link"
                    to="/ciclos"            
                    dense
                    >
                        <q-item-section avatar>
                            <q-icon color="primary" name="keyboard_arrow_right" />
                        </q-item-section>
                        <q-item-section>Ciclos</q-item-section>
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
                        <q-item-section avatar>
                            <q-icon color="primary" name="keyboard_arrow_right" />
                        </q-item-section>
                        <q-item-section>Data Loader</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    to="/series">
                    <q-item-section avatar>
                        <q-icon color="primary" name="keyboard_arrow_right" />
                    </q-item-section>
                        <q-item-section>Series</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    to="/currency">
                        <q-item-section avatar>
                            <q-icon color="primary" name="keyboard_arrow_right" />
                        </q-item-section>
                        <q-item-section>Currency</q-item-section>
                    </q-item>                    
                    <q-item 
                    active-class="my-menu-link"
                    to="/symbols">
                        <q-item-section avatar>
                            <q-icon color="primary" name="keyboard_arrow_right" />
                        </q-item-section>
                        <q-item-section>Symbols</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    :to="{name:'opciones'}">
                        <q-item-section avatar>
                            <q-icon color="primary" name="keyboard_arrow_right" />
                        </q-item-section>
                        <q-item-section>Opciones</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    :to="{name:'calendario-semanal-loader'}">
                        <q-item-section avatar>
                            <q-icon color="primary" name="keyboard_arrow_right" />
                        </q-item-section>
                        <q-item-section>Calendario Semanal</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    :to="{name:'calendario-diario-loader'}">
                    <q-item-section avatar>
                            <q-icon color="primary" name="keyboard_arrow_right" />
                        </q-item-section>
                        <q-item-section>Calendario Diario</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    :to="{name:'broker'}">
                    <q-item-section avatar>
                            <q-icon color="primary" name="keyboard_arrow_right" />
                        </q-item-section>
                        <q-item-section>Broker</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    :to="{name:'cuenta'}">
                    <q-item-section avatar>
                            <q-icon color="primary" name="keyboard_arrow_right" />
                        </q-item-section>
                        <q-item-section>Cuenta</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    :to="{name:'usuario'}">
                    <q-item-section avatar>
                            <q-icon color="primary" name="keyboard_arrow_right" />
                        </q-item-section>
                        <q-item-section>Usuario</q-item-section>
                    </q-item>
                    <q-item 
                    active-class="my-menu-link"
                    :to="{name:'stocksplit'}">
                    <q-item-section avatar>
                            <q-icon color="primary" name="keyboard_arrow_right" />
                        </q-item-section>
                        <q-item-section>Stock Split</q-item-section>
                    </q-item>
                </q-list>
            </q-expansion-item>
        </q-list>
    </div>
</template>
<script>
export default {
    name:"MenuPrincipal",
    data:()=>{
        return {

        }
    }
}
</script>
<style lang="sass">
.my-menu-link
  
</style>