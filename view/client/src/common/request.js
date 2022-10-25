function config(){
    return {
        headers:{
            'Authorization':localStorage.getItem("token")
        }
    }
}

export {config}
