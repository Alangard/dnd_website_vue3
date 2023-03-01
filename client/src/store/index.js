
import { createStore } from 'vuex'


export default createStore({
  state(){
    return{
      isMobile: null,
      theme: 'light',
      modals_info: {id: 0, state: false, modal_type: '', action_pressed: false},
      emoticons: {all:
                    [
                      {emoticon_id: "d2_dealwithit_ES", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bd/Emoticon_dealwithit.gif'},
                      {emoticon_id: "d2_evil_NS", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/1/18/Emoticon_devil.gif'},
                      {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif'},
                      {emoticon_id: "d2_smile_QOP", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6e/Emoticon_relieved.gif'},
                      {emoticon_id: "d2_stunned_Rosh", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.gif'},
                      {emoticon_id: "d2_cool_NP", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/e/ec/Emoticon_cool.gif'},
                      {emoticon_id: "d2_happytear_lich", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/d/d9/Emoticon_happytears.gif'},
                      {emoticon_id: "d2_highfive_sniper", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/d/d9/Emoticon_highfive.gif'},
                      {emoticon_id: "d2_rage_axe", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/e/e4/Emoticon_rage.gif'},
                      {emoticon_id: "d2_surprise_mipo", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/d/d9/Emoticon_surprise.gif'},
                      {emoticon_id: "d2_smile_CM", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/f/f2/Emoticon_smile.gif'},
                      {emoticon_id: "d2_thinking_ember", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/f/f5/Emoticon_thinking.gif'}
                    ],
                  most_popular:
                    [
                      {emoticon_id:"d2_cool_NP", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/e/ec/Emoticon_cool.gif'},
                      {emoticon_id:"d2_happytear_lich", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/d/d9/Emoticon_happytears.gif'},
                      {emoticon_id:"d2_highfive_sniper", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/d/d9/Emoticon_highfive.gif'},
                    ]
                },
      user_info: {
                  username: 'Alangard.1', user_profile_img_url: '', user_role:'user',//usert2.804357
                  emoticons:{
                              favorites:[{emoticon_id:'d2_dealwithit_ES', emoticon_url:'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bd/Emoticon_dealwithit.gif'},{emoticon_id:'d2_facepalm_WR', emoticon_url:'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif'}], 
                              recent:[{emoticon_id:'d2_facepalm_WR', emoticon_url:'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif'},{emoticon_id:'d2_stunned_Rosh', emoticon_url:'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.gif'}]
                            }
                  },

      // The order of reactions in short_post_data is determined by backend. Array can saves the order of element
      short_post_data: {
        '1985':{
                data: {
                        post_id:'1985', post_date: '2022-11-11T17:38:00.379Z', 
                        creator_nickname: 'User1.804838', creator_profile_img_url:'https://cs9.pikabu.ru/post_img/big/2019/10/30/10/1572455476123442192.jpg', 
                        title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.1', 
                        post_img_url: 'https://thumbs.dreamstime.com/b/blog-information-website-concept-workplace-background-text-view-above-127465079.jpg', 
                        description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.'
                      },
                reactions: {"top3_reactions__list":[ 
                                                      {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif'},
                                                      {emoticon_id: "d2_smile_QOP", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6e/Emoticon_relieved.gif'},
                                                      {emoticon_id: "d2_evil_NS", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/1/18/Emoticon_devil.gif'},
                                                    ], 
                            "reacted": true
                          },
                tags: {"tags_list": [1, 2, 4]}, 
                comments:{"counter": 290, "commented": false}
                },
        '2009':{
                data: {
                        post_id:'2009', post_date: '2021-11-11T17:38:00', 
                        creator_nickname: 'User2.804839', creator_profile_img_url:'', 
                        title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.2',
                        post_img_url : '', 
                        description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.'
                      },
                reactions: {"top3_reactions__list":[
                                                      {emoticon_id: "d2_stunned_Rosh", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.gif'},
                                                    ], 
                            "reacted": false
                          },
                tags: {"tags_list": [1, 2, 3]},
                comments:{"counter": 20, "commented": true}
                },
        '1':{
                data: {
                        post_id:'1', post_date: '2022-11-11T17:48:00.379Z', 
                        creator_nickname: 'User4.804841', creator_profile_img_url:'https://avatars.mds.yandex.net/i?id=850f39a77c8c28ab157103493cf178df-4079986-images-thumbs&n=13',
                        post_img_url : '',
                        title: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis velit quas quasi perspiciatis.3',   
                        description:'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Accusantium asperiores repudiandae obcaecati perspiciatis, voluptatem hic, in rerum accusamus maiores molestias inventore nisi ratione ea! Iste aperiam sit itaque consequuntur nemo.'
                      },
                reactions: {"top3_reactions__list":[], "reacted": false},
                tags: {"tags_list": []}, 
                comments:{"counter": 0, "commented": false}
            },
      },


      postData: {
      },

      // The order of reactions is determined by backend. Array can saves the order of element
      reactions:{
        '1985':
          [
            {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif', 
              users_data: [
                {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif',username: 'user35.804254', user_profile_img_url: '', reaction_date: '2022-11-11T16:35:00.379Z'},
                {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif',username: 'user11.804816', user_profile_img_url: '', reaction_date: '1995-12-17T23:12:00.379Z'}, 
                {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif',username: 'user65.804811', user_profile_img_url: '', reaction_date: '1995-12-17T21:25:00.379Z'},
                {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif',username: 'user24.804824', user_profile_img_url: '', reaction_date: '1995-12-17T21:24:00.379Z'}, 
                {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif',username: 'user32.804871', user_profile_img_url: '', reaction_date: '1995-12-17T09:24:00.379Z'}, 
                {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif',username: 'user33.804708', user_profile_img_url: '', reaction_date: '1995-12-17T07:24:00.379Z'},
              ]
            },
            
            {emoticon_id: "d2_evil_NS", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/1/18/Emoticon_devil.gif', 
              users_data: [
                {emoticon_id: "d2_evil_NS", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/1/18/Emoticon_devil.gif',username: 'user19.804856', user_profile_img_url: '', reaction_date: '1997-12-17T03:24:00.379Z'},
                {emoticon_id: "d2_evil_NS", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/1/18/Emoticon_devil.gif',username: 'user122.804737', user_profile_img_url: '', reaction_date: '1995-12-21T03:24:00.379Z'}, 
                {emoticon_id: "d2_evil_NS", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/1/18/Emoticon_devil.gif',username: 'user299.804802', user_profile_img_url: '', reaction_date: '1995-12-17T03:24:00.379Z'},
              ]
            },
            
            {emoticon_id: "d2_smile_QOP", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6e/Emoticon_relieved.gif',
              users_data: [
                {emoticon_id: "d2_smile_QOP", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6e/Emoticon_relieved.gif',username: 'user44.804844', user_profile_img_url: '', reaction_date: '2009-12-18T03:24:00.379Z'},
                {emoticon_id: "d2_smile_QOP", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6e/Emoticon_relieved.gif',username: 'user42.804835', user_profile_img_url: '', reaction_date: '2009-12-17T03:24:00.379Z'}
              ]
            },

            {emoticon_id: "d2_stunned_Rosh", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.gif',
              users_data: [
                {emoticon_id: "d2_stunned_Rosh", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.gif',username: 'usert2.804357', user_profile_img_url: '', reaction_date: '2023-01-24T17:13:57.072Z'},
                {emoticon_id: "d2_stunned_Rosh", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.gif',username: 'user12.804833', user_profile_img_url: '', reaction_date: '2009-12-17T03:25:00.379Z'}
              ]
            },

            {emoticon_id: "d2_dealwithit_ES", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bd/Emoticon_dealwithit.gif', 
              users_data: [
                {emoticon_id: "d2_dealwithit_ES", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bd/Emoticon_dealwithit.gif', username: 'user1.804838', user_profile_img_url: '', reaction_date: '1995-12-17T03:24:00.379Z'}
              ]
            }
          ],

        '2009': 
          [
            {emoticon_id: "d2_stunned_Rosh", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.giff', 
              users_data: [              
                {emoticon_id: "d2_stunned_Rosh", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.giff', username: 'user9.804899', user_profile_img_url: '', reaction_date: '2002-12-17T03:27:00.379Z'},
                {emoticon_id: "d2_stunned_Rosh", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.giff', username: 'user12.804833', user_profile_img_url: '', reaction_date: '2002-12-17T03:24:00.379Z'}, 
              ]
            }
          ],
        
        '1': [],
      },


      // reactions: {
      //   '1985':[
          // {emoticon_id: "d2_stunned_Rosh", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.gif', username: 'usert2.804357', profile_img_url: '', date: '2022-12-06T16:35:39.379Z'},
          // {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif', username: 'user35.804254', user_profile_img_url: '', date: '2022-11-11T16:35:00.379Z'},
          // {emoticon_id: "d2_smile_QOP", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6e/Emoticon_relieved.gif', username: 'user44.804844', user_profile_img_url: '', date: '2009-12-18T03:24:00.379Z'},
          // {emoticon_id: "d2_smile_QOP", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6e/Emoticon_relieved.gif', username: 'user42.804835', user_profile_img_url: '', date: '2009-12-17T03:24:00.379Z'},
          // {emoticon_id: "d2_stunned_Rosh", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.gif', username: 'user12.804833', profile_img_url: '', date: '2009-12-17T03:25:00.379Z'},
          // {emoticon_id: "d2_evil_NS", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/1/18/Emoticon_devil.gif', username: 'user19.804856', user_profile_img_url: '', date: '1997-12-17T03:24:00.379Z'},
          // {emoticon_id: "d2_evil_NS", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/1/18/Emoticon_devil.gif', username: 'user122.804737', user_profile_img_url: '', date: '1995-12-21T03:24:00.379Z'}, 
          // {emoticon_id: "d2_evil_NS", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/1/18/Emoticon_devil.gif', username: 'user299.804802', user_profile_img_url: '', date: '1995-12-17T03:24:00.379Z'},
          // {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif', username: 'user11.804816', user_profile_img_url: '', date: '1995-12-17T23:12:00.379Z'}, 
          // {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif', username: 'user65.804811', user_profile_img_url: '', date: '1995-12-17T21:25:00.379Z'},
          // {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif', username: 'user24.804824', user_profile_img_url: '', date: '1995-12-17T21:24:00.379Z'}, 
          // {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif', username: 'user32.804871', user_profile_img_url: '', date: '1995-12-17T09:24:00.379Z'}, 
          // {emoticon_id: "d2_facepalm_WR", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Emoticon_facepalm.gif', username: 'user33.804708', user_profile_img_url: '', date: '1995-12-17T07:24:00.379Z'},
          // {emoticon_id: "d2_dealwithit_ES", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bd/Emoticon_dealwithit.gif', username: 'user1.804838', user_profile_img_url: '', reaction_date: '1995-12-17T03:24:00.379Z'}
      //   ],

      //   '2009':[
      //     {emoticon_id: "d2_stunned_Rosh", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.giff', username: 'user9.804899', user_profile_img_url: '', date: '2002-12-17T03:27:00.379Z'},
      //     {emoticon_id: "d2_stunned_Rosh", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.giff', username: 'user12.804833', user_profile_img_url: '', date: '2002-12-17T03:24:00.379Z'}, 
      //   ],

      //   '1': [],
      // }

    }




      
      
     
    


    
  },
  getters: {

    getModalActionStatus(state){
      return state.modals_info.action_pressed;
    },

    //returns true/false
    getIsMobileState (state) {
        return state.isMobile;
    },

    //returns string 'light'/'dark' 
    getTheme (state){
        return state.theme;
    },

    // new getters
    getShrotPostData(state){
      return state.short_post_data;
    },


    //////////////////////////////////////////////////////////

    getIndexOfReactionByID: (state) => (input_obj) =>{
      const {reactions_obj, emoticon_id} = input_obj;
      return reactions_obj.findIndex(element => element.emoticon_id == emoticon_id);
    },

    //////////////////////////////////////////////////////////////////////////////






    getPostData (state){
      return state.postData;
    },

    getAllUserInfo(state){//
      return state.user_info;
    },

    getUserInfo(state){//
      return {'username': state.user_info.username, 'user_profile_img_url': state.user_info.user_profile_img_url, 'user_role': state.user_info.user_role}
    },

    getUserEmoticonFavorites(state){ //getUserEmoticon
      return state.user_info.emoticons.favorites;
    },

    getUserEmoticonRecent(state){//
      return state.user_info.emoticons.recent;
    },

    getAllEmoticons(state){//
      return state.emoticons.all;
    },

    getMostPopularEmoticons(state){//
      return state.emoticons.most_popular;
    },

    // Returns the index of the emoticon in the Favorites section by reaction's id. If there is no emoticon, the getter will return -1
    getIndexEmotInFavorites: (state) => (emoticon_id) =>{
      for(var [reaction_index, emoticon] of state.user_info.emoticons.favorites.entries()){
        if(emoticon.emoticon_id == emoticon_id){
          return reaction_index;
        }
      }
      return -1;      
    },

    getIndexEmotInRecent: (state) => (emoticon_id) =>{
      for(var [reaction_index, emoticon] of state.user_info.emoticons.recent.entries()){
        if(emoticon.emoticon_id == emoticon_id){
          return reaction_index;
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
          let data = new Map(Object.entries(reaction.data));
          if(data.get(user_info.username) != undefined){
            return reaction;
          }
        }
        return -1;
      }
      catch(err){console.log(err);}
    },

    //Method returning preformatted time now in datetime format
    getDatetimeNow(state){
      return new Date().toISOString();
    },

    //Method replacing the first character with an uppercase character
    capitalizeFirstLetter: (state) => (string) => {
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
  },

  mutations: {
    /////////////////////////////////////////////////////////////
    
    ////////////////////////////////////////////////////////////


    //Change the state of page size (true - mobile, false - desktop)
    changeIsMobileFlag(state, flag_pos) {
        state.isMobile = flag_pos;
    },

    //Change the website theme and add a value 'theme' to the local storage
    changeTheme(state, chose_theme){
      if(chose_theme == 'dark' || chose_theme == 'light'){
        state.theme = chose_theme;
        localStorage.theme = chose_theme;
      }
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
  },

  actions: {

    changeReactionStatus(context, payload){
      debugger
      const {post_id, pressed_emoticon_id, pressed_emoticon_url} = payload;
      let reaction_obj = null;

      for(const reaction of context.state.reactions[post_id]){
        let index_of_user = 0;
        for(const user of reaction.users_data){

          if(user.username == context.getters.getAllUserInfo.username && reaction.emoticon_id == pressed_emoticon_id){
            reaction.users_data.splice(index_of_user, 1);
            return true;
          }

          else if(user.username == context.getters.getAllUserInfo.username){
            reaction.users_data.splice(index_of_user, 1);
          }

          else if(reaction.emoticon_id == pressed_emoticon_id){
            reaction_obj = {
              'reaction_proxy': reaction, 
              'reaction_data':{
                              'emoticon_id': reaction.emoticon_id, 
                              'emoticon_url': reaction.emoticon_url,
                              'username': context.getters.getUserInfo.username, 
                              'user_profile_img_url': context.getters.getUserInfo.user_profile_img_url, 
                              'reaction_date': context.getters.getDatetimeNow
                            }
            };
          }


          index_of_user++;
        }
      }

      //
      if(reaction_obj !== null){
        reaction_obj.reaction_proxy.users_data.unshift(reaction_obj.reaction_data);

        // Add emoticon to "Recent" after it has been selected for reaction
        context.dispatch('addReactionToRecent', 
          {'emoticon_id': pressed_emoticon_id, 'emoticon_url': pressed_emoticon_url}
        );
      }

      else{
        //For an emoticon that is not yet in the database, create a new structure using the template
        const NewReactionData = {'emoticon_id': pressed_emoticon_id, 'emoticon_url': pressed_emoticon_url, 
          'users_data':[
            {
              'emoticon_id': pressed_emoticon_id, 
              'emoticon_url': pressed_emoticon_url,
              'username': context.getters.getUserInfo.username, 
              'user_profile_img_url': context.getters.getUserInfo.user_profile_img_url, 
              'reaction_date': context.getters.getDatetimeNow
            }
          ]
        };

        context.state.reactions[post_id].push(NewReactionData)

        context.dispatch('addReactionToRecent', 
          {'emoticon_id': pressed_emoticon_id, 'emoticon_url': pressed_emoticon_url}
        );
      }
    },
    

    changeStatusReactionInFavorites(context, payload){
      debugger
      const {emoticon_id, emoticon_url} = payload;
      const IndexEmotInFavorites = context.getters.getIndexEmotInFavorites(emoticon_id);


      try{
        if(IndexEmotInFavorites == -1){ 
            context.state.user_info.emoticons.favorites.push({'emoticon_id': emoticon_id, 'emoticon_url': emoticon_url});
            //send data to server
        }
        else{
            context.state.user_info.emoticons.favorites.splice(IndexEmotInFavorites, 1);
            //send data to server
        }
      }
      catch(err){console.log(err)}
    },

    addReactionToRecent(context, payload){
      // исправить баг с добавлением в избранное и появлением дипликатов в recent
      debugger
      const {emoticon_id, emoticon_url} = payload;
      const IndexEmotInRecent = context.getters.getIndexEmotInRecent(emoticon_id);
      const RecentEmoticonsList = context.getters.getUserEmoticonRecent;

      try{
        if(IndexEmotInRecent == -1){
          if(RecentEmoticonsList.length < 5){
            RecentEmoticonsList.push({'emoticon_id': emoticon_id, 'emoticon_url':emoticon_url});
          }
          else{
            RecentEmoticonsList.splice(-1, 1, {'emoticon_id': emoticon_id, 'emoticon_url':emoticon_url});
          }
        }
      }
      catch(err){console.log(err)}  
    }
  },

  modules: {
  }
})
