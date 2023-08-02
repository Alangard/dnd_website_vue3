import axios from 'axios'
import interceptorsInstance, {authHeader} from '@/api/main'

const BASE_URL = axios.defaults.baseURL;


class JournalService {

    async get_posts(url){
        return await interceptorsInstance.get(url, { headers: authHeader() })
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
    
    async remove_reaction(post_id){
        return await interceptorsInstance.delete(`post/${post_id}/remove_reaction/`, { headers: authHeader()})
    }
    
    async add_reaction(data){
        return await interceptorsInstance.post(`post/${data.post_id}/add_reaction/`, 
            {'reaction_type': data.reaction_type}, 
            {headers: authHeader()}
        )
    }

    async change_reaction(data){
        return await interceptorsInstance.patch(`post/${data.post_id}/update_reaction/`, 
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

    async add_comment(data){
        return await interceptorsInstance.post(`post/${data.post_id}/comment/create/`,
            {'text': data.text},
            {headers: authHeader()}
        )
    }

    async add_comment_reply(data){
        return await interceptorsInstance.post(`comment/${data.comment_id}/create/`,
            {'text': data.text},
            {headers: authHeader()}
        )
    }

    async delete_comment(comment_id){
        console.log('delete')
        return await interceptorsInstance.delete(`comment/${comment_id}/delete/`,
            {headers: authHeader()}
        )
    }

    async delete_comment_branch(comment_id){
        return await interceptorsInstance.delete(`comment/${comment_id}/delete_branch/`,
            {headers: authHeader()}
        )
    }

    async edit_comment(data){
        return await interceptorsInstance.put(`comment/${data.comment_id}/update/`,
            data.edit_data,
            {headers: authHeader()}
        )
    }

    async partial_edit_comment(data){
        return await interceptorsInstance.patch(`comment/${data.comment_id}/update/`,
            data.edit_data,
            {headers: authHeader()}
        )
    }





}

export default new JournalService();