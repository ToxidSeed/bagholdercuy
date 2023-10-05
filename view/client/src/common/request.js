function config(){
    return {
        headers:{
            'Authorization':localStorage.getItem("token")
        }
    }
}

//console.log(localStorage.getItem("token"))

let postconfig = function(){
    return {
        headers:{
            'Authorization':localStorage.getItem("token")
        }
    }
}

let get_postconfig = function(){
    return {
        headers:{
            'Authorization':localStorage.getItem("token")
        }
    }
}

export {config, postconfig, get_postconfig}
