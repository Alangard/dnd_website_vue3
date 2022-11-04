<template>
    <div class="main_wrapper">
        <div class="article">
            <div class="recent section">
                <div class='section_header' id='recent'>Recent</div>
                <div class='section_body'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sed veniam eius soluta, facere est fugit ratione consequatur ipsum optio quam. Excepturi, quos ipsum in eveniet esse ea voluptatem veniam fugit?</div>
            </div>
            <div class="favorites section">
                <div class='section_header' id='favorites'>Favorites</div>
                <div class='section_body'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sed veniam eius soluta, facere est fugit ratione consequatur ipsum optio quam. Excepturi, quos ipsum in eveniet esse ea voluptatem veniam fugit?</div>
            </div>
            <div class="most_popular section">
                <div class='section_header' id='most_popular'>Most Popular</div>
                <div class='section_body'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sed veniam eius soluta, facere est fugit ratione consequatur ipsum optio quam. Excepturi, quos ipsum in eveniet esse ea voluptatem veniam fugit?</div>
            </div>
            <div class="favorites section">
                <div class='all section_header' id='all'>All</div>
                <div class='section_body'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sed veniam eius soluta, facere est fugit ratione consequatur ipsum optio quam. Excepturi, quos ipsum in eveniet esse ea voluptatem veniam fugit?</div>
            </div>
        </div>
        <div class="aside">
            <a class='aside_link recent' href="#recent">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
            </a>
            <a class='aside_link favorites' href="#favorites">
                 <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                </svg>
            </a>
            <a class='aside_link most_popular' href="#most_popular">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-flame" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                    <path d="M12 12c2 -2.96 0 -7 -1 -8c0 3.038 -1.773 4.741 -3 6c-1.226 1.26 -2 3.24 -2 5a6 6 0 1 0 12 0c0 -1.532 -1.056 -3.94 -2 -5c-1.786 3 -2.791 3 -4 2z"></path>
                </svg>
            </a>
            <a class='aside_link all'  href="#all">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="7" height="7"></rect>
                    <rect x="14" y="3" width="7" height="7"></rect>
                    <rect x="14" y="14" width="7" height="7"></rect>
                    <rect x="3" y="14" width="7" height="7"></rect>
                </svg>
            </a>

        </div>
    </div>
</template>

<script>
// import { ref, onMounted } from 'vue'
//     const headers = ['Recent', 'Favorites', 'Most Popular', 'All'];
//     const currentSection = ref('')

//     onMounted(() => {
//         const observer = new IntersectionObserver((entries) => {
//             entries.forEach((entry) => {
//                 if(entry.intersectionRatio > 0){
//                     currentSection.value = entry.target.getAttribute('id');
//                 }
//             })
//         });
//         document.querySelectorAll('.section_header').forEach((section) => {
//             observer.observe(section);
//         });
//     });
</script>

<style lang="scss" scoped>
.main_wrapper{
    display: flex;
    margin-bottom: 10px;
}

.article{
    max-height: 300px;
    overflow-y: hidden;
    scroll-behavior: smooth;
    border-radius: 5px;

    &:hover, &:focus{
        overflow-y: scroll;
    }
    
    &::-webkit-scrollbar{width: 0.7vw;}

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

.section{
    margin: 0 5px 5px 0;
    border-radius: 5px;
    font-weight: 300;
    padding-bottom: 5px;
    color: var(--text_color_secondary);
    background-color: var(--bg_button_color);

    .section_header{
        position: sticky;
        top: 0;
        padding: 5px 5px 5px 15px;
        font-weight: 400;
        border-bottom: 3px solid transparent;
        border-radius: 5px;
        background-color: var(--bg_button_color);

        &.active{
        border-bottom: 3px solid var(--bg_button_active_color);
        color: var(--bg_button_active_color);
    }

    }

    .section_body{padding: 5px 10px 0 15px;}
}



.aside{
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-left: 5px;
    background-color: var(--bg_button_color);
    border-radius: 5px;

    .aside_link{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        border: 3px solid transparent;
        padding: 10px 0;
        cursor: pointer;

        &:hover{background-color: var(--active_section_color);}
        &:hover > svg{stroke: var(--bg_button_active_color);}
        &.active{
            border-left: 3px solid var(--bg_button_active_color);
            background-color: var(--active_section_color);
        }

        svg{
            width: 20px;
            height: 20px;
            stroke: var(--text_color_secondary);
        }
    }

}

</style>