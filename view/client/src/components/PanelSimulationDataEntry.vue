<template>
    <div class="row q-ma-md">
        <div class="col-3">
            <div class="row">
                <div class="col-3">
                    <q-input v-model="quantity" label="quantity"/>
                </div>
                <div class="col-5">
                    <q-select v-model="frequency" :options="options" label="Standard" class="q-ml-xs"/>
                </div>
                <div class="col-4">
                    <div class="row">
                        <div>
                            <q-btn color="primary" label="Add" class="q-ml-xs" @click="add"/>                    
                        </div>
                        <div>
                            <q-btn color="secondary" label="Run" class="q-ml-xs" @click="run"/>                    
                        </div>
                    </div>
                </div>                                
            </div>
            <q-table
            dense
            class="q-mt-md"
            title="Frequency"
            :data="data"
            :columns="columns"
            row-key="name"
            />
        </div>
        <div class="col-9">
        <GrowthPotential 
        v-bind:sim_params="sim_params" 
        v-bind:upd_time="upd_time"
        />
        </div>
    </div>
</template>
<script>

import GrowthPotential from './GrowthPotential.vue'

export default {
    name:"PanelSimulationDataEntry",
    components:{
        GrowthPotential
    },
    data:() =>{
        return{
            quantity:0,
            frequency:'days',
            options:[
                'days','weeks','months','years','all time'
            ],
            data:[],            
            columns:[
                {
                    name:'quantity',
                    label:'quantity',
                    field:'quantity',
                    align:'left',
                    style: 'width: 75px',
                },{
                    name:'frequency',
                    label:'frequency',
                    field:'frequency',
                    align:'left'
                }
            ],
            sim_params:[],
            upd_time:null
        }
    },
    methods:{
        add:function(){
            this.data.push({
                quantity:this.quantity,
                frequency:this.frequency
            })
        },
        run:function(){
            this.sim_params = this.data
            this.upd_time = Date.now();
            console.log(this.upd_time)
        }
    }
}
</script>