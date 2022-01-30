<template>
    <div>
        <q-card flat>
            <q-card-section>                
                <!--<q-toolbar class="text-primary">
                    <q-btn flat round dense icon="fas fa-sync" />
                    <q-toolbar-title>                        
                    </q-toolbar-title>                    
                </q-toolbar>-->
            </q-card-section>
            <q-card-section>
                <div class="q-pa-mid row">
                    <q-table
                        class="col-6"
                        :data="data" 
                        :columns="columns"                      
                        row-key="name"  
                    />
                </div>
            </q-card-section>
        </q-card>
    </div>
</template>
<script>
export default {
    name:"PanelOverview",
    components:{

    },
    data: () => {   
        return {
            data:[
                {descripcion:"Actual",gp:"20%", gp_pen:"100", gp_eur:"100", gp_usd:"100"},
                {descripcion:"Mes en Curso", gp:"10%", gp_pen:"100", gp_eur:"100", gp_usd:"100"},
                {descripcion:"3 meses", gp:"-10%", gp_pen:"100", gp_eur:"100", gp_usd:"100"},
                {descripcion:"52 semanas", gp:"15%", gp_pen:"100", gp_eur:"100", gp_usd:"100"}                
            ],
            columns:[
                {name:'descripcion',field:'descripcion',label:'Descripción',align:'left'},
                {name:'gp',field:'gp',label:'G/P%',align:'right'},
                {name:'gp_pen',field:'gp_pen',label:'G/P PEN',align:'right'},
                {name:'gp_eur',field:'gp_eur',label:'G/P EUR',align:'right'},
                {name:'gp_usd',field:'gp_usd',label:'G/P USD',align:'right'}
            ]
        }
    }
}
</script>