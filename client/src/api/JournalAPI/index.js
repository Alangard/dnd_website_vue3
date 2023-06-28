import axios from 'axios'
import useStore from 'vuex'
import AuthService from '@/api/AuthAPI/auth';
import authHeader from '../AuthAPI/auth-header';

const user = JSON.parse(localStorage.getItem('user'));
const store = useStore();
const BASE_URL = '/api/v1/';


class JournalService {
    get_post(user_data){
        if(AuthService.expired_token(user.refresh)){
            store.dispatch("auth/login", user_data)
        }
        else{
            if(AuthService.expired_token(user.access)){
                AuthService.refresh_access_token()
            }
        }
        return axios.get(BASE_URL + 'posts/', { headers: authHeader() })
    }

    // refresh_access_token(){
    //     return axios.post(JWT_URL + 'refresh/', 
    //         {
    //             refresh: JSON.parse(localStorage.getItem('user')).refresh
    //         }
    //     )
    //     .then(response => {
    //         localStorage.setItem('user', JSON.stringify(response.data))
    //         return response.data;
    //     });
    // }

    // expired_token(token){
    //     let base64Url = token.split(".")[1];
    //     let base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    //     let jsonPayload = decodeURIComponent(
    //         atob(base64).split("").map(function(c) {
    //             return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
    //         }).join("")
    //     );

    //     const result_JWT_data = JSON.parse(jsonPayload);
    //     const expiration_datetime = new Date(result_JWT_data.exp * 1000);
    //     const now_datetime = new Date();
    //     const delta_datetime = Math.abs(expiration_datetime - now_datetime) * 1000;
        
    //     if(delta_datetime <= 80 && delta_datetime >= 60){return true}
    //     else{return false}
          
    // }

}

export default new JournalService();