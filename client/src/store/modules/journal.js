import AuthService from '@/api/AuthAPI/auth';
import authHeader from '@/api/AuthAPI/auth-header';



const user = JSON.parse(localStorage.getItem('user'));
const initialState = user
  ? { status: { loggedIn: true }, user }
  : { status: { loggedIn: false }, user: null };

export const journal = {
  namespaced: true,
  state: initialState,
  actions: {
    get_posts({ commit }, user) {
        if(user && user.refresh){
            if(AuthService.expired_token(user.refresh)){dispatch("auth/login", user_data)}
            else{
                if(AuthService.expired_token(user.access)){AuthService.refresh_access_token()}
            }
        }

        return axios.get(BASE_URL + 'posts/', { headers: authHeader() })
    }
  },


  mutations: {
    loginSuccess(state, user) {
      state.status.loggedIn = true;
      state.user = user;
    },
    loginFailure(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    logout(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    registerSuccess(state) {
      state.status.loggedIn = false;
    },
    registerFailure(state) {
      state.status.loggedIn = false;
    }
  },
  getters: {
    loginState(state){
      return state.status.loggedIn
    }
  }

};