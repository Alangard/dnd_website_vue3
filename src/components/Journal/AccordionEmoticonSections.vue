<template>

    <div class="main_container">

        <div class="accordion" id="personal_emots_sections">
            <div class="recent accordion-item">
                <h2 class="accordion-header" id="recent">
                    <button 
                        class="accordion-button" 
                        type="button" 
                        data-bs-toggle="collapse" 
                        data-bs-target="#recent_body" 
                        aria-expanded="false" 
                        aria-controls="recent_body"  
                        @click='isClicked'>
                    
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="10"></circle>
                            <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>

                        <span>Recent</span>
                    </button>
                </h2>
                <div id="recent_body" class="accordion-collapse collapse show" aria-labelledby="recent" data-bs-parent="#personal_emots_sections">
                    <div class="accordion-body">
                        <emoticon-btn></emoticon-btn>
                    </div>
                </div>
            </div>

            <div class="favorites accordion-item">
                <h2 class="accordion-header" id="favorites">
                    <button class="accordion-button collapsed" 
                            type="button" data-bs-toggle="collapse" 
                            data-bs-target="#favorites_body" 
                            aria-expanded="false" 
                            aria-controls="favorites_body" 
                            @click='isClicked'>
                        
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                        </svg>

                        <span>Favorites</span>

                    </button>
                </h2>
                <div id="favorites_body" class="accordion-collapse collapse" aria-labelledby="favorites" data-bs-parent="#personal_emots_sections">
                    <div class="accordion-body">
                        <strong>This is the second item's accordion body.</strong> It is hidden by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go within the <code>.accordion-body</code>, though the transition does limit overflow.
                    </div>
                </div>
            </div>

            <div class="most_popular accordion-item">
                <h2 class="accordion-header" id="most_popular">
                    <button 
                        class="accordion-button collapsed" 
                        type="button" 
                        data-bs-toggle="collapse" 
                        data-bs-target="#most_popular_body" 
                        aria-expanded="false" 
                        aria-controls="most_popular_body"
                        @click='isClicked'>
                        
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-flame" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                            <path d="M12 12c2 -2.96 0 -7 -1 -8c0 3.038 -1.773 4.741 -3 6c-1.226 1.26 -2 3.24 -2 5a6 6 0 1 0 12 0c0 -1.532 -1.056 -3.94 -2 -5c-1.786 3 -2.791 3 -4 2z"></path>
                        </svg>

                        <span>Most Popular</span>

                    </button>
                </h2>
                <div id="most_popular_body" class="accordion-collapse collapse" aria-labelledby="most_popular" data-bs-parent="#personal_emots_sections">
                    <div class="accordion-body">
                        <strong>This is the third item's accordion body.</strong> It is hidden by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go within the <code>.accordion-body</code>, though the transition does limit overflow.
                    </div>
                </div>
            </div>
        </div>

    </div>

</template>

<script>
import EmoticonBtn from './EmoticonBtn.vue';
export default {
  components: { EmoticonBtn },
    data(){return{}},
    methods:{
        isClicked(event){
            const id = event.target.attributes['data-bs-target'].value.slice(1).split('_body')[0];

            for(const element of document.querySelectorAll('.accordion-item')){
                if(element.className.includes(id)){
                    if(event.target.attributes['aria-expanded'].value == 'true'){
                        element.classList.add('show');
                    }
                    else{element.classList.remove('show');}
                    break;
                }
            }
        },
    },
    mounted(){
        document.querySelector('#recent_body').classList.remove('show');
    }

}
</script>

<style lang="scss" scoped>

    .main_container{
        margin-top: 10px;
    }

    .accordion-item{
        margin-bottom: 10px;
        box-shadow: none;
        border: none;
        background-color: transparent;
    }

    .accordion-item button{
        outline: none;
        box-shadow: none;
        border-radius: 5px;
        color: var(--text_color_secondary);
        padding: 5px 10px;
        background-color: var(--bg_button_color);
        border-left: 4px solid var(--bg_button_color);

        &::after{
            background-image: none;
        }

        &:hover{
            border-left: 4px solid var(--bg_button_active_color);
            color: var(--bg_button_active_color);
        }

        &:hover > svg{
            stroke: var(--bg_button_active_color);
        }
    }
    
    .accordion-item button[aria-expanded="true"]{
        color: var(--bg_button_active_color);
        border-bottom: 2px solid var(--bg_button_active_color);
        border-left: 4px solid var(--bg_button_active_color);
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
    }

    .accordion-item button[aria-expanded="true"] > svg{
       stroke: var(--bg_button_active_color);
    }

    svg{
        margin-right: 10px;
        stroke: var(--text_color_secondary);
    }

    .accordion-body{
        border-radius: 5px;
        border-top-left-radius: 0;
        border-top-right-radius: 0;
        background-color:var(--bg_button_color);
        font-weight: 300;
        color: var(--text_color_secondary);
        border-left: 4px solid var(--bg_button_active_color);
    }

    
</style>