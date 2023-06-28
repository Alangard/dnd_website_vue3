import { moment } from 'moment'

export const DateTimeFormat = (datetime_str) => {
    let moment = require('moment');
    return moment(datetime_str).fromNow()
}

