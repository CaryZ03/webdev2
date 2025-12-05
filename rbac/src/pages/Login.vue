<template>
  <div class="login-container">
    <div class="login-box">
      <h2>权限管理系统</h2>
      <div class="form-group">
        <input 
          v-model="form.username" 
          type="text" 
          placeholder="用户名" 
          :disabled="loading"
          @keyup.enter="login"
        />
      </div>
      <div class="form-group">
        <input 
          v-model="form.password" 
          type="password" 
          placeholder="密码" 
          :disabled="loading"
          @keyup.enter="login"
        />
      </div>
      <button 
        @click="login" 
        :disabled="loading || !form.username || !form.password"
        class="login-btn"
      >
        <span v-if="loading">登录中...</span>
        <span v-else>登录</span>
      </button>
      <p v-if="err" class="error-message">{{ err }}</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import request from '../utils/request'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = reactive({ username: '', password: '' })
const loading = ref(false)
const err = ref('')

async function login() {
  if (!form.username || !form.password) {
    err.value = '请输入用户名和密码'
    return
  }

  loading.value = true
  err.value = ''
  
  try {
    const res = await request('/api/v1/auth/login', { 
      method: 'POST', 
      body: JSON.stringify(form) 
    })
    
    if (res && res.code === 200) {
      localStorage.setItem('token', res.data.token)
      router.push('/home')
    } else {
      err.value = res?.message || '登录失败，请检查用户名和密码'
    }
  } catch (error) {
    err.value = '网络错误，请稍后重试'
    console.error('Login error:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.login-box h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
  box-sizing: border-box;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.form-group input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.login-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: opacity 0.3s;
  margin-bottom: 15px;
}

.login-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  text-align: center;
  font-size: 14px;
  margin-top: 10px;
}
</style>