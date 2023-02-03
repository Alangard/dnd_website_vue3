<template>
    <modal @close_modal='this.$emit("close_alert")'>
        <template #modal_header>
            <div class="header">
                {{ this.alert_object.header }}
            </div>       
        </template>

        <template #modal_body>
            <div class='message_text'>
                {{ this.alert_object.message }}
            </div>
            <div class="btn_container">
                <button class="cancel_btn" @click='this.$emit("close_alert")'>Cancel</button>
                <button class="action_btn" @click='this.$emit("doAction")'>{{ this.alert_object.action }}</button>
            </div>
        </template>
    </modal>

</template>

<script>
import Modal from '@/components/Templates_components/Modal.vue';


export default {
    components:{Modal},
    props:['alert_object'],

    data(){
        return{}
    },

    methods:{
    }
}
</script>

<style lang="scss" scoped>

    *{
        padding: 0;
        margin: 0;
        font-family: 'Lato', sans-serif;
        font-size: 14px;
        font-weight: 300;
        color: var(--text_color_secondary);
        
    }

    .header{
        font-weight: 700;
    }
    .btn_container{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-end;
        margin-top: 10px;

        button{
            border: none;
            outline: none;
            border-radius: 5px;
            padding: 5px;
            margin: 0 5px;
            font-weight: 500;
            font-size: 16px;
            text-transform: uppercase;
            background-color: var(--bg_button_color);

            &:hover {background-color: var(--bg_button_active_color); color: #ffff}
        }

        .action_btn{
                color: var(--error_color);
                background-color: var(--bg_button_color);
                &:hover {background-color: var(--error_color); color: #ffff}
        }
    }


</style>