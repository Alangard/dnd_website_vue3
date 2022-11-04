<template>
  <div class="accordion" ref='emots_accordion'>
    
        <AccordionItem>
          <template #accordion-trigger>
            <div class="recent btn_content">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                <span>Recent</span>
            </div>
          </template>
          <template #accordion-content>
            <div class="according_body_container">
                Lorem ipsum dolor, sit amet consectetur adipisicing elit. Praesentium quo adipisci perspiciatis quas enim voluptatem, perferendis delectus eos numquam sed dolor ducimus fugit ut inventore officia consequuntur, tenetur ea quos.
            </div>
          </template>
        </AccordionItem>

        <AccordionItem>
          <template #accordion-trigger>
            <div class="favorites btn_content">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                </svg>

                <span>Favorites</span>
            </div>
          </template>
          <template #accordion-content>
            <div class="according_body_container">
                Lorem ipsum dolor, sit amet consectetur adipisicing elit. Praesentium quo adipisci perspiciatis quas enim voluptatem, perferendis delectus eos numquam sed dolor ducimus fugit ut inventore officia consequuntur, tenetur ea quos.
            </div>
          </template>
        </AccordionItem>

        <AccordionItem>
          <template #accordion-trigger>
            <div class="most_popular btn_content">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-flame" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                    <path d="M12 12c2 -2.96 0 -7 -1 -8c0 3.038 -1.773 4.741 -3 6c-1.226 1.26 -2 3.24 -2 5a6 6 0 1 0 12 0c0 -1.532 -1.056 -3.94 -2 -5c-1.786 3 -2.791 3 -4 2z"></path>
                </svg>
                <span>Most Popular</span>
            </div>
          </template>
          <template #accordion-content>
            <div class="according_body_container">
                <reaction-btn></reaction-btn>
                Lorem ipsum dolor, sit amet consectetur adipisicing elit. Praesentium quo adipisci perspiciatis quas enim voluptatem, perferendis delectus eos numquam sed dolor ducimus fugit ut inventore officia consequuntur, tenetur ea quos.
            </div>
          </template>
        </AccordionItem>
  </div>
</template>

<script>
import LongPressBtn from '@/components/Templates_components/LongPressBtn.vue';
import AccordionItem from './AccordionItem.vue';
import ReactionBtn from '../ReactionBtn.vue';
export default {
    components: { AccordionItem, LongPressBtn, ReactionBtn,},
    props: {},
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

<style lang="scss" scoped>
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
