<template>
    <q-dialog v-model="opened" persistent transition-show="flip-down" transition-hide="flip-up">
      <q-card> 
            <q-card-section class="q-pt-xs q-pb-xs" >
                <q-icon name="fa fa-info-circle" size="md" color="red" text-color="white" /> {{title}}            
            </q-card-section>
            <q-separator/>
            <q-card-section class="q-pt-md q-pb-xs">
            {{message}}
            </q-card-section>            
            <q-card-section class="q-pt-none q-mt-none" >
                <div>
                    <ul class="q-mt-none">
                        <li v-for="item in errors" v-bind:key="item">
                            {{item}}
                        </li>
                    </ul>
                </div>
            </q-card-section>            
        <q-separator />
        <q-card-actions align="right">
            <q-btn dense color="primary" v-close-popup>OK</q-btn>
            <q-btn flat v-close-popup>Cerrar</q-btn>
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
                errors:[],
                opened: false
            }
        },
        methods:{
            new:function(appresp=null, args=null){
                this.errors = []
                this.opened = true;
                if (appresp != null){
                    this.process_appresp(appresp)
                }else{
                    if (args.title != undefined){
                        this.title = args.title
                    }
                    if (args.action != undefined){
                        this.action = args.action
                    }
                    if (args.message != undefined){
                        this.message = args.message
                    }
                }                
            },
            process_appresp:function(appresp){
                var has_errors = false    
                console.log(has_errors)                                
                if (appresp != null){
                    if (appresp.errors.length > 0){
                        has_errors = true
                        this.errors = appresp.errors
                    }
                    this.message = appresp.message
                    this.title = "Error"
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
