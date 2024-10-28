import { ParamNotFoundError, ParamEmptyError } from "./custom-error"
import _ from "lodash"

export class ParamsHelper{
    constructor(params){
        if (params == undefined){
            throw new Error("No se ha indicado ningun parametro")
        }
        this.input_params = params        
        this.output = {}
    }

    get_param = function(param_name, requerido=false){
        if (!(param_name in this.input_params)){
            if (requerido == true){
                throw new ParamNotFoundError(`No se ha encontrado el parametro ${param_name}`)
            }

            return ""
        }

        return this.input_params[param_name]
    }    

    val = function(param_name, requerido=false){
        if (requerido == true){
            this.requerido(param_name)  
        }                
    }

    validar = function(config){         
        for (let campo in config){            
            this.validar_campo(campo, config[campo])
        }
    }

    validar_campo = function(campo, configuracion){                      
        if (configuracion.requerido == true){            
            this.requerido(campo)
        }
        
    }

    requerido = function(param_name){                
        if (!(param_name in this.input_params)){
            throw new ParamNotFoundError(`No se ha encontrado el parametro ${param_name}`)         
        }        
        if (_.includes(["", undefined, null], this.input_params[param_name]) == true){
            throw new ParamEmptyError(`El parametro ${param_name} no puede estar vacío`)
        }
    }

    build = function(config){
        for (let campo in config){            
            this.validar_campo(campo, config[campo])
            this.ouput[campo] = this.input_params[campo]
        }
    }

    add = function(campo, config){
        this.validar_campo(campo, config)
        this.output[campo] = this.input_params[campo]
    }
}