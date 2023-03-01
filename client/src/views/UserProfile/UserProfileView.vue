<template>
    <div>Это страница пользователя {{id.split('.')[0]}}</div>
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