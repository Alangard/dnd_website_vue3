import { createStore } from 'vuex'


export default createStore({
  state(){
    return{
      isMobile: null,
      modalIsOpen: false,
      theme: 'light',
      user_info: {username: 'usert2.804357', profile_img_url: '', date: '2022-11-21T09:24:00',
                  emoticons:{favorites:[{reaction_id:'d2_dealwithit_ES', img_url:'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bd/Emoticon_dealwithit.gif'},{reaction_id:'d2_facepalm_WR', img_url:'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif'}], 
                             recent:[{reaction_id:'d2_facepalm_WR', img_url:'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif'},{reaction_id:'d2_stunned_Rosh', img_url:'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.gif'}]
                            }
                  },
      postData: {
        '1985':{
                data: {post_id:'1985', img_url: 'https://thumbs.dreamstime.com/b/blog-information-website-concept-workplace-background-text-view-above-127465079.jpg', creator_nickname: 'User1.804838', profile_img_url:'https://cs9.pikabu.ru/post_img/big/2019/10/30/10/1572455476123442192.jpg', post_date: '2022-11-11T17:38:00', title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.1', description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.'},
                reactions: [ {reaction_id:"d2_dealwithit_ES", img_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bd/Emoticon_dealwithit.gif', data: [{username: 'user1.804838', profile_img_url: '', date: '1995-12-17T03:24:00'}]},
                            {reaction_id:"d2_evil_NS", img_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/1/18/Emoticon_devil.gif', data: [{username: 'user19.804856', profile_img_url: '', date: '1997-12-17T03:24:00'}, {username: 'user122.804737', profile_img_url: '', date: '1995-12-21T03:24:00'}, {username: 'user299.804802', profile_img_url: '', date: '1995-12-17T03:24:00'},]},
                            {reaction_id:"d2_facepalm_WR", img_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif', data: [{username: 'user32.804871', profile_img_url: '', date: '1995-12-17T09:24:00'}, {username: 'user33.804708', profile_img_url: '', date: '1995-12-17T07:24:00'}, {username: 'user35.804254', profile_img_url: '', date: '2022-11-11T16:35:00'}, {username: 'user24.804824', profile_img_url: '', date: '1995-12-17T21:24:00'}, {username: 'user11.804816', profile_img_url: '', date: '1995-12-17T23:12:00'}, {username: 'user65.804811', profile_img_url: '', date: '1995-12-17T21:25:00'}]},
                            {reaction_id:"d2_smile_QOP", img_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6e/Emoticon_relieved.gif', data: [{username: 'user42.804835', profile_img_url: '', date: '2009-12-17T03:24:00'},{username: 'user44.804844', profile_img_url: '', date: '2009-12-18T03:24:00'}]},
                            {reaction_id:"d2_stunned_Rosh", img_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.gif', data: [{username: 'user12.804833', profile_img_url: '', date: '2009-12-17T03:25:00'},{username: 'usert2.804357', profile_img_url: '', date: '2022-11-21T09:24:00'}]}
                          ],
                tag_list: [1, 2, 4], comments:{'counter': 290, data:{}}
                },
        '2009':{
                data: {post_id:'2009', img_url : '', creator_nickname: 'User2.804839', profile_img_url:'', post_date: '2021-11-11T17:38:00', title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.2', description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.'},
                reactions: [ {reaction_id:"d2_stunned_Rosh", img_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.gif', data: [{username: 'user12.804833', profile_img_url: '', date: '2002-12-17T03:24:00'}, {username: 'user9.804899', profile_img_url: '', date: '2002-12-17T03:27:00'}]}
                           ],
                tag_list: [1, 2, 3], comments:{'counter': 11, data:{}}
                },
        '1':{
                data: {post_id:'1', img_url : '',creator_nickname: 'User4.804841', profile_img_url:'https://avatars.mds.yandex.net/i?id=850f39a77c8c28ab157103493cf178df-4079986-images-thumbs&n=13', post_date: '2022-11-11T17:48:00', title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.3', description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.'},
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

    getModalState(state){
      console.log(state.modalIsOpen)
      return state.modalIsOpen;
      
    },

    getTheme (state){
        return state.theme;
    },

    getPostData (state){
      return state.postData;
    },

    getReactionByPostId: (state) => (post_id) =>{
      return state.reactions[post_id];
    },

    getUserInfo(state){
      return state.user_info;
    },

    getUserEmoticon(state){
      return state.user_info.emoticons;
    },


    getIndexEmotInFavorites: (state) => (emote_id) =>{
      for(var [index, reaction] of state.user_info.emoticons.favorites.entries()){
        if(reaction.reaction_id == emote_id){
          console.log(index);
          return index;
        }
      }
      return -1;      
    },

    findAllUserReactionsByPostId: (state) => (payload) =>{
      try{
        var reactionsList = [];
        var chosenReaction = [];
        var {post_id, reaction_id, user_info} = payload;
        var reactions_el = state.postData[post_id].reactions;

        for(var reaction of reactions_el){
          for(var [index, user_data] of reaction.data.entries()){
            if(user_data.username == user_info.username){
              if(reaction.reaction_id == reaction_id){
                chosenReaction.push(...[reaction.data, index]);
                return [chosenReaction, reactionsList];
              }
              else{
                reactionsList.push([reaction.data, index]);
                return [chosenReaction, reactionsList];
              }
            }
          }
        }
        return [chosenReaction, reactionsList];
      }

      catch(err){
        console.log(err);
      }
      
    },

    //Getter to help determine if the user has left a reaction and its index in reaction.data by post_id
    getDataOfUserReaction: (state) => (payload) => {
      try{
        const [post_id, user_info] = payload;
        const reaction_data__by_id = state.postData[post_id].reactions;

        for(var reaction of reaction_data__by_id){
          for(var[index, user_data] of reaction.data.entries()){
              if(user_data.username == user_info.username){
                return [reaction, index]
              }
          }
        }
        return [undefined, undefined]
      }
      catch(err){console.log(err);}
    }
  },

  mutations: {
    changeIsMobileFlag  (state, flag_pos) {
        state.isMobile = flag_pos;
    },

    changeModalState (state){
      state.modalIsOpen = !state.modalIsOpen;
      console.log(state.modalIsOpen);
    },

    changeTheme (state, chose_theme){
      if(chose_theme == 'dark' || chose_theme == 'light'){
        state.theme = chose_theme;
      }
      console.log(state.theme);
    },

    printData (state, post_id){
      console.log(state.postData[post_id])
    },

    changeStatus(state){
      state.is_favorite = !state.is_favorite;
      console.log(state.is_favorite)
    },


// Reactions mutations 
    addNewReaction(state, payload){
      try{
        const [data, user_info] = payload;
        data.push(user_info);
        //console.log(data);
      }
      catch(err){console.log(err)}
    },

    removeReaction(state, payload){
      try{
        const [data, index] = payload;
        data.splice(index, 1);
        //console.log(data);
      }
      catch(err){console.log(err);}
    },

    addReactionInFavorites(state, emote_data){
      try{
        const [id, url] = emote_data;
        state.user_info.emoticons.favorites.push({'id': id, 'url': url});
        //console.log(state.user_info.emoticons.favorites);
      }
      catch(err){console.log(err);}
    },

    removeReactionFromFavorites(state, emot_index){
      try{
        state.user_info.emoticons.favorites.splice(emot_index, 1);
        //console.log(data);
      }
      catch(err){console.log(err);}
    }
  },

  actions: {
    changeReactionStatus(context, payload){
      var [reaction_dict, reaction_index__of_reaction_data, user_info, post_id, chosen_reaction_id] = payload;

      //Checking whether the user has left this reaction to the post before
      if(reaction_index__of_reaction_data != undefined){

        if(reaction_dict.reaction_id == chosen_reaction_id){
          context.commit('removeReaction', [reaction_dict.data, reaction_index__of_reaction_data]);
          
        }
        else{
          const data = context.state.postData[post_id].reactions.find(reaction => reaction.reaction_id == chosen_reaction_id).data;
          context.commit('removeReaction', [reaction_dict.data, reaction_index__of_reaction_data]);
          context.commit('addNewReaction', [data, user_info]);
        }
      }
      else{
        const data = context.state.postData[post_id].reactions.find(reaction => reaction.reaction_id == chosen_reaction_id).data;
        context.commit('addNewReaction', [data, user_info]);
      }
    },

    changeStatusReactionInFavorites(context, emote_data){
      var [reaction_id, reaction_url] = emote_data;

      const emotInFavorites = context.getters.getIndexEmotInFavorites(reaction_id);
      if(emotInFavorites == -1){
        context.commit('addReactionInFavorites', [reaction_id, reaction_url]);
      }
      else{
        context.commit('removeReactionFromFavorites', emotInFavorites)
      }

    }
  },

  modules: {
  }
})
