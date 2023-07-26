import JournalService from '@/api/JournalAPI/index'


const user = JSON.parse(localStorage.getItem('user'));
const initialState = user
  ? { status: { loggedIn: true }, user, haveInitialPosts: false, PostsList: [], Reactions: [], Comments: [], Comment: {}}
  : { status: { loggedIn: false }, user: null, haveInitialPosts: false, PostsList: [], Reactions: [], Comments: [], Comment: {} };

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

    getReactions({ commit }, data){
      return JournalService.get_reactions(data.post_id).then(
        reactions_data => {
          commit('gettingReactionsSuccess', reactions_data.data);
          return Promise.resolve(reactions_data.data);
        },
        error => {
          return Promise.reject(error);
        }
      );
    },

    set_reaction({ commit, dispatch}, data){
      //Если пользователь оставлял реакцию
      if(data.user_reaction.reacted){

        //Если выбранная реакция соответствует оставленной
        if(data.reaction_type == data.user_reaction.reaction_type){
          
          commit('removeReaction', {'post_id': data.post_id,'reaction_type': data.reaction_type})

          JournalService.remove_reaction(data.post_id).then(
            response => {return Promise.resolve(response.data);},
            error => {return Promise.reject(error);}
          );
        }
        else{
          commit('changeReaction', {'post_id': data.post_id,'reaction_type': data.reaction_type})

          JournalService.change_reaction({'post_id': data.post_id,'reaction_type': data.reaction_type}).then(
            response => {return Promise.resolve(response.data);},
            error => {return Promise.reject(error);}
          );            
        }
      }

      else{
        commit('setReaction', {'post_id': data.post_id,'reaction_type': data.reaction_type})

        JournalService.add_reaction({'post_id': data.post_id,'reaction_type': data.reaction_type}).then(
          response => {return Promise.resolve(response.data);},
          error => {return Promise.reject(error);}
        );
      }
    },

    getPostsComments({commit}, post_id){
      JournalService.get_posts_comments(post_id).then(
        response => {
          commit('gettingCommentsSuccess', response.data);
          return Promise.resolve(response.data);},
        error => {return Promise.reject(error);}
      )
    },

    getComment({commit}, comment_id){
      JournalService.get_comment(comment_id).then(
        comment_data => {
          commit('gettingCommentSuccess', comment_data.data);
          return Promise.resolve(comment_data.data);},
        error => {return Promise.reject(error);}
      ); 
    },

    deleteComment({ commit }, comment_id) {
     
      if(comment.replies && comment.replies.length > 0){
        JournalService.delete_comment(comment_id).then(
          response => {return Promise.resolve(response.data);},
          error => {return Promise.reject(error);}
        );   
      }
      else{
        JournalService.delete_comment_branch(comment_id).then(
          response => {return Promise.resolve(response.data);},
          error => {return Promise.reject(error);}
        ); 
      }
    },

    createComment({commit}, comment_data){

      JournalService.add_comment(comment_data).then(
        response => {
          commit('', comment_data)
          return Promise.resolve(response.data);},
        error => {return Promise.reject(error);}
      );   
    },

    createCommentReply({commit}, ){},

    editComment({commit}, ){


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

    setPostsList(state, posts_list){
      state.PostsList = posts_list
    },

    updatePostsList(state, post_data){
      state.PostsList.unshift(post_data)
    },

    gettingReactionsSuccess(state, reactions_data){
      state.Reactions = reactions_data;
    },

    setReaction(state, chosen_data){
      const post_obj =  state.PostsList.results.find(post => post.id == chosen_data.post_id)
      switch (chosen_data.reaction_type){
        case 'like':
          post_obj.post_reactions.num_likes += 1
          break
        case 'dislike':
          post_obj.post_reactions.num_dislikes += 1
          break
      }
      post_obj.post_reactions.total_reactions += 1
      
      post_obj.user_reaction = {'reacted': true, 'reaction_type': chosen_data.reaction_type}
    },

    removeReaction(state, chosen_data){
      const post_obj =  state.PostsList.results.find(post => post.id == chosen_data.post_id)
      switch (chosen_data.reaction_type){
        case 'like':
          post_obj.post_reactions.num_likes -= 1
          break
        case 'dislike':
          post_obj.post_reactions.num_dislikes -= 1
          break
      }
      post_obj.post_reactions.total_reactions -= 1
      post_obj.user_reaction = {'reacted': false, 'reaction_type': ''}


    },

    changeReaction(state, chosen_data){
      const post_obj =  state.PostsList.results.find(post => post.id == chosen_data.post_id)
      switch(chosen_data.reaction_type){
        case 'like':
          post_obj.post_reactions.num_likes += 1
          post_obj.post_reactions.num_dislikes -= 1
          break
        case 'dislike':
          post_obj.post_reactions.num_dislikes += 1
          post_obj.post_reactions.num_likes -= 1
          break  
      }
      post_obj.user_reaction.reaction_type = chosen_data.reaction_type
    },

    gettingCommentsSuccess(state, comments_data){
      state.Comments = comments_data;
    },

    gettingCommentSuccess(state, comment_data){
      state.Comment = comment_data;
    },

    deleteComment(state, comment_id) {
      function removeCommentById(comments, commentId) {
        return comments.filter(comment => {
          if (comment.id === commentId) {
            if(comment.replies && comment.replies.length > 0){
              comment.status = 'd'
              comment.text = 'Комментарий удалён'
              return true
            }
            else{           
              return false; // Удалить комментарий с заданным id
            }
            
          }
          if (comment.replies && comment.replies.length > 0) {
            comment.replies = removeCommentById(comment.replies, commentId); // Удалить комментарии из ответов комментария
          }
          return true;
        });
      }

      state.Comments.comments = removeCommentById(state.Comments.comments, comment_id);
    },

    addCommentReply(state, comment_id){

    },

    addComment(state, post_id){
      state.Comments.comments.push(
      )
    },

    editCommentText(state, comment_data){
    }
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
    },

    getReactions(state){
      return state.Reactions.results
    },

    getPostById(state, post_id){
      return state.PostsList.results.filter(post => post.id == 2)
    },

    getComments(state){
      return state.Comments
    },


    
  }

};