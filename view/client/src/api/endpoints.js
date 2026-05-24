export const SERIE = {
    MARKETSTACK_LOAD: "SerieManager/MarketStackLoaderController/load",
    MARKETDATA_LOAD: "SerieManager/MarketDataLoaderController/load",
    INVESTING_LOAD: "SerieManager/InvestingLoaderController/load"
}

export const OPERACION = {
    IBKR_LOAD: "operacion/IbkrLoaderController/cargar_operaciones_ibkr",
    IBKR_LOAD_DETAIL: "operacion/IbkrLoaderController/get_ibkr_import_trades_detail",
    IBKR_GEN_TRANSACCIONES: "operacion/GeneradorTransaccionController/generar"
}

export const TRANSACCION = {
    GET_FECHAS_CON_TRANSACCIONES: "transaccion/TransaccionController/get_fechas_con_transacciones",
    GET_TRANSACCIONES_X_FECHA: "transaccion/TransaccionController/get_transacciones_x_fecha",
    GET_TRANSACCIONES_X_SYMBOL: "transaccion/TransaccionController/get_transacciones_x_symbol",
    GET_MAX_FECHAS_AGROUPADAS_X_SYMBOL: "transaccion/TransaccionController/get_max_fechas_agroupadas_x_symbol"
}