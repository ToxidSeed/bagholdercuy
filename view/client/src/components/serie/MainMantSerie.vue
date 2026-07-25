<template>
    <div>
        <q-toolbar>
            <q-btn class="q-ml-xs" color="blue-10" dense icon="menu" flat>
                <q-menu>
                    <q-list dense>
                        <q-item clickable v-close-popup :to="{ name: 'iexcloud-loader' }" v-if="false">
                            <q-item-section class="text-subtitle1">
                                <div>Carga de series desde <span class="text-blue-10 text-bold">iexcloud</span></div>
                            </q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click="store.abrir_w_nasdaq_loader()">
                            <q-item-section class="text-subtitle1">
                                <div>Carga de series desde <span class="text-blue-10 text-bold">Csv Nasdaq</span></div>
                            </q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click="win_marketstack_loader_open = true" v-if="false">
                            <q-item-section class="text-subtitle1">
                                <div>Carga de series desde <span class="text-blue-10 text-bold">marketstack</span></div>
                            </q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click="win_marketdata_loader_open = true">
                            <q-item-section class="text-subtitle1">
                                <div>Carga de series desde <span class="text-blue-10 text-bold">marketdata</span></div>
                            </q-item-section>
                        </q-item>

                        <q-item clickable v-close-popup @click="win_alphavantage_loader_open = true">
                            <q-item-section class="text-subtitle1">
                                <div>Carga de series desde <span class="text-blue-10 text-bold">alphavantage</span></div>
                            </q-item-section>
                        </q-item>

                        <q-item clickable v-close-popup @click="win_massive_loader_open = true">
                            <q-item-section class="text-subtitle1">
                                <div>Carga de series desde <span class="text-blue-10 text-bold">massive</span></div>
                            </q-item-section>
                        </q-item>

                        <q-item clickable v-close-popup @click="win_investing_csv_loader_open = true">
                            <q-item-section class="text-subtitle1">
                                <div>Carga de series desde <span class="text-blue-10 text-bold">Investing CSV</span>
                                </div>
                            </q-item-section>
                        </q-item>
                    </q-list>
                </q-menu>
            </q-btn>
            <q-toolbar-title class="text-blue-10">Series</q-toolbar-title>
        </q-toolbar>
        <q-card>
            <!--
            <div class="q-pl-xs row">
                <div class="col-3">
                    <router-view></router-view>                
                </div>
            </div>                       
            <q-separator/>         
            -->
            <div class="col">
                <div class="row">
                    <div class="col">
                        <TableResumenSerie />
                    </div>
                </div>
            </div>
        </q-card>
        <WinNasdaqCsvLoader v-model="store.state.w_nasdaq_loader.open" />
        <WinMarketStackLoader v-model="win_marketstack_loader_open" />
        <WinMarketDataLoader v-model="win_marketdata_loader_open" />
        <WinAlphavantageLoader v-model="win_alphavantage_loader_open" />
        <WinMassiveLoader v-model="win_massive_loader_open" />
        <WinInvestingLoader v-model="win_investing_csv_loader_open" />
    </div>
</template>
<script>
import store from './store'
import TableResumenSerie from '@/components/serie/TableResumenSerie.vue'
import WinNasdaqCsvLoader from './WinNasdaqCsvLoader.vue'
import WinMarketStackLoader from './WinMarketStackLoader.vue'
import WinMarketDataLoader from './WinMarketDataLoader.vue'
import WinInvestingLoader from './WinInvestingLoader.vue'
import WinAlphavantageLoader from './WinAlphavantageLoader.vue'
import WinMassiveLoader from './WinMassiveLoader.vue'
//import PanelSerieLoader from '@/components/serie/PanelSerieLoader.vue'
export default {
    name: "MainMantSerie",
    components: {
        TableResumenSerie,
        WinNasdaqCsvLoader,
        WinMarketStackLoader,
        WinMarketDataLoader,
        WinInvestingLoader,
        WinAlphavantageLoader,
        WinMassiveLoader
        //      PanelSerieLoader
    },
    data: () => {
        return {
            visible: 0,
            store: store,
            win_marketstack_loader_open: false,
            win_marketdata_loader_open: false,
            win_investing_csv_loader_open: false,
            win_alphavantage_loader_open: false,
            win_massive_loader_open: false
        }
    }
}
</script>