<template>    
    <q-card class="no-border-radius" flat bordered>
        <q-item>                
            <q-item-section>
                <q-item-label class="text-grey-8 text-subtitle2">Estadisticas de carga </q-item-label>                    
            </q-item-section>
        </q-item>           
        <q-card-section>
            <q-separator/>        
            <div class="q-pt-md" v-for="(item, index) in testdata" :key="index">
                <div class="row">
                    <div class="col-6">
                        <q-card-section horizontal>
                            <div class="col-2">{{item.key_serie.label}}</div>
                            <div class="col-9 q-pl-md">
                                <div>
                                    <span class="text-bold">Min: </span><span>{{ item.key_serie.min }}</span><span class="text-bold"> - Max: </span><span>{{ item.key_serie.max }}</span>                     
                                </div>
                                <div>
                                    <span  class="text-weight-bold text-blue-10">{{item.key_serie.registros}} registros</span>
                                </div>
                            </div>
                            <div>
                                <q-btn size="12px" flat dense round icon="more_vert" />
                            </div>
                        </q-card-section>
                    </div>
                    <q-separator vertical/>
                    <div class="col">
                        <q-card-section horizontal class="q-pl-md">
                            <div class="col-2">{{ item.key_variacion.label }}</div>
                            <div class="col-9 q-pl-md">
                                <div>
                                    <span class="text-bold">Min: </span><span>{{ item.key_variacion.min }}</span><span class="text-bold"> - Max: </span><span>{{ item.key_variacion.max }}</span>                    
                                </div>
                                <div>
                                    <span  class="text-weight-bold text-blue-10">{{item.key_variacion.registros}} registros</span>
                                </div>
                            </div>
                            <div>
                                <q-btn size="12px" flat dense round icon="more_vert" />
                            </div>
                        </q-card-section>
                    </div>      
                </div>  
                <q-separator/>        
            </div>

        </q-card-section>                         
    </q-card>    
</template>
<script>
export default{
    name: "PanelEstadisticasCarga",
    data() {
        return {
            testdata:[
                {
                    "key_serie":{
                        "label":"Series Diarias",
                        "min":"01/01/2024",
                        "max":"11/05/2024",
                        "registros": "35555"
                    },
                    "key_variacion":{
                        "label":"Variaciones Diarias",
                        "min":"01/01/2024",
                        "max":"11/05/2024",
                        "registros": "35555"
                    }
                },
                {
                    "key_serie":{
                        "label":"Series Semanales",
                        "min":"2024/20",
                        "max":"2024/35",
                        "registros": "4222"
                    },
                    "key_variacion":{
                        "label":"Variaciones Semanales",
                        "min":"2024/20",
                        "max":"2024/35",
                        "registros": "4222"
                    }
                },
                {
                    "key_serie":{
                        "label":"Series Mensuales",
                        "min":"feb 2024",
                        "max":"mar 2024",
                        "registros": "50"
                    },
                    "key_variacion":{
                        "label":"Variaciones Mensuales",
                        "min":"feb 2024",
                        "max":"mar 2024",
                        "registros": "50"
                    }
                }
            ],
            data:[]
        }
    },
    methods: {
        
    }
}
</script>