from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

TOKEN_EXPIRE_TIME = 2 * 60 * 60

users = {
    "admin": {"id": 1, "username": "admin", "password": "123456", "role": "admin", "email": "admin@rbac.com", "dept": "管理部"},
    "user":  {"id": 2, "username": "user",  "password": "123456", "role": "user",  "email": "user@rbac.com",  "dept": "研发部"}
}

all_menus = [
    {"id": 1, "name": "个人信息", "path": "/home/profile", "roles": ["admin", "user"]},
    {"id": 2, "name": "用户管理", "path": "/home/users",   "roles": ["admin"]},
    {"id": 3, "name": "系统设置", "path": "/home/settings", "roles": ["admin"]}
]

def verify_token(token):
    if not token or "-" not in token:
        return None, "无效的token格式"
    
    try:
        parts = token.split("-")
        if len(parts) < 4 or parts[0] != "fake" or parts[1] != "jwt":
            return None, "无效的token格式"
        
        user_id = int(parts[2])
        expire_time = float(parts[3])
    except (ValueError, IndexError):
        return None, "无效的token格式"
    
    if time.time() > expire_time:
        return None, "token已过期"
    
    user = next((u for u in users.values() if u["id"] == user_id), None)
    if not user:
        return None, "用户不存在"
    
    return user, None

@app.post("/api/v1/auth/login")
def login():
    data = request.get_json()
    u = users.get(data.get("username"))
    if not u or u["password"] != data.get("password"):
        return jsonify(code=400, message="用户名或密码错误"), 400
    
    expire_time = time.time() + TOKEN_EXPIRE_TIME
    token = f"fake-jwt-{u['id']}-{expire_time}"
    
    return jsonify(code=200, data={"token": token, "user": {"username": u["username"], "role": u["role"]}})

@app.get("/api/v1/menus")
def menus():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.split(" ")[-1] if auth_header else ""
    
    user, error_msg = verify_token(token)
    if not user:
        return jsonify(code=401, message=error_msg or "未授权，请重新登录"), 401
    
    role = user["role"]
    filtered_menus = [m for m in all_menus if role in m["roles"]]
    return jsonify(code=200, data=filtered_menus)

@app.get("/api/v1/user/profile")
def profile():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.split(" ")[-1] if auth_header else ""
    
    user, error_msg = verify_token(token)
    if not user:
        return jsonify(code=401, message=error_msg or "未授权，请重新登录"), 401
    
    return jsonify(code=200, data=user)

@app.post("/api/v1/admin/delete-user")
def delete_user():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.split(" ")[-1] if auth_header else ""
    
    user, error_msg = verify_token(token)
    if not user:
        return jsonify(code=401, message=error_msg or "未授权，请重新登录"), 401
    
    role = user["role"]
    if role != "admin":
        return jsonify(code=403, message="权限不足"), 403
    return jsonify(code=200, message="删除成功")

if __name__ == '__main__':
    app.run(port=3000, debug=True)