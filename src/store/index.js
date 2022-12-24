import { createStore } from 'vuex'


export default createStore({
  state(){
    return{
      isMobile: null,
      theme: 'light',
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
                  username: 'usert2.804357', user_profile_img_url: '',
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
                {username: 'user35.804254', user_profile_img_url: '', date: '2022-11-11T16:35:00.379Z'},
                {username: 'user11.804816', user_profile_img_url: '', date: '1995-12-17T23:12:00.379Z'}, 
                {username: 'user65.804811', user_profile_img_url: '', date: '1995-12-17T21:25:00.379Z'},
                {username: 'user24.804824', user_profile_img_url: '', date: '1995-12-17T21:24:00.379Z'}, 
                {username: 'user32.804871', user_profile_img_url: '', date: '1995-12-17T09:24:00.379Z'}, 
                {username: 'user33.804708', user_profile_img_url: '', date: '1995-12-17T07:24:00.379Z'},
              ]
            },
            
            {emoticon_id: "d2_evil_NS", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/1/18/Emoticon_devil.gif', 
              users_data: [
                {username: 'user19.804856', user_profile_img_url: '', date: '1997-12-17T03:24:00.379Z'},
                {username: 'user122.804737', user_profile_img_url: '', date: '1995-12-21T03:24:00.379Z'}, 
                {username: 'user299.804802', user_profile_img_url: '', date: '1995-12-17T03:24:00.379Z'},
              ]
            },
            
            {emoticon_id: "d2_smile_QOP", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6e/Emoticon_relieved.gif',
              users_data: [
                {username: 'user44.804844', user_profile_img_url: '', date: '2009-12-18T03:24:00.379Z'},
                {username: 'user42.804835', user_profile_img_url: '', date: '2009-12-17T03:24:00.379Z'}
              ]
            },

            {emoticon_id: "d2_stunned_Rosh", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.gif',
              users_data: [
                {username: 'usert2.804357', profile_img_url: '', date: '2022-12-06T16:35:39.379Z'},
                {username: 'user12.804833', profile_img_url: '', date: '2009-12-17T03:25:00.379Z'}
              ]
            },

            {emoticon_id: "d2_dealwithit_ES", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bd/Emoticon_dealwithit.gif', 
              users_data: [
                {username: 'user1.804838', user_profile_img_url: '', reaction_date: '1995-12-17T03:24:00.379Z'}
              ]
            }
          ],

        '2009': 
          [
            {emoticon_id: "d2_stunned_Rosh", emoticon_url: 'https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Dotakin_roshan_stars.giff', 
              users_data: [              
                {username: 'user9.804899', user_profile_img_url: '', date: '2002-12-17T03:27:00.379Z'},
                {username: 'user12.804833', user_profile_img_url: '', date: '2002-12-17T03:24:00.379Z'}, 
              ]
            }
          ],
        
        '1': [],
      }

    }




      
      
     
    


    
  },
  getters: {

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








    getPostData (state){
      return state.postData;
    },

    getAllUserInfo(state){//
      return state.user_info;
    },

    getUserInfo(state){//
      return {'username': state.user_info.username, 'profile_img_url': state.user_info.profile_img_url}
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
    getIndexEmotInFavorites: (state) => (reaction_id) =>{
      for(var [reaction_index, reaction] of state.user_info.emoticons.favorites.entries()){
        if(reaction.reaction_id == reaction_id){
          return reaction_index;
        }
      }
      return -1;      
    },

    getIndexEmotInRecent: (state) => (reaction_id) =>{
      for(var [reaction_index, reaction] of state.user_info.emoticons.recent.entries()){
        if(reaction.reaction_id == reaction_id){
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

    //A method describing verbally the time from a completed event
    dateTimeFormat: (state) => (datetime_string) => {
        const datetime = new Date(datetime_string);
        const now_datetime = new Date();
        const diff_in_seconds = Math.floor((now_datetime - datetime) / 1000);

        if(diff_in_seconds >= 3600){
            if(Math.floor(diff_in_seconds / 3600) == 1){
                return `more than ${Math.floor(diff_in_seconds / 3600)} hour ago`;
            }

            else if(Math.floor(diff_in_seconds / 3600) == 2 || Math.floor(diff_in_seconds / 3600) == 3){
                return `more than ${Math.floor(diff_in_seconds / 3600)} hours ago`;
            }

            else{
                //getMonth returns an integer number, between 0 and 11
                const [month, day, year] = [datetime.getMonth() + 1, datetime.getDate(), datetime.getFullYear()];
                const [hour, minutes] = [datetime.getHours(), datetime.getMinutes()];
                return `${day}/${month}/${year} at ${hour}:${minutes}`;
            }
        }

        else if (diff_in_seconds < 3600 && diff_in_seconds >= 60){
            if(Math.floor(diff_in_seconds / 60) == 1){
                return `more than ${Math.floor(diff_in_seconds/60)} minute ago`;
            }

            else if((Math.floor(diff_in_seconds / 60) == 5)){
                return `more than ${Math.floor(diff_in_seconds/60)} minutes ago`;
            }

            else if(Math.floor(diff_in_seconds / 60) >= 5){
                return `more than ${Math.floor(diff_in_seconds/60)} minutes ago`;
            }
        }

        else {
            return 'now';
        }
    }

  },

  mutations: {
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

    addReactionInFavorites(state, emote_data){
      try{
        const [id, url] = emote_data;
        state.user_info.emoticons.favorites.push({'reaction_id': id, 'img_url': url});
        //console.log(state.user_info.emoticons.favorites);
      }
      catch(err){console.log(err);}
    },

    removeReactionFromFavorites(state, reaction_index){
      try{
        state.user_info.emoticons.favorites.splice(reaction_index, 1);
        //console.log(data);
      }
      catch(err){console.log(err);}
    },
  },

  actions: {

    changeReactionStatus(context, payload){
      const [reaction_dict, reaction_index__of_reaction_data, post_id, chosen_reaction_data] = payload;
      const datetime = context.getters.getDatetimeNow;
      const user_info_obj = {'username': context.state.user_info.username, 'profile_img_url': context.state.user_info.profile_img_url, 'date': datetime};

      //Checking whether the user has left this reaction to the post before
      if(reaction_index__of_reaction_data != undefined){

        if(reaction_dict.reaction_id == chosen_reaction_data.reaction_id){
          context.commit('removeReaction', [reaction_dict.data, reaction_index__of_reaction_data]);
          
        }
        else{
          const data = context.state.postData[post_id].reactions.find(reaction => reaction.reaction_id == chosen_reaction_data.reaction_id)
          context.commit('removeReaction', [reaction_dict.data, reaction_index__of_reaction_data]);

          //Checking whether a reaction to the post has been left by someone else before
          if(data != undefined){
            context.commit('addNewReaction', [data.data, user_info_obj]);
          }
          else{
            const data = context.state.postData[post_id].reactions.push({"reaction_id":chosen_reaction_data.reaction_id, "img_url": chosen_reaction_data.img_url, "data":[user_info_obj]});
          }
          
        }
      }
      else{
        const data = context.state.postData[post_id].reactions.find(reaction => reaction.reaction_id == chosen_reaction_data.reaction_id).data;
        context.commit('addNewReaction', [data, user_info_obj]);
      }
    },

    changeStatusReactionInFavorites(context, reaction_data){
      var [reaction_id, reaction_url] = reaction_data;
      const emotInFavorites = context.getters.getIndexEmotInFavorites(reaction_id);
      
      if(emotInFavorites == -1){
        context.commit('addReactionInFavorites', [reaction_id, reaction_url]);
      }
      else{
        context.commit('removeReactionFromFavorites', emotInFavorites)
      }
    },

    addReactionToRecent(context, reaction_data){
      // исправить баг с добавлением в избранное и появлением дипликатов в recent
      try{
        const [reaction_id, reaction_url] = reaction_data;
        const reaction_index = context.getters.getIndexEmotInRecent(reaction_id);
        const recent_emots_list = context.getters.getUserInfo.emoticons.recent;

        if(reaction_index == -1){
          if(recent_emots_list.length < 5){
            recent_emots_list.push({'reaction_id': reaction_id, 'img_url':reaction_url});
          }
          else{
            recent_emots_list.splice(-1, 1, {'reaction_id': reaction_id, 'img_url':reaction_url});
          }
        }
      }
      catch(err){console.log(err);}


    }
  },

  modules: {
  }
})
