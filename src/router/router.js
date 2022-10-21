import { createRouter, createWebHistory } from 'vue-router'
import JournalView from '../views/Journal/JournalView.vue'
import PostItem from '../views/Journal/PostItem.vue'
import ShopView from '../views/Shop/ShopView.vue'
import ShopItem from '../views/Shop/ShopItem.vue'
import MapView from '../views/MapView.vue'
import RelationsTree from '../views/RelationsTreeView.vue'
import NotFound from '../views/404.vue'

const data = {
  '1':[],
  '2':[]
};

const routes = [
  {
    path: '/',
    name: 'home',
    redirect: to => {
      return {path: '/map'}
    },
  },
  {
    path: '/journal',
    name: 'journal',
    component: JournalView,
    children: [
    ]
  },
  {
    path: '/journal/:id',
    name: 'postitem',
    component: PostItem,
    beforeEnter(to) {
      const id = to.params.id;
      if(!(id in data)){return {
        name:'404',
        params: {pathMatch: to.path.substring(1).split('/')},
        query: to.query,
        hash: to.hash,
      }}
    }
  },
  {
    path: '/shop',
    name: 'shop',
    component: ShopView,
  },
  {
    path: '/shop/:id', 
    name: 'shopItem',
    component: ShopItem,
  },
  {
    path: '/map',
    name: 'map',
    component: MapView
  },
  {
    path: '/relations_tree',
    name: 'relations_tree',
    component: RelationsTree
  },
  {
    path: '/:pathMatch(.*)*',
    name: '404',
    component: NotFound,
    meta: {
      hideNavbar: true,
    }
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
