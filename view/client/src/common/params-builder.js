import { ParamNotFoundError, ParamEmptyError } from "./custom-error"
import _ from "lodash"

export class ParamsBuilder{
    constructor(data){
        this.data = data
        this._config = {}
        this._output = {}
    }

    requerido = function(param_name){                
        if (!(param_name in this.data)){
            throw new ParamNotFoundError(`No se ha encontrado el parametro ${param_name}`)         
        }        
        if (_.includes(["", undefined, null], this.data[param_name]) == true){
            throw new ParamEmptyError(`El parametro ${param_name} no puede estar vacío`)
        }
    }

    validar_campo = function(campo, configuracion){                      
        if (configuracion.requerido == true){            
            this.requerido(campo)
        }        
    }
    
    add = function(campo, config){
        this.validar_campo(campo, config)
        this._output[campo] = this.data[campo]
        this._config[campo] = config
    }

    get output(){
        return this._output
    }

    get config(){
        return this._config
    }
}