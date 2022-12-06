<template>
    <div class="section" :id='this.item_id'>
        <div class='section_header'>
            <slot name='scrollspy_section__header'></slot>
        </div>
        <div class='section_body'>
            <slot name='scrollspy_section__body'></slot>
        </div>
    </div>
</template>

<script>
export default {
    props:['item_id'],
    data() {return {}},
}
</script>

<style lang="scss" scoped>

.section{
    margin: 0 7px 5px 0;
    border-radius: 5px;
    font-weight: 300;
    padding-bottom: 5px;
    color: var(--text_color_secondary);
    background-color: var(--bg_button_color);

    .section_header{
        position: sticky;
        z-index: 9999;
        top: -2px;
        padding: 5px 5px 5px 15px;
        font-weight: 400;
        border-bottom: 3px solid transparent;
        border-radius: 5px;
        background-color: var(--bg_button_color);

        &.active{
            border-bottom: 3px solid var(--bg_button_active_color);
            color: var(--bg_button_active_color);
            background-color: var(--active_section_color);
        }

    }

    .section_body{
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        padding: 5px 10px 0 10px;
    }
}



</style>