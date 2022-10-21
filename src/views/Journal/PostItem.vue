<template>
    <div>Это пост под номером {{id}}</div>
</template>

<script>
export default {
    data(){
        return{
            id: this.$route.params.id
        }
    }
}
</script>