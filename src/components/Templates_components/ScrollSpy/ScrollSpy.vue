<template>
    <div class="main_wrapper">
        <div class="article" ref="content" :class='{mobile: isMobile}'>
            <slot name='scrollspy_articles'></slot>
        </div>
        <div class="aside" :class='{mobile: isMobile}'>
            <slot name='scrollspy_aside__links'></slot>
        </div>
    </div>
</template>

<script>
export default {
    props:['isMobile'],

    data() {return {}},

    mounted(){
        this.$nextTick(function () {
            // The code that will be run only after
            // all views are rendered

            const sections = document.querySelectorAll('.section');
            const links_list = document.querySelectorAll('.aside_link');

            var options = {
                root: document.querySelector('.article'),
                rootMargin: '0% 0% -97% 0%',
                threshold: 0
            }

            const cb = (entries) => {
                entries.forEach(entry => {
                    if(entry.isIntersecting ){
                        links_list.forEach((link) => link.classList.remove('active'));
                        sections.forEach((section) => section.querySelector('.section_header').classList.remove('active'));


                        const activeId = entry.target.id;
                        const activeLink = document.querySelector(`.aside_link[id="${activeId}"]`);
                        const activeSection = document.querySelector(`.section[id="${activeId}"]`);
                        
                        if(activeLink){activeLink.classList.add('active');}
                        if(activeSection){activeSection.querySelector('.section_header').classList.add('active')};
                    }

                });
            };

            const sectionObserver = new IntersectionObserver(cb, options);
            sections.forEach((s) => sectionObserver.observe(s));
        })  

    },
}
</script>

<style lang="scss" scoped>
.main_wrapper{
    display: flex;
    margin-bottom: 10px;
}

.article{
    position: relative;
    max-height: 300px;
    width: 100%;
    overflow-y: hidden;
    scroll-behavior: smooth;
    border-radius: 5px;

    &:hover, &:focus{
        overflow-y: scroll;
    }
    
    &::-webkit-scrollbar{
        width: 7px;
        min-width: 5px;
    }

    &::-webkit-scrollbar-track{
        background-color: transparent;
        border-radius: 5px;
    }

    &::-webkit-scrollbar-thumb{
        background-color: var(--text_color_secondary);
        border-radius: 5px;
    }

    &.mobile{
        overflow-y: scroll;
    }
}

.aside{
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-left: 5px;
    background-color: var(--bg_button_color);
    border-radius: 5px;
}

</style>