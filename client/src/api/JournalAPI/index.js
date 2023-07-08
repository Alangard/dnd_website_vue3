import axios from 'axios'
import authHeader from '../AuthAPI/auth-header';

const BASE_URL = '/api/v1/';


class JournalService {
    get_posts(url){
        return axios.get(BASE_URL + url, { headers: authHeader() })
    }

    get_reactions(post_id){
        return axios.get(BASE_URL + `post/${post_id}/reactions/`)
    }

    userReactionOnPost(data){
        return axios.get(BASE_URL + `post/${data.post_id}/reactions/?username=${data.username}`)
    }

    get_reaction(reaction_id){
        return axios.get(BASE_URL + `post_reaction/${reaction_id}/`)
    }
    
    remove_reaction(post_id){
        return axios.delete(BASE_URL + `post/${post_id}/remove_reaction/`, { headers: authHeader()})
    }
    
    add_reaction(data){
        return axios.post(BASE_URL + `post/${data.post_id}/add_reaction/`, 
            {'reaction_type': data.reaction_type}, 
            {headers: authHeader()}
        )
    }

    change_reaction(data){
        return axios.patch(BASE_URL + `post/${data.post_id}/update_reaction/`, 
            {'reaction_type': data.reaction_type},
            {headers: authHeader()}
        )
    }

    get_posts_comments(post_id){
        return axios.get(BASE_URL + `post/${post_id}/comments/`,)
    }

    get_comment(comment_id){
        return axios.get(BASE_URL + `comment/${comment_id}/`,)
    }


    add_comment(data){
        return axios.post(BASE_URL + `post/${data.post_id}/comment/create/`,
            {'text': data.text},
            {headers: authHeader()}
        )
    }

    add_comment_reply(data){
        return axios.post(BASE_URL + `comment/${data.comment_id}/create/`,
            {'text': data.text},
            {headers: authHeader()}
        )
    }

    delete_comment(comment_id){
        return axios.delete(BASE_URL + `comment/${comment_id}/delete/`,
            {headers: authHeader()}
        )
    }

    delete_comment_branch(comment_id){
        return axios.delete(BASE_URL + `comment/${comment_id}/delete_branch/`,
            {headers: authHeader()}
        )
    }

    edit_comment(data){
        return axios.put(BASE_URL + `comment/${data.comment_id}/update/`,
            data.edit_data,
            {headers: authHeader()}
        )
    }

    partial_edit_comment(data){
        return axios.patch(BASE_URL + `comment/${data.comment_id}/update/`,
            data.edit_data,
            {headers: authHeader()}
        )
    }





}

export default new JournalService();