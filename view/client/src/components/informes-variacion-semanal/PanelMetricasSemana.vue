<template>
    <div class="row">        
        <q-card class="col-3">
            <q-card-section class="q-pa-none"> 
                <div class="text-center q-pt-xs text-subtitle1">
                    <div>Lunes</div>                              
                    <div>18/12/2023</div>                              
                </div>
                <q-separator/>
                <div class="row">                    
                    <div class="col-6">
                        <div class="q-pl-xs">Apertura</div>
                        <div class="text-center text-subtitle1">60</div>
                    </div>   
                    <q-separator vertical/>        
                    <div class="col">
                        <div class="q-pl-xs">Cierre</div>
                        <div class="text-center text-subtitle1">70</div>
                    </div>                                                                                                
                </div>    
                <q-separator/>            
                <div class="row">
                    <div class="col-6">
                        <div class="q-pl-xs">Maximo</div>
                        <div class=" text-center text-subtitle1">90</div>
                    </div>       
                    <q-separator vertical/>                        
                    <div class="col">
                        <div class="q-pl-xs">Minimo</div>                        
                        <div class="col-6 text-center text-subtitle1">110</div>
                    </div>                    
                </div>
            </q-card-section>
            <q-separator/>
            <q-card-section>
                <div class="row text-center">
                    <div class="col-6 text-teal text-h6">+50</div>                
                    <div class="col text-teal text-h6">+10%</div>
                </div>
            </q-card-section>
        </q-card>
    </div>
</template>
<script>
export default {

}
</script>
<style scoped>
.q-toolbar {
    min-height: auto;
}
</style>