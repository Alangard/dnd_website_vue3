<template>
    <scroll-spy :isMobile='this.isMobile'>
        <template #scrollspy_articles>
            <scroll-spy-item :item_id='"recent"'>
                <template #scrollspy_section__header>Recent</template>
                <template #scrollspy_section__body>
                    Lorem, ipsum dolor sit amet consectetur adipisicing elit. Ab numquam voluptate dignissimos qui consequatur, vero exercitationem rerum nobis asperiores maxime quibusdam alias repudiandae incidunt, dolor ad architecto. Totam, accusantium nam!
                </template>
            </scroll-spy-item>

            <scroll-spy-item :item_id='"favorites"'>
                <template #scrollspy_section__header>Favorites</template>
                <template #scrollspy_section__body>
                    Lorem, ipsum dolor sit amet consectetur adipisicing elit. Ab numquam voluptate dignissimos qui consequatur, vero exercitationem rerum nobis asperiores maxime quibusdam alias repudiandae incidunt, dolor ad architecto. Totam, accusantium nam!
                </template>
            </scroll-spy-item>

            <scroll-spy-item :item_id='"most_popular"'>
                <template #scrollspy_section__header>Most Popular</template>
                <template #scrollspy_section__body>
                    Lorem, ipsum dolor sit amet consectetur adipisicing elit. Ab numquam voluptate dignissimos qui consequatur, vero exercitationem rerum nobis asperiores maxime quibusdam alias repudiandae incidunt, dolor ad architecto. Totam, accusantium nam!
                </template>
            </scroll-spy-item>

            <scroll-spy-item :item_id='"all"'>
                <template #scrollspy_section__header>All</template>
                <template #scrollspy_section__body>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Placeat, architecto est, maiores ullam odit voluptas alias, dolorum ad quod culpa odio soluta consequuntur ea sapiente veniam ratione excepturi quibusdam delectus!
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit. Expedita tempore facere illo repudiandae, totam ex vitae atque recusandae vero molestiae voluptatibus? Id temporibus sit non dolor eligendi alias, quod atque?
                    Lorem, ipsum dolor sit amet consectetur adipisicing elit. Ab numquam voluptate dignissimos qui consequatur, vero exercitationem rerum nobis asperiores maxime quibusdam alias repudiandae incidunt, dolor ad architecto. Totam, accusantium nam!
                </template>
            </scroll-spy-item>
        </template>


        <template #scrollspy_aside__links :isMobile ='this.isMobile'>
            <scroll-spy-aside-item :item_id='"recent"'>
                <template #scrollspy_aside__body>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                    </svg>
                </template>
            </scroll-spy-aside-item>

            <scroll-spy-aside-item :item_id='"favorites"'>
                <template #scrollspy_aside__body>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                    </svg>
                </template>
            </scroll-spy-aside-item>

            <scroll-spy-aside-item :item_id='"most_popular"'>
                <template #scrollspy_aside__body>
                     <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-flame" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                        <path d="M12 12c2 -2.96 0 -7 -1 -8c0 3.038 -1.773 4.741 -3 6c-1.226 1.26 -2 3.24 -2 5a6 6 0 1 0 12 0c0 -1.532 -1.056 -3.94 -2 -5c-1.786 3 -2.791 3 -4 2z"></path>
                    </svg>
                </template>
            </scroll-spy-aside-item>

            <scroll-spy-aside-item :item_id='"all"'>
                <template #scrollspy_aside__body>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="3" width="7" height="7"></rect>
                        <rect x="14" y="3" width="7" height="7"></rect>
                        <rect x="14" y="14" width="7" height="7"></rect>
                        <rect x="3" y="14" width="7" height="7"></rect>
                    </svg>
                </template>
            </scroll-spy-aside-item>
        </template>

    </scroll-spy>
</template>


<script>
import ScrollSpy from '@/components/Templates_components/ScrollSpy/ScrollSpy.vue'
import ScrollSpyItem from '@/components/Templates_components/ScrollSpy/ScrollSpyItem.vue'
import ScrollSpyAsideItem from '@/components/Templates_components/ScrollSpy/ScrollSpyAsideItem.vue'
export default {
    components: { ScrollSpy,ScrollSpyItem,ScrollSpyAsideItem},
    props:['isMobile'],
    data(){return{}}
}
</script>

<style lang="scss" scoped>

</style>