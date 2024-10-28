export default {
    imp_cierre_ant:0,
    imp_apertura:0,
    imp_maximo:0,
    imp_minimo:0,
    imp_cierre_act:0,
    imp_variacion:0,
    pct_variacion:0,
    fill_variacion_semana_actual: async function(data){
        console.log(data)
        this.imp_cierre_ant = data.imp_cierre_ant
        this.imp_apertura = data.imp_apertura
        this.imp_maximo = data.imp_maximo
        this.imp_minimo = data.imp_minimo
        this.imp_cierre_act = data.imp_cierre
        this.imp_variacion = data.imp_variacion_cierre
        this.pct_variacion = data.pct_variacion_cierre
    }
}