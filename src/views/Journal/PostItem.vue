<template>
    <comments></comments>
</template>


<script>
import Comments from '@/components/Journal/Comments/Comments.vue';
export default {
    components: { Comments } ,
    data(){
        return{
            id: this.$route.params.id
        }
    }
}
</script>