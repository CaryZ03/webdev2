import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Home from '../pages/Home.vue'
import Profile from '../pages/Profile.vue'

const routes = [
  { path: '/', name: 'Login', component: Login },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    children: [
      { path: 'profile', name: 'Profile', component: Profile }
    ]
  }
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path === '/') {
    token ? next('/home') : next()
  } else {
    token ? next() : next('/')
  }
})

export default router