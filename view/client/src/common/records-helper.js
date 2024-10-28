class RecordsHelper{
    constructor(records){
        this.records = records
    }

    toFixed = function(config){
        this._formatear_registros()                
    }

    _formatear_registros = function(config){
        for (record in this.records){
            this._formatear_campos(record, config)
        }
    }

    _formatear_campos = function(record, config){
        for (campo in config){
            
        }
    }
}


/**
 * 
 * CALL 490
 */