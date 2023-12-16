export class HttpError extends Error{
    constructor(message, httpresponse){
        super(message);
        this.httpresponse = httpresponse
    }
}

