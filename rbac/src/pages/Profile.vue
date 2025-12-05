<template>
  <div class="profile-container">
    <h2 class="page-title">个人信息</h2>
    <div class="card">
      <div class="card-header">
        <h3>用户信息</h3>
      </div>
      <div class="card-body">
        <div class="info-item">
          <span class="label">用户名：</span>
          <span class="value">{{ info.username || '加载中...' }}</span>
        </div>
        <div class="info-item">
          <span class="label">邮箱：</span>
          <span class="value">{{ info.email || '加载中...' }}</span>
        </div>
        <div class="info-item">
          <span class="label">部门：</span>
          <span class="value">{{ info.dept || '加载中...' }}</span>
        </div>
        <div class="info-item">
          <span class="label">角色：</span>
          <span class="value role-badge" :class="info.role === 'admin' ? 'admin' : 'user'">
            {{ info.role === 'admin' ? '管理员' : '普通用户' }}
          </span>
        </div>
      </div>
      <div class="card-footer">
        <button @click="adminOp" class="admin-btn" :disabled="loading">
          <span v-if="loading">操作中...</span>
          <span v-else>管理员操作</span>
        </button>
        <p v-if="msg" class="message" :class="msgType">{{ msg }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import request from '../utils/request'

const info = ref({})
const msg = ref('')
const msgType = ref('error')
const loading = ref(false)

onMounted(async () => {
  try {
    const res = await request('/api/v1/user/profile')
    if (res && res.code === 200) {
      info.value = res.data || {}
    } else {
      msg.value = '获取个人信息失败'
      msgType.value = 'error'
    }
  } catch (error) {
    console.error('Failed to load profile:', error)
    msg.value = '获取个人信息失败'
    msgType.value = 'error'
  }
})

async function adminOp() {
  msg.value = ''
  loading.value = true
  
  try {
    const res = await request('/api/v1/admin/delete-user', { 
      method: 'POST',
      body: JSON.stringify({})
    })
    
    if (res && res.code === 403) {
      msg.value = '权限不足'
      msgType.value = 'error'
    } else if (res && res.code === 200) {
      msg.value = '操作成功'
      msgType.value = 'success'
    } else {
      msg.value = res?.message || '操作失败'
      msgType.value = 'error'
    }
  } catch (error) {
    console.error('Admin operation error:', error)
    msg.value = '操作失败，请稍后重试'
    msgType.value = 'error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 600px;
}

.page-title {
  margin-bottom: 30px;
  color: #333;
  font-size: 24px;
  font-weight: 500;
}

.card {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
}

.card-body {
  padding: 25px;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.label {
  font-weight: 500;
  color: #666;
  min-width: 80px;
}

.value {
  color: #333;
  flex: 1;
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.role-badge.admin {
  background: #e7f1ff;
  color: #667eea;
}

.role-badge.user {
  background: #f0f0f0;
  color: #666;
}

.card-footer {
  padding: 20px 25px;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.admin-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: opacity 0.3s;
  margin-bottom: 10px;
}

.admin-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.admin-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.message {
  margin: 10px 0 0 0;
  padding: 10px;
  border-radius: 4px;
  font-size: 14px;
}

.message.error {
  background: #fee;
  color: #e74c3c;
  border: 1px solid #fcc;
}

.message.success {
  background: #efe;
  color: #27ae60;
  border: 1px solid #cfc;
}
</style>