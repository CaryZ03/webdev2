export default async (url, options = {}) => {
  const token = localStorage.getItem('token')
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers,
  }

  try {
    const response = await fetch('http://localhost:3000' + url, {
      ...options,
      headers,
    })

    if (response.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/'
      return { code: 401, message: '未授权，请重新登录' }
    }

    return response.json()
  } catch (error) {
    console.error('Request error:', error)
    return { code: 500, message: '网络错误，请稍后重试' }
  }
}