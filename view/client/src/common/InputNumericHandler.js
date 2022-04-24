var func = {
    preventInvalidNumbers:function(event){
        console.log(event)
        var value = event.target.value

        //keycodes
        /*
        - del 48 al 57 los numeros del 0 al 9
        - del 96 al 105 los numeros del 0 al 9 del teclado numerico
        - 37 y 39 (flech izquierda, flecha derecha)
        - 110 punto decimal
        - 8 backspace
        - 46 suprimir
        - 16 shift
        - 36 inicio
        - 35 fin
        - 86 (control + v)
        - 9 tab
        */       
        if (
            !(
                (event.keyCode >= 48 && event.keyCode <= 57) ||
                (event.keyCode >= 96 && event.keyCode <= 105) ||
                (event.keyCode == 37 || event.keyCode == 39) ||
                (event.keyCode == 110) ||
                event.keyCode == 8 ||
                event.keyCode == 46 ||
                event.keyCode == 16 ||
                event.keyCode == 36 ||
                event.keyCode == 35 ||
                event.keyCode == 9 ||
                (event.keyCode==86 && event.ctrlKey == true)
            )
        ){                
           event.preventDefault()               
        }

        if (value == "0" && 
            (
                (event.keyCode >= 48 && event.keyCode <= 57) ||
                (event.keyCode >= 96 && event.keyCode <= 105)
            )
        ){
            event.preventDefault()
        }
                
        /**
         * Si ya existe el . decimal no hace nada
        */
        if (value.indexOf(".") != -1 &&  event.keyCode == 110){
            event.preventDefault()
        }   
        
        /*
        Si existe mas de 2 decimales retornar el valor cortado
        */        
    },
    formatDecimal:function(value, decimals){        
        
        //verify if string is an decimal
        if (isNaN(Number(value))){
            return ""
        }    
        //Si es un string como float 
        let pos = value.indexOf(".")

        //si no hay decimal devuelve todo el valor        
        if (pos == -1){
            return value
        }        
        
        let len = value.length
        len = len - (len-(pos+1)-decimals)                

        console.log(value.substring(0, len))
        return value.substring(0, len)
    }
}

export default func