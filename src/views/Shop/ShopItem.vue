<template>
    <div class="main-container" :class="{'light-theme': this.$store.state.theme =='light', 'dark-theme': this.$store.state.theme =='dark'}">

        <div class="test-div">
           Shop Item {{id}}
        </div>
    </div>

</template>

<script>
import { onBeforeMount } from '@vue/runtime-core'
export default {
    data(){
        return{
            id: this.$route.params.id,
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