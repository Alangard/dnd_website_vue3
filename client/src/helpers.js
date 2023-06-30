
// Places "and" or "," as word separators in sentences
export function Separator (index, array_of_objects = []) {
      if(array_of_objects.length > 2){
        if(index == array_of_objects.length - 2){return ' and '}
        else if(index < array_of_objects.length - 1){return ', '}
        else{return ''}
      }
      else if(array_of_objects.length == 2){
        if(index < 1){return ' and '}
      }
}

// Convert datetime to the format "n-time from publication
export function DateTimeFormat (datetime_str) {
    let moment = require('moment');
    return moment(datetime_str).fromNow()
}






