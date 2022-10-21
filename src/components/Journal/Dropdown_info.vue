<template>
<div class="reactors_container" v-show='this.isHover'>
    <div class="reactors_list">
        <div class="reactors_info"
            v-for='reactor in this.reactors_list.slice(0,5)' :key='reactor'>
                <img class="profile_img" src="../../assets/test_blog_photo.png" alt="">
                <span class="profile_name">{{reactor.username.split('.')[0]}}</span> 
        </div>
        <div class='more_reactors_btn' data-bs-toggle="modal" data-bs-target="#ReactorsModal" v-if="this.reactors_list.length> 5">Show more...</div>
    </div>
</div>

 
</template>

<script>
export default {
    data(){return{}},
    props:['isHover','reactors_list'],
}
</script>

<style lang="scss" scoped>

.reactors_list{
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
    padding: 5px 10px;
    width: max-content;
    background-color:var(--bg_button_color);
    border-radius: 10px;
    color: var(--text_color_secondary);
    font-weight: 300;

    .reactors_info{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding: 4px 5px;

        .profile_img{
            border-radius: 50%;
            width: 20px;
            height: 20px;
            margin-right: 8px;
            background-color: #ffff;
        }

        .profile_name{
            max-width: 100px;
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap; 
            cursor: pointer;

            &:hover{
                color: var(--bg_button_active_color);
            }
        }
    }

    .more_reactors_btn{
        display: flex;
        justify-content: center;
        padding: 2px 0;
        cursor: pointer;

        &:hover{
            color: var(--bg_button_active_color);
        }
    }

    .reactors_info:not(:last-child){
        border-bottom: 1px solid var(--text_color_secondary);
    }
}

</style>