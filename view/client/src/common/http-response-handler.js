import { HttpError } from "./custom-error"
import store from "@/store/store"

export class HttpResponseHandler{
    static throwIfError = function(response){
        let response_data = response.data                

        if (response_data.success == false){                             
            throw new HttpError(response_data.message, response)
        }
    }
    static showMessage = function(response){
        store.dispatch("incluir_httpresp", response)
    }
    static showMessageIfError = function(response){
        store.dispatch("incluir_httpresp_si_apperror", response)
    }
}