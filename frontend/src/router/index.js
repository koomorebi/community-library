import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Layout from '../views/Layout.vue'
import Dashboard from '../views/Dashboard.vue'
import BookList from '../views/BookList.vue'
import CategoryList from '../views/CategoryList.vue'
import MemberList from '../views/MemberList.vue'
import BorrowList from '../views/BorrowList.vue'
import RemindSettings from '../views/RemindSettings.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: Dashboard, meta: { title: '工作台' } },
      { path: 'books', name: 'BookList', component: BookList, meta: { title: '图书管理' } },
      { path: 'categories', name: 'CategoryList', component: CategoryList, meta: { title: '分类管理' } },
      { path: 'members', name: 'MemberList', component: MemberList, meta: { title: '会员管理' } },
      { path: 'borrows', name: 'BorrowList', component: BorrowList, meta: { title: '借阅管理' } },
      { path: 'remind', name: 'RemindSettings', component: RemindSettings, meta: { title: '提醒设置' } },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/')
  } else {
    next()
  }
})

export default router
