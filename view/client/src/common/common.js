function headers(){    
    let headers = {
        'Authorization':localStorage.getItem("token")
    }
    return headers
}

export {headers}    