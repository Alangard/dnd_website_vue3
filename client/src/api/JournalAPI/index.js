import axios from 'axios'
import authHeader from '../AuthAPI/auth-header';

const BASE_URL = '/api/v1/';


class JournalService {
    get_posts(url){
        return axios.get(BASE_URL + url, { headers: authHeader() })        
    }

}

export default new JournalService();