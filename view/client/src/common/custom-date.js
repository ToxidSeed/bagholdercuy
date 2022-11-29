import date from 'date-and-time'
import {CLIENT_DATE_FORMAT,ISO_DATE_FORMAT} from '@/common/constants.js'

const cdate = {
    iso_to_client:function(value){
        return date.transform(value,ISO_DATE_FORMAT, CLIENT_DATE_FORMAT)
    }
}

export {cdate}