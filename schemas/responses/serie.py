from config.extensions import ma


class SeriesSynchronizationResponseSchema(ma.Schema):
    market_data_provider = ma.String()
    cod_symbol = ma.String()
    fch_min_serie = ma.Date(allow_none=True)
    fch_max_serie = ma.Date(allow_none=True)


series_synchronization_response_schema = SeriesSynchronizationResponseSchema()
