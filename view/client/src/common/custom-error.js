export class HttpError extends Error{
    constructor(message, httpresponse){        
        super(message)
        this.httpresponse = httpresponse
    }
}

export class ParamNotFoundError extends Error{
    constructor(message){
        super(message)
    }
}

export class ParamEmptyError extends Error{
    constructor(message){
        super(message)
    }
}