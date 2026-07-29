<template>
    <q-page class="q-pl-md q-pr-md">
        <!-- Header of the page -->

        <!-- Main Card -->
        <q-card class="ibkr-sync-card q-pa-xl row items-center justify-between no-wrap">
            <!-- Left Side -->
            <div class="col col-grow q-pr-xl column justify-between" style="min-height: 200px;">
                <div>

                    <!-- Title -->
                    <div class="text-h3 text-weight-bold text-grey-9 q-mb-md">
                        IBKR Contracts Sync Center
                    </div>

                    <!-- Description -->
                    <div class="text-subtitle1 text-grey-6 q-mb-lg" style="max-width: 700px; line-height: 1.6;">
                        Recupera y actualiza las definiciones de contrato más recientes de la API de Interactive
                        Brokers. Esta acción refresca los conids, símbolos y datos de registro del portafolio completo.
                    </div>
                </div>

                <!-- Stats Row -->
                <div class="row q-gutter-x-xl q-mt-xs">
                    <div>
                        <div class="text-caption text-weight-bold text-grey-5 uppercase-tracking q-mb-xs">LAST SYNC
                        </div>
                        <div class="text-h6 text-weight-bold text-grey-8">{{ lastSync }}</div>
                    </div>
                    <div>
                        <div class="text-caption text-weight-bold text-grey-5 uppercase-tracking q-mb-xs">TOTAL RECORDS
                        </div>
                        <div class="text-h6 text-weight-bold text-grey-8">{{ totalRecords }}</div>
                    </div>
                    <div>
                        <div class="text-caption text-weight-bold text-grey-5 uppercase-tracking q-mb-xs">STATUS</div>
                        <div class="q-mt-xs">
                            <q-chip dense class="text-weight-medium text-subtitle2 q-ma-none q-px-sm"
                                :class="statusBadgeClass">
                                {{ statusText }}
                            </q-chip>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Side (Sync Button Card) -->
            <div class="col-auto">
                <q-btn flat no-caps :loading="syncing" class="sync-btn-card text-white q-pa-md" @click="handleSync">
                    <template v-slot:loading>
                        <div class="column items-center justify-center">
                            <q-spinner-oval size="44px" class="q-mb-md" />
                            <div class="text-h6 text-weight-bold q-mb-xs">Syncing...</div>
                            <div class="text-caption text-blue-2 text-weight-medium">Updating portfolio conids</div>
                        </div>
                    </template>

                    <div class="column items-center justify-center">
                        <q-icon name="cloud_sync" size="44px" class="q-mb-md" />
                        <div class="text-h6 text-weight-bold q-mb-xs">Sync All Contracts</div>
                    </div>
                </q-btn>
            </div>
        </q-card>

        <!-- Search / Filter Bar -->
        <div class="row items-center justify-between q-mt-xl q-mb-md no-wrap">
            <div class="row items-center q-gutter-x-sm col">
                <!-- Search Input -->
                <q-input v-model="filterSymbol" outlined dense placeholder="Filter by Symbol (e.g. AAPL, TSLA)..."
                    class="bg-white filter-input col-grow" style="max-width: 350px;">
                    <template v-slot:prepend>
                        <q-icon name="filter_list" size="20px" class="text-grey-6" />
                    </template>
                </q-input>

                <!-- Exchange Dropdown -->
                <q-select v-model="selectedExchange" :options="exchangeOptions" outlined dense
                    class="bg-white exchange-select" style="width: 180px;" />

                <!-- Apply Button -->
                <q-btn label="Apply" no-caps unelevated class="apply-btn text-weight-medium q-px-md"
                    @click="applyFilters" />
            </div>

            <div class="row items-center q-gutter-x-md text-grey-8">
                <div class="text-subtitle2 text-weight-regular">Display: {{ filteredData.length }} rows</div>

                <!-- View Mode toggle group -->
                <div class="view-toggle-group row no-wrap">
                    <q-btn flat dense icon="table_chart"
                        :class="viewMode === 'grid' ? 'active-toggle' : 'inactive-toggle'" @click="viewMode = 'grid'" />
                    <q-btn flat dense icon="list" :class="viewMode === 'list' ? 'active-toggle' : 'inactive-toggle'"
                        @click="viewMode = 'list'" />
                </div>
            </div>
        </div>

        <!-- Table -->
        <q-table :data="filteredData" :columns="columns" row-key="conid" dense flat :pagination="pagination"
            separator="vertical" class="contracts-table border-table">
        </q-table>
    </q-page>
</template>

<script>
import IbkrApi from "@/api/ibkr.js"
import { HttpResponseHandler } from "@/common/http-response-handler.js"

export default {
    name: "IbkrContractsPage",
    data() {
        return {
            syncing: false,
            lastSync: "2023-10-27 14:30",
            totalRecords: "1,240",
            statusText: "Ready",

            filterSymbol: "",
            selectedExchange: "All Exchanges",
            appliedFilterSymbol: "",
            appliedSelectedExchange: "All Exchanges",
            exchangeOptions: ["All Exchanges", "NASDAQ", "NYSE", "ARCA", "BATS"],
            viewMode: "grid",

            pagination: {
                rowsPerPage: 20
            },
            columns: [
                {
                    name: 'conid',
                    label: 'CONID (PK)',
                    align: 'left',
                    field: 'conid',
                    sortable: true,
                    style: "width:50px"
                },
                {
                    name: 'cod_symbol',
                    label: 'SYMBOL',
                    align: 'left',
                    field: 'cod_symbol',
                    sortable: true,
                    style: "width:50px"
                },
                {
                    name: 'exchange',
                    label: 'EXCHANGE',
                    align: 'left',
                    field: 'exchange',
                    sortable: true,
                    style: "width:50px"
                },
                {
                    name: 'fch_hr_registro',
                    label: 'REGISTRATION DATE',
                    align: 'left',
                    field: 'fch_hr_registro',
                    sortable: true,
                    style: "width:50px"
                },
                {
                    name: '',
                    label: '',
                    align: 'right',
                    field: ''
                }
            ],
            data: [
                {
                    conid: 4391,
                    cod_symbol: "AAPL",
                    exchange: "NASDAQ",
                    fch_hr_registro: "2023-10-27 14:30:12"
                },
                {
                    conid: 265598,
                    cod_symbol: "TSLA",
                    exchange: "NASDAQ",
                    fch_hr_registro: "2023-10-27 14:31:00"
                },
                {
                    conid: 271439,
                    cod_symbol: "MSFT",
                    exchange: "NASDAQ",
                    fch_hr_registro: "2023-10-27 14:32:45"
                },
                {
                    conid: 12087,
                    cod_symbol: "SPY",
                    exchange: "ARCA",
                    fch_hr_registro: "2023-10-27 14:35:10"
                },
                {
                    conid: 495512572,
                    cod_symbol: "NVDA",
                    exchange: "NASDAQ",
                    fch_hr_registro: "2023-10-28 09:15:30"
                }
            ]
        };
    },
    computed: {
        statusBadgeClass() {
            if (this.syncing) {
                return "text-orange-9 bg-orange-1";
            }
            return "text-teal-8 bg-teal-1";
        },
        filteredData() {
            return this.data.filter(item => {
                const matchesSymbol = this.appliedFilterSymbol ?
                    item.cod_symbol.toLowerCase().includes(this.appliedFilterSymbol.toLowerCase()) : true;
                const matchesExchange = this.appliedSelectedExchange && this.appliedSelectedExchange !== 'All Exchanges' ?
                    item.exchange.toLowerCase() === this.appliedSelectedExchange.toLowerCase() : true;
                return matchesSymbol && matchesExchange;
            });
        }
    },
    methods: {
        applyFilters() {
            this.appliedFilterSymbol = this.filterSymbol;
            this.appliedSelectedExchange = this.selectedExchange;
        },
        handleSync() {
            if (this.syncing) return;

            const exchangeToSync = this.selectedExchange === 'All Exchanges' ? 'AMEX' : this.selectedExchange;

            this.syncing = true;
            this.statusText = "Syncing";

            const api = new IbkrApi();
            api.sync_all_conids({ exchange: exchangeToSync })
                .then(httpresp => {
                    HttpResponseHandler.showMessage(httpresp);

                    // Update last sync date info
                    const now = new Date();
                    const formattedDate = now.getFullYear() + '-' +
                        String(now.getMonth() + 1).padStart(2, '0') + '-' +
                        String(now.getDate()).padStart(2, '0') + ' ' +
                        String(now.getHours()).padStart(2, '0') + ':' +
                        String(now.getMinutes()).padStart(2, '0');

                    this.lastSync = formattedDate;

                    if (httpresp.data && httpresp.data.success) {
                        const count = httpresp.data.data ? httpresp.data.data.inserted_count : 0;
                        console.log(count)
                        this.$q.notify({
                            type: 'positive',
                            message: httpresp.data.message || `Sincronización exitosa de conids para ${exchangeToSync}`
                        });
                    }
                })
                .catch(err => {
                    this.$q.notify({
                        type: 'negative',
                        message: `Error al sincronizar contratos: ${err.message || err}`
                    });
                })
                .finally(() => {
                    this.syncing = false;
                    this.statusText = "Ready";
                });
        }
    }
};
</script>

<style scoped>
.ibkr-sync-card {
    position: relative;
    border-radius: 16px;
    background-color: #ffffff;
    background-size: 24px 24px;
    border: 1px solid rgba(0, 0, 0, 0.06);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
    overflow: hidden;
}

.dot-indicator {
    width: 8px;
    height: 8px;
    background-color: #26a69a;
    /* teal-5 */
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(38, 166, 154, 0.5);
    }

    70% {
        box-shadow: 0 0 0 10px rgba(38, 166, 154, 0);
    }

    100% {
        box-shadow: 0 0 0 0 rgba(38, 166, 154, 0);
    }
}

.uppercase-tracking {
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-size: 0.75rem;
}

.sync-btn-card {
    width: 260px;
    height: 200px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(21, 101, 216, 0.2);
    background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.sync-btn-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 14px 30px rgba(21, 101, 216, 0.35);
    background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
}

.sync-btn-card:active {
    transform: translateY(-1px);
}

/* Filter bar styles */
.filter-input>>>.q-field__control {
    border-radius: 6px !important;
}

.exchange-select>>>.q-field__control {
    border-radius: 6px !important;
}

.apply-btn {
    background-color: #f7f9fd;
    color: #1e3a8a;
    border: 1px solid rgba(30, 58, 138, 0.15);
    border-radius: 6px;
    height: 40px;
    font-size: 0.9rem;
    transition: all 0.2s ease;
}

.apply-btn:hover {
    background-color: #eff6ff;
    border-color: rgba(30, 58, 138, 0.3);
}

/* View toggle button group */
.view-toggle-group {
    border: 1px solid rgba(0, 0, 0, 0.12);
    border-radius: 6px;
    overflow: hidden;
}

.active-toggle {
    background-color: #eff6ff;
    color: #1e88e5;
    width: 40px;
    height: 36px;
    border-radius: 0;
}

.inactive-toggle {
    background-color: #ffffff;
    color: #616161;
    width: 40px;
    height: 36px;
    border-radius: 0;
}

/* Table styling */
.border-table {
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 8px;
    overflow: hidden;
}

.contracts-table>>>.q-table th {
    color: #374151;
    /* grey-8 */
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.5px;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.contracts-table>>>.q-table td {
    padding: 12px 16px;
}
</style>
