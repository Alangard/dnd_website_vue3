<template>

<div class="modal fade" id="ReactorsModal">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
            <div class="modal-header">
                Reacted users
                <svg data-bs-dismiss="modal" aria-label="Close" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </div>

            <div class="modal-body">
                <img class="profile_img" data-bs-dismiss="modal" src="../../assets/test_blog_photo.png" alt="" 
                    v-for="reactor in this.reactors_list" :key='reactor'
                    :title=reactor.username.split(/[.]/)[0]
                    @click="$router.push({ name: 'user', params: {id: reactor.username } })"
                >
            </div>

        </div>
    </div>
</div>

</template>


<script>
export default {
    props:['reactors_list'],
    data(){
        return{}
    }   
}
</script>

<style lang="scss" scoped>

.modal-content{
    background-color:var(--bg_color);
}

.modal-header{
    border-bottom:  2px solid var(--text_color_secondary);
    color: var(--text_color_primary);

    svg{
        cursor: pointer;
        stroke: var(--text_color_primary);

        &:hover{
            stroke: var(--bg_button_active_color);
        }
    }
}

.modal-body{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    padding: 0 4px;
    
    .profile_img{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin: 20px 15px;
        background-color: #ffff;
        cursor: pointer;

        &:hover{
            transform: scale(1.4);
            filter: drop-shadow(0 0 5px var(--bg_button_active_color));
        }
    }
}


</style>