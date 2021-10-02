<template>
    <q-dialog v-model="opened" persistent transition-show="flip-down" transition-hide="flip-up">
      <q-card class="bg-primary text-white">
        <q-bar>
          <!--<q-icon name="network_wifi" />
          <q-icon name="network_cell" />
          <q-icon name="battery_full" />
          <div>9:34</div>-->

          <q-space />

          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip class="bg-white text-primary">Close</q-tooltip>
          </q-btn>
        </q-bar>

        <q-card-section>
          <div class="text-h6">Alert</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          {{message}}
        </q-card-section>
        <q-separator />
        <q-card-actions>
            <q-btn flat dense v-close-popup>Aceptar</q-btn>
            <q-btn flat dense v-close-popup>Cancelar</q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
</template>
<script>
    export default {
        name:"MessageBox",
        data () {
            return {
                title:"",
                message:"",
                action:"",
                opened: false
            }
        },
        methods:{
            new:function(args){
                this.opened = true;
                if (args.title != undefined){
                    this.title = args.title
                }
                if (args.action != undefined){
                    this.action = args.action
                }
                if (args.message != undefined){
                    this.message = args.message
                }
            },
            onOk(){
                if (this.action != ""){
                    this.$emit(this.action)
                }                
            }
        }
    }
</script>
