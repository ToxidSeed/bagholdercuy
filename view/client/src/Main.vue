<template>
<q-layout view="hHh lpR fFf">

    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="left = !left" />

        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
          </q-avatar>
          BagHolder
        </q-toolbar-title>
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
  }
}
</script>

<style>
</style>
