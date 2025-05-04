import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import UsersView from '../views/UsersView.vue'
import AddNewProfileView from '../views/AddNewProfileView.vue'
import ProfileFavouritesView from '../views/ProfileFavouritesView.vue'
import LogoutView from '../views/LogoutView.vue'
import ViewProfilesView from '../views/ViewProfilesView.vue'
import ProfileMatchesView from '../views/ProfileMatchesView.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/Login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/Users',
      name: 'Users',
      component: UsersView
    },
    {
      path: '/addprofile',
      name: 'addprofile',
      component: AddNewProfileView
    },
    {
      path: '/Favourites',
      name: 'Favourites',
      component: ProfileFavouritesView
    },
    {
      path: '/Logout',
      name: 'logout',
      component: LogoutView
    },
    {
      path: '/profiles/:id',
      name: 'ViewProfile',
      component: ViewProfilesView
    },
    {
      path:'/profiles/matches/:id',
      name: 'matchprofile',
      component: ProfileMatchesView
    }

  ]
})

export default router
