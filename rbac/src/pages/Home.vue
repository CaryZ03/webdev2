<template>
  <div class="home">
    <header class="header">
      <div class="header-left">
        <h1>权限管理系统</h1>
      </div>
      <div class="header-right">
        <span class="username">欢迎，{{ user.username || '用户' }}</span>
        <button @click="logout" class="logout-btn">退出</button>
      </div>
    </header>
    <div class="content-wrapper">
      <aside class="sidebar">
        <nav class="menu">
          <div 
            v-for="m in menus" 
            :key="m.id" 
            class="menu-item"
            :class="{ active: $route.path === m.path }"
            @click="navigateTo(m.path)"
          >
            {{ m.name }}
          </div>
        </nav>
      </aside>
      <main class="main-content">
        <router-view v-if="$route.path !== '/home'" />
        <div v-else class="welcome-page">
          <div class="welcome-content">
            <h2>欢迎使用权限管理系统</h2>
            <p>请从左侧菜单选择功能</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import request from '../utils/request'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const menus = ref([])
const user = ref({})

onMounted(async () => {
  try {
    const menuRes = await request('/api/v1/menus')
    if (menuRes && menuRes.code === 200) {
      menus.value = menuRes.data || []
    }
    
    const userRes = await request('/api/v1/user/profile')
    if (userRes && userRes.code === 200) {
      user.value = userRes.data || {}
    }
  } catch (error) {
    console.error('Failed to load data:', error)
  }
})

function navigateTo(path) {
  router.push(path)
}

function logout() {
  localStorage.removeItem('token')
  router.push('/')
}
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.header {
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-left h1 {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.username {
  font-size: 14px;
}

.logout-btn {
  padding: 6px 16px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.content-wrapper {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 220px;
  background: #f8f9fa;
  border-right: 1px solid #e9ecef;
  overflow-y: auto;
}

.menu {
  padding: 20px 0;
}

.menu-item {
  padding: 12px 20px;
  cursor: pointer;
  transition: all 0.3s;
  color: #495057;
  font-size: 14px;
  border-left: 3px solid transparent;
}

.menu-item:hover {
  background: #e9ecef;
  color: #667eea;
}

.menu-item.active {
  background: #e7f1ff;
  color: #667eea;
  border-left-color: #667eea;
  font-weight: 500;
}

.main-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
  background: #fff;
}

.welcome-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  min-height: 400px;
}

.welcome-content {
  text-align: center;
  color: #666;
}

.welcome-content h2 {
  font-size: 28px;
  margin-bottom: 15px;
  color: #333;
  font-weight: 400;
}

.welcome-content p {
  font-size: 16px;
  color: #999;
}
</style>