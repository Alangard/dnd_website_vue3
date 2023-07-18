import axios from 'axios'
import authHeader from './auth-header';

const BASE_URL = 'api/v1/auth/'

class AuthService {
    login(user_data){
        return axios.post(BASE_URL + 'jwt/create/', 
            {
                username: user_data.username,
                password: user_data.password
            }
        )
        .then(response => {
            if(response.data.access){
                localStorage.setItem('user', JSON.stringify(response.data))
            }

            return response.data;
        });
    }

    logout(){
        localStorage.removeItem('user');
    }

    user_create(user_data){
        return axios.post(BASE_URL + 'user/register/', 
            {
                username: user_data.username,
                email: user_data.email,
                password: user_data.password,
            }
        )
    }

    user_activate(user_data){
        return axios.post(BASE_URL + 'user/activation/',
            {
                email: user_data.email,
                confirmation_code: user_data.activation_code 
            }
        )
    }

    resend_confirmation_code(email){
        return axios.post(BASE_URL + 'user/resend_confirmation_code/', 
            {
                email: email
            }
        )
    }

    user_get(){
        return axios.get(BASE_URL + 'users/me/', { headers: authHeader() })
    }

    user_put(user_data){
        return axios.put(BASE_URL + 'users/me/', user_data, { headers: authHeader()})
    }

    user_patch(user_data){
        return axios.put(BASE_URL + 'users/me/', user_data, { headers: authHeader()})
    }

    user_delete(user_data){
        return axios.put(BASE_URL + 'users/me/', {current_password: user_data.current_password}, { headers: authHeader()})
    }

    reset_password(user_data){
        return axios.patch(BASE_URL + 'user/reset_password/', 
            {
                email: user_data.email,
            }
        );
    }

    reset_password_confirmation(user_data){
        return axios.patch(BASE_URL + 'user/reset_password_confirm/', 
            {   
                confirmation_code: user_data.confirmation_code,
                new_password:  user_data.new_password,
            }
        );
    }

    refresh_access_token(){
        const refresh = JSON.parse(localStorage.getItem('user')).refresh
        const user_data = JSON.parse(localStorage.getItem('user')).user_data

        return axios.post(BASE_URL + 'jwt/refresh/', 
            {
                refresh: refresh
            }
        )
        .then(response => {
            localStorage.setItem('user', JSON.stringify({'user_data': user_data, 'access': response.data.access, 'refresh': refresh}))
            return response.data;
        });
    }

    verify_access_token(){
        const access = JSON.parse(localStorage.getItem('user')).access

        return axios.post(BASE_URL + 'jwt/verify/', 
            {
                token: access
            }
        )
    }

    expired_token(token){
        let base64Url = token.split(".")[1];
        let base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
        let jsonPayload = decodeURIComponent(
            atob(base64).split("").map(function(c) {
                return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
            }).join("")
        );

        const result_JWT_data = JSON.parse(jsonPayload);
        const expiration_datetime = new Date(result_JWT_data.exp * 1000);
        const now_datetime = new Date();
        const delta_datetime = Math.abs(expiration_datetime - now_datetime) * 1000;
        
        if(delta_datetime < 60){
            
            console.log(`exp: ${expiration_datetime}   now: ${now_datetime}   delta: ${delta_datetime}`)
            return true}
        else{return false}
          
    }

}

export default new AuthService();