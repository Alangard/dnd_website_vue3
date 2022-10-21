import { createStore } from 'vuex'

export default createStore({
  state(){
    return{
      theme: '',
      postData: {
        '1985':{
                data: {post_id:'1985', post_img : 'dsdsdsd', creator_nickname: 'User1', post_date: '21 July 2022 21:37', title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.1', description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.'},
                reactions: [ {'name':"12.gif", data: [{'username': 'user1.804838', 'profile_img': ''}]},
                            {'name':"15.gif", data: [{'username': 'user19.804856', 'profile_img': ''}, {'username': 'user122.804737', 'profile_img': ''}, {'username': 'user299.804802', 'profile_img': ''}]},
                            {'name':"19.gif", data: [{'username': 'user32.804871', 'profile_img': ''}, {'username': 'user33.804708', 'profile_img': ''}, {'username': 'user35.804254', 'profile_img': ''}, {'username': 'user24.804824', 'profile_img': ''}, {'username': 'user11.804816', 'profile_img': ''}, {'username': 'user65.804811', 'profile_img': ''}, ]},
                            {'name':"29.gif", data: [{'username': 'user42.804835', 'profile_img': ''}, {'username': 'user44.804844', 'profile_img': ''}]},
                          ],
                tag_list: [1, 2, 4], comments:{}
                },
        '2009':{
                data: {post_id:'2009', post_img : '', creator_nickname: 'User2', post_date: '1 January 2022 22:54', title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.2', description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.'},
                reactions: [ {'name':"9.gif", data: [{'username': 'user12.804833', 'profile_img': ''}, {'username': 'user9.804899', 'profile_img': ''}]}
                           ],
                tag_list: [1, 2, 3], comments:{}
                },
        '1':{
                data: {post_id:'1', post_img : 'dsd',creator_nickname: 'User4', post_date: '1 August 2021 19:10', title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.3', description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.'},
                reactions: [],
                tag_list: [1], comments:{}
            },
      }
      /*  '1':{
                post_id:'1',
                reactions: [["12.gif", 10]],
                post_img : 'dsd',
                data: {creator_nickname: 'User4', post_date: '1 August 2021 19:10', title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.3', description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.', tag_list: [1], comments:{}}
                },
        '27':{
                post_id:'27',
                reactions: [["12.gif", 1],["15.gif",3], [ "19.gif", 9]],
                post_img : 'sd',
                data: {creator_nickname: 'User3', post_date: '3 October 2022 09:18', title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.4', description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.', tag_list: [1, 2, 3, 4, 5], comments:{}}
                },
        '397':{
                post_id:'397',
                reactions: [["9.gif",19]],
                post_img : '',
                data: {creator_nickname: 'User10', post_date: '1 September 2022 06:32', title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.5', description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.', tag_list: [1, 2, 5], comments:{}}
                },
       */
      
     
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
