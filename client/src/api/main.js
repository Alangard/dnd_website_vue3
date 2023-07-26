import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/v1/'

const interceptorsInstance = axios.create({baseURL: axios.baseURL});

// Настройка interceptors
interceptorsInstance.interceptors.response.use(
    (response) => response,

    async (error) => {
      const originalRequest = error.config;
      
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
  
        try {
          // Authorization failed due to invalid token
          const token = await getNewToken();
          // Repeat the request with a new token
          originalRequest.headers['Authorization'] = `Bearer ${token}`;
          return interceptorsInstance(originalRequest);
        } catch (error) {
          // Handling the error of getting a new token
          throw new Error('Failed to get a new token');
        }
      }
      return Promise.reject(error);
    }
)


async function getNewToken() {
  try {
    const refresh = JSON.parse(localStorage.getItem('user')).refresh
    const user_data = JSON.parse(localStorage.getItem('user')).user_data

    const response = await axios.post('auth/jwt/refresh/', {refresh: refresh});
    const newToken = response.data.access;

    localStorage.setItem('user', JSON.stringify({'user_data': user_data, 'access': newToken, 'refresh': refresh}))

    return newToken;
  } catch (error) {
    // Handling the error of getting a new token
    throw new Error('Failed to get a new token');
  }
}


export function authHeader(){
    let user = JSON.parse(localStorage.getItem('user'));

    if(user && user.access){
        return { Authorization: 'Bearer ' + user.access }
    }
    else{
        return {};
    }
}

export default interceptorsInstance