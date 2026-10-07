class InteractiveBrokersSeriesService:
    """
    Interactive brokers entrega las series diarias por lo que luego se tendra que cargar en las tablas respectivas.

    - Series Diarias (Se Carga con la data de interactive brokers)
    - Variaciones Diarias (Se Carga a partir de las series diarias)
    - Series Semanales (Se Carga a partir de las series diarias)
    - Variaciones Semanales (Se Carga a partir de las series diarias)
    - Series Mensuales (Se Carga a partir de las series diarias)
    - Variaciones Mensuales (Se Carga a partir de las series diarias)
    
    """
    def load(self, cod_symbol, df_series, modo_carga):
        pass    