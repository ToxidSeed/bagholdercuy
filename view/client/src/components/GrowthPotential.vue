<template>
    <div class="row">
        <q-card class="my-card col-3" v-for="item in sim_data" v-bind:key="item.iter">
        <q-item>            
            <q-item-section>
            <q-item-label>{{item.deep_text}}</q-item-label>
            <!--<q-item-label caption>Subhead</q-item-label>-->
            </q-item-section>
        </q-item>

        <!--<img src="https://cdn.quasar.dev/img/parallax2.jpg">-->
        <div class="row q-ma-md">
            <div class="col-7">
                <q-input  v-model="item.max_price" label="Precio máximo" />
                <q-input  v-model="item.max_price_date" label="Fecha de precio máximo" />
                <q-input  v-model="item.current_price" label="Precio actual" />
                <q-input  v-model="item.pct_change_text" label="% cambio" />
                <q-input  v-model="item.time_to_recover_text" label="Time to recover" />
            </div>
            <div class="col-5">
                <div class="fit row items-center justify-center">
                    <div>{{item.growth_potential_text}}</div>
                </div>
            </div>                
        </div>
        </q-card>       
    </div>
</template>
<script>
export default {
    name:"GrowthPotential",
    props:{
        sim_params:{
            default:[]
        },
        upd_time:null
    },
    data:() =>{
        return {
            sim_data:[]            
        }
    },
    watch:{
        upd_time:function(old_time, new_time){
            console.log(old_time)
            console.log(new_time)

            this.run()            
        }
    },
    methods:{
        run:function(){
            this.$http.post(
            this.$backend_url+'SimulationManager/SimulationManager/run',{
                sim_params:this.sim_params
            }).then(httpresponse => {
                var response = httpresponse.data
                this.sim_data = response.data
            })
        }
    }
}
</script>