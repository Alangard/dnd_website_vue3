import { createStore } from 'vuex'

export default createStore({
  state(){
    return{
      isMobile: true,
      is_favorite: true,
      theme: '',
      postData: {
        '1985':{
                data: {post_id:'1985', post_img : 'dsdsdsd', creator_nickname: 'User1.804838', post_date: '21 July 2022 21:37', title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.1', description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.'},
                reactions: [ {'name':"12.gif", data: [{'username': 'user1.804838', 'profile_img': '', 'date': '1995-12-17T03:24:00'}]},
                            {'name':"15.gif", data: [{'username': 'user19.804856', 'profile_img': '', 'date': '1997-12-17T03:24:00'}, {'username': 'user122.804737', 'profile_img': '', 'date': '1995-12-21T03:24:00'}, {'username': 'user299.804802', 'profile_img': '', 'date': '1995-12-17T03:24:00'}]},
                            {'name':"19.gif", data: [{'username': 'user32.804871', 'profile_img': '', 'date': '1995-12-17T09:24:00'}, {'username': 'user33.804708', 'profile_img': '', 'date': '1995-12-17T07:24:00'}, {'username': 'user35.804254', 'profile_img': '', 'date': '1995-12-17T05:24:00'}, {'username': 'user24.804824', 'profile_img': '', 'date': '1995-12-17T21:24:00'}, {'username': 'user11.804816', 'profile_img': '', 'date': '1995-12-17T23:12:00'}, {'username': 'user65.804811', 'profile_img': '', 'date': '1995-12-17T21:25:00'}, ]},
                            {'name':"29.gif", data: [{'username': 'user42.804835', 'profile_img': '', 'date': '2009-12-17T03:24:00'}, {'username': 'user44.804844', 'profile_img': '', 'date': '2009-12-18T03:24:00'}]},
                            {'name':"9.gif", data: [{'username': 'user12.804833', 'profile_img': '', 'date': '2009-12-17T03:25:00'}]}
                          ],
                tag_list: [1, 2, 4], comments:{'counter': 290, data:{}}
                },
        '2009':{
                data: {post_id:'2009', post_img : '', creator_nickname: 'User2.804839', post_date: '1 January 2022 22:54', title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.2', description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.'},
                reactions: [ {'name':"9.gif", data: [{'username': 'user12.804833', 'profile_img': '', 'date': '2002-12-17T03:24:00'}, {'username': 'user9.804899', 'profile_img': '', 'date': '2002-12-17T03:27:00'}]}
                           ],
                tag_list: [1, 2, 3], comments:{'counter': 11, data:{}}
                },
        '1':{
                data: {post_id:'1', post_img : 'dsd',creator_nickname: 'User4.804841', post_date: '1 August 2021 19:10', title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.3', description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.'},
                reactions: [],
                tag_list: [1], comments:{'counter': 27, data:{}}
            },
      },

      
      
     
    }
  },
  getters: {
    getIsMobileState (state) {
        return state.isMobile;
      
    },

    getTheme (state){
        return state.theme;
    },

    getPostData (state){
      return state.postData;
    },

    getReactionByPostId: state => post_id =>{
      return state.reactions[post_id];
    },

    getStatus(state){
      return state.is_favorite;
    }
  },

  mutations: {
    changeIsMobileFlag (state, flag_pos) {
        state.isMobile = flag_pos;
    },

    changeTheme (state, chose_theme){
        state.theme = chose_theme;
        console.log(state.theme)
    },

    printData (state, post_id){
      console.log(state.postData[post_id])
    },

    changeStatus(state){
      state.is_favorite = !state.is_favorite;
      console.log(state.is_favorite)
    }

  /*  changePostData (state, post_id, new_postData){
      state.postData[post_id] = new_postData;
      console.log(state.postData[post_id])
    }
  */
  },

  actions: {
  },
  modules: {
  }
})
