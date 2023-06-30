import JournalService from '@/api/JournalAPI/index'


const user = JSON.parse(localStorage.getItem('user'));
const initialState = user
  ? { status: { loggedIn: true }, user, haveInitialPosts: false, PostsList: [] }
  : { status: { loggedIn: false }, user: null, haveInitialPosts: false, PostsList: [] };

export const journal = {
  namespaced: true,
  state: initialState,
  actions: {
    get_posts({ commit }, url) {
      return JournalService.get_posts(url).then(
        posts_data => {
          commit('gettingPostSuccess', posts_data.data);
          return Promise.resolve(posts_data.data);
        },
        error => {
          commit('gettingPostFailure');
          return Promise.reject(error);
        }
      );
    },


  },


  mutations: {

    gettingPostSuccess(state, posts_data){
      state.haveInitialPosts = true;
      state.PostsList = posts_data
    },

    gettingPostFailure(state){
      state.haveInitialPosts = false;
    },
  },

  getters: {
    loginState(state){
      return state.status.loggedIn
    },

    getPostsData(state){
      return state.PostsList
    },

    getPosts(state){
      return state.PostsList.results
    }
  }

};