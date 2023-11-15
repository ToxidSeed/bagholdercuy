<template>
<q-layout view="hHh lpR fFf">

    <q-header elevated class="bg-white text-blue-10">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="left = !left" />

        <q-toolbar-title>
          <q-avatar>
            <img src="/532625_cash_coins_hand_income_investment_icon.png">
          </q-avatar>
          BagHolder
        </q-toolbar-title>
        <span class="q-mr-xs text-h6">{{cod_cuenta}}</span>        
        <q-btn  color = "red" dense round icon="power_settings_new" @click="cerrar_cesion"/>
      </q-toolbar>
    </q-header>

    <q-drawer show-if-above v-model="left"  bordered>
      <MenuPrincipal/>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
    <MessageBox/>
  </q-layout>  
   <!-- <PanelSimulationDataEntry/>-->   
</template>

<script>
import MessageBox from '@/components/dialogs/MessageBox.vue'
import MenuPrincipal from './components/MenuPrincipal.vue'
//import PanelSimulationDataEntry from './components/PanelSimulationDataEntry.vue'

export default {
  name: 'Main',

  components: {
    MenuPrincipal,
    MessageBox
    //GrowthPotential
    //PanelSimulationDataEntry
  },
  data () {
    return {
      left: false,
      right: false,
      cod_cuenta:""
    }
  },
  methods:{
    cerrar_cesion:function(){
      localStorage.removeItem("logeado")
      localStorage.removeItem("token")
      this.$router.push("/login")
    }
  },
  mounted:function(){
    this.cod_cuenta = localStorage.getItem("cod_cuenta")
    let nom_cuenta = localStorage.getItem("nom_cuenta")    
    console.log(nom_cuenta)
  }
}
</script>

<style>
</style>
