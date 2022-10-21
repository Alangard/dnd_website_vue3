<template>
    <div class="main-container" :class="{'light-theme': this.$store.state.theme =='light', 'dark-theme': this.$store.state.theme =='dark'}">

        <div class="test-div">
            test div
        </div>
    </div>

</template>

<script>
export default {
    data(){
        return{
            data: {'1': [],
                   '2': []},
        }
    },

}
</script>


<style lang="scss" scoped>
.main-containe{
    width: 400px;
    height: 400px;

    .test-div{
        background-color: var(--bg_color);
    }


}
</style>