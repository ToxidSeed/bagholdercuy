class GestorObjeto{
    constructor(objeto){
        this.objeto = objeto
    }

    reset = function(defaults={}){
        for (let element in this.objeto){
            if (element in defaults){
                this.objeto[element] = defaults[element]    
            }else{
                this.objeto[element] = ""
            }            
        }
    }

    set_campos = function(objeto_referencia){
        for (let element in this.objeto){
            if (element in objeto_referencia){
                this.objeto[element] = objeto_referencia[element]
            }
        }
    }

    set_data = function(objeto_referencia={}){
        for (let element in objeto_referencia){            
            this.objeto[element] = objeto_referencia[element]
        }
    }        

    get_elemento = function(nom_elemento){
        if (this.objeto == null || this.objeto == undefined){
            return ""
        }
        
        if (!(nom_elemento in this.objeto)){
            return ""
        }
        if (this.objeto[nom_elemento] == undefined){
            return ""
        }

        if (this.objeto[nom_elemento] == null){ 
            return ""
        }

        return this.objeto[nom_elemento]
    }
}

export default GestorObjeto