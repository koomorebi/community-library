import { defineStore } from 'pinia'
import { login } from '../api/auth'
import router from '../router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null,
  }),
  actions: {
    async login(username, password) {
      const res = await login({ username, password })
      this.token = res.access_token
      localStorage.setItem('token', res.access_token)
      router.push('/')
    },
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('token')
      router.push('/login')
    },
  },
})
