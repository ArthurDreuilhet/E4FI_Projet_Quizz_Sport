import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/Homepage.vue'
import QuizzPage from '@/views/QuizzPage.vue'
import QuestionPage from '@/views/Question.vue'
import AdminPage from '@/views/Admin_Page.vue'
import Login_Page from '@/components/Login_Page.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path: '/start',
      name: 'QuizzPage',
      component: QuizzPage,
    },
    {
      path: '/question',
      name: 'QuestionPage',
      component: QuestionPage,
    },
    {
      path: '/admin',
      name: 'AdminPage',
      component: AdminPage,
    },
    {
      path: '/admin/login',
      name: 'AdminLogin',
      component: Login_Page,
    },
    {
      path: '/result',
      name: 'ResultsPage',
      component: () => import('../views/Result.vue'),
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/QuizzPage.vue'),
    },
  ],
})

export default router
