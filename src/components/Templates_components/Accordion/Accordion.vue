<template>
  <div class="accordion" ref='emots_accordion'>
      <slot name='accordion_body'></slot>
  </div>
</template>

<script>
export default {
    data() {
        return {
            Accordion: {
                count: 0,
                active: null
            },

        };
    },
    
    provide() {
        return { Accordion: this.Accordion };
    },

    watch:{
        'Accordion.active'(newValue, oldValue){
            const btn_elements = this.$refs.emots_accordion.querySelectorAll('.btn_content');

            for(const element of btn_elements){
                element.classList.remove('active');
            }

            if(typeof newValue === 'number'){
                btn_elements[newValue].classList.toggle('active');
            }
            else{
                btn_elements[oldValue].classList.remove('active');
            }
        }
    }
};
</script>

<style lang="scss">
.accordion {
  margin: 0;
  padding: 0;

    &__item:last-child {
    border-bottom: none;
    }

    .btn_content{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        width: 100%;

        &.active > span, &.active > svg{
            color: var(--bg_button_active_color);
            stroke: var(--bg_button_active_color); 
        }

        &:hover > span, &:hover > svg{
            color: var(--bg_button_active_color);
            stroke: var(--bg_button_active_color);
        }

        svg{
            width: 20px;
            height: 20px;
            stroke: var(--text_color_secondary);
            margin-right: 5px;
        }
    }  
}
</style>
