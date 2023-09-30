



<script setup>

Есть следующий код


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

Оптимизируй код или напиши оптимальный новый код, который реализует систему лайк/дизлайк.
Код должен выполнять функции "поставить лайк", "поставить дизлайк", "сменить лайк на дизлайк или дизлай на лайк".
При этом результат должен быть записан в поле 'user_reaction': {reacted:false, reaction_type:""} объекта state.PostsList.results во Vuex.
В качестве входных данных могут быть использованы данные в своём формате или в следующем формате
data = {
    'post_id': 87, // post_id
    'reaction_type': 'like'/'dislike',
}

</script>