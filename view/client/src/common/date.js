import date from 'date-and-time';
var func = {
    iso_to_format:function(data, format){
        let pdata = date.parse(data, 'YYYY-MM-DD')
        return date.format(pdata, format)
    },
    format_to_iso:function(data, format){           
        let pdata = date.parse(data, format)        
        return date.format(pdata, 'YYYY-MM-DD')
    }
}

export default func