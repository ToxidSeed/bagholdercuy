<template>
<q-layout view="hHh lpR fFf">

    <q-header elevated class="bg-white text-primary">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="left = !left" />

        <q-toolbar-title>
          <q-avatar>
            <img src="/532625_cash_coins_hand_income_investment_icon.png">
          </q-avatar>
          BagHolder
        </q-toolbar-title>
        <q-btn label="Cerrar Cesión" flat @click="cerrar_cesion"/>
      </q-toolbar>
    </q-header>

    <q-drawer show-if-above v-model="left"  bordered>
      <OptionsList/>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>  
   <!-- <PanelSimulationDataEntry/>-->   
</template>

<script>
import OptionsList from './components/OptionsList.vue'
//import PanelSimulationDataEntry from './components/PanelSimulationDataEntry.vue'

export default {
  name: 'Main',

  components: {
    OptionsList
    //GrowthPotential
    //PanelSimulationDataEntry
  },
  data () {
    return {
      left: false,
      right: false
    }
  },
  methods:{
    cerrar_cesion:function(){
      localStorage.removeItem("logeado")
      localStorage.removeItem("token")
      this.$router.push("/login")
    }
  }
}
</script>

<style>
</style>
