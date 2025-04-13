# 学习网站API接口文档

## 1. 概述
### 1.1 基础信息
- **基础URL**: `http://127.0.0.1:8000/api/`
- **认证方式**: JWT (Bearer Token)
- **响应格式**: JSON
- **版本**: v1.0

### 1.2 通用响应格式
```json
{
    "code": 200,
    "message": "成功",
    "data": {}
}
```

### 1.3 错误处理
- 所有错误返回统一格式
- 包含错误码和描述信息

## 通用响应格式
```json
{
    "code": 200,          // 状态码
    "message": "成功",    // 响应消息
    "data": {}           // 响应数据
}
```

## 2. 认证接口

### 2.1 用户注册
### 注意事项
- 不允许注册管理员账号(user_type='admin')
- 尝试注册管理员账号将返回400错误
- **接口**: `POST /users/register/`
- **描述**: 新用户注册接口
- **请求头**: 无
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |--------|------|------|------|
  | username | string | 是 | 用户名 |
  | email | string | 是 | 邮箱地址 |
  | password | string | 是 | 密码 |
  | user_type | string | 是 | 用户类型(teacher/student)，不允许注册管理员账号 |
  | student_id | string | 条件必填 | 学号，当user_type为student时必填 |
  | teacher_id | string | 条件必填 | 教工号，当user_type为teacher时必填 |
- **请求示例**:
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "user_type": "student",
    "student_id": "2024001"
  }
  ```
- **响应示例**:
  ```json
  {
    "code": 200,
    "message": "注册成功",
    "data": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "user_type": "student",
      "student_id": "2024001"
    }
  }
  ```
- **错误码**:
  | 错误码 | 说明 |
  |--------|------|
  | 400 | 参数错误 |
  | 409 | 用户名已存在 |

### 1.2 用户登录
- **接口**：`POST /users/login/`
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |--------|------|------|------|
  | email | string | 是 | 用户邮箱 |
  | password | string | 是 | 用户密码 |
- **请求体示例**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **响应**：
  ```json
  {
    "code": 200,
    "message": "成功",
    "data": {
      "access": "access_token",
      "refresh": "refresh_token"
    }
  }
  ```

### 1.3 刷新Token
- **接口**：`POST /users/token/refresh/`
- **请求体**：
  ```json
  {
    "refresh": "refresh_token"
  }
  ```
- **响应**：
  ```json
  {
    "code": 200,
    "message": "刷新成功",
    "data": {
      "access": "new_access_token"
    }
  }
  ```

### 1.4 用户注销
- **接口**：`POST /users/logout/`
- **请求头**：`Authorization: Bearer <access_token>`
- **响应**：
  ```json
  {
    "code": 200,
    "message": "注销成功"
  }
  ```
- **说明**：
  - 注销后用户需要重新登录才能访问受保护接口
  - 注销会清除用户的登录状态

## 2. 用户管理接口

### 2.1 获取用户信息
- **接口**：`GET /users/profile/`
- **请求头**：`Authorization: Bearer <access_token>`
- **响应**：
  ```json
  {
    "code": 200,
    "message": "成功",
    "data": {
      "username": "string",
      "email": "user@example.com",
      "user_type": "student"
    }
  }
  ```

### 2.2 更新用户信息
- **接口**：`PUT /users/profile/`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |--------|------|------|------|
  | username | string | 否 | 新用户名 |
  | password | string | 否 | 新密码 |
  | phone | string | 否 | 新手机号 |
- **请求体示例**:
  ```json
  {
    "username": "new_username",
    "password": "new_password",
    "phone": "13800138000"
  }
  ```
- **响应**：
  ```json
  {
    "code": 200,
    "message": "更新成功",
    "data": {
      "id": 1,
      "username": "new_username",
      "email": "user@example.com",
      "phone": "13800138000"
    }
  }
  ```
- **说明**：
  - 邮箱地址不可更改
  - 可以只更新部分字段，不需要同时更新所有字段

## 3. 课程管理接口

### 3.1 创建课程
- **接口**：`POST /courses/`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |--------|------|------|------|
  | name | string | 是 | 课程名称 |
  | description | string | 否 | 课程描述 |
  | teacher | integer | 是 | 教师ID |
  | chapters | array | 否 | 课程章节ID列表 |
  | status | string | 否 | 课程状态(active/archived)，默认active |
- **请求体示例**:
  ```json
  {
    "name": "Python编程",
    "description": "Python基础课程",
    "teacher_id": 1,
    "chapter": "basic"
  }
  ```
- **响应示例**:
  ```json
  {
    "code": 201,
    "message": "创建成功",
    "data": {
      "id": 1,
      "name": "Python编程",
      "teacher": {
        "id": 1,
        "username": "teacher1",
        "user_type": "teacher"
      },
      "description": "Python基础课程",
      "created_at": "2023-01-01T00:00:00Z",
      "students": [],
      "student_count": 0,
      "chapter": "basic",
      "chapter_display": "基础课程"
    }
  }
  
- **错误码**:
  | 错误码 | 说明 |
  |--------|------|
  | 400 | 参数错误 |
  | 401 | 未授权 |
  | 403 | 权限不足 |
    "chapter_id": "章节编号"
  
- **响应示例**:
  ```json
  {
    "code": 201,
    "message": "创建成功",
    "data": {
      "id": 1,
      "name": "Python编程",
      "description": "Python基础课程",
      "chapter_id": 1,
      "teacher": {
        "id": 1,
        "username": "teacher1",
        "user_type": "teacher"
      },
      "created_at": "2023-01-01T00:00:00Z",
      "student_count": 0
    }
  }
  ```
- **错误码**:
  | 错误码 | 说明 |
  |--------|------|
  | 400 | 参数错误 |
  | 401 | 未授权 |
  | 403 | 权限不足 |

### 3.2 获取课程列表
- **接口**：`GET /courses/`
- **请求参数**：
  - `page`: 页码（默认1）
  - `size`: 每页数量（默认10）
  - `search`: 搜索关键词
  - `status`: 课程状态筛选(active/archived)
  - `ordering`: 排序字段（created_at/-created_at）
- **响应**：
  ```json
  {
    "code": 200,
    "message": "成功",
    "data": {
      "total": 100,
      "pages": 10,
      "current_page": 1,
      "items": [
        {
          "id": 1,
          "title": "课程标题",
          "description": "课程描述",
          "chapter": "章节编号",
          "teacher": {
            "id": 1,
            "username": "teacher"
          },
          "created_at": "2024-03-20T10:00:00Z"
        }
      ]
    }
  }
  ```

### 3.3 获取课程详情
- **接口**：`GET /courses/{id}/`
- **响应**：
  ```json
  {
    "code": 200,
    "message": "成功",
    "data": {
      "id": 1,
      "name": "测试课程",
      "description": "课程描述",
      "teacher": {
        "id": 1,
        "username": "teacher"
      }
    }
  }
  ```

### 3.4 更新课程
- **接口**：`PUT /courses/{id}/`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体**：
  ```json
  {
    "title": "新课程标题",
    "description": "新课程描述"
  }
  ```
- **响应**：
  ```json
  {
    "code": 200,
    "message": "更新成功",
    "data": {
      "id": 1,
      "title": "新课程标题",
      "description": "新课程描述",
      "teacher": {
        "id": 1,
        "username": "teacher"
      },
      "created_at": "2024-03-20T10:00:00Z"
    }
  }
  ```

### 3.5 删除课程
- **接口**：`DELETE /courses/{id}/`
- **请求头**：`Authorization: Bearer <access_token>`
- **响应**：
  ```json
  {
    "code": 200,
    "message": "删除成功"
  }
  ```

## 4. 课程章节管理接口

### 4.1 获取章节列表
- **接口**：`GET /api/courses/chapters/`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求参数**：
  - `page`: 页码（默认1）
  - `size`: 每页数量（默认10）
  - `search`: 搜索关键词（搜索name和description字段）
  - `ordering`: 排序字段（order/-order/created_at/-created_at）
- **响应示例**:
  ```json
  {
    "code": 200,
    "message": "成功",
    "data": {
      "total": 10,
      "pages": 1,
      "current_page": 1,
      "items": [
        {
          "id": 1,
          "name": "基础课程",
          "description": "课程基础内容",
          "order": 1,
          "created_at": "2024-03-20T10:00:00Z"
        },
        {
          "id": 2,
          "name": "进阶课程",
          "description": "课程进阶内容",
          "order": 2,
          "created_at": "2024-03-20T10:00:00Z"
        }
      ]
    }
  }
  ```

### 4.2 创建章节
- **接口**：`POST /api/courses/chapters/`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |--------|------|------|------|
  | name | string | 是 | 章节名称 |
  | description | string | 否 | 章节描述 |
  | order | integer | 否 | 排序序号，默认1 |
- **响应示例**:
  ```json
  {
    "code": 201,
    "message": "创建成功",
    "data": {
      "id": 1,
      "name": "基础课程",
      "description": "课程基础内容",
      "order": 1
    }
  }
  ```

### 4.3 更新章节
- **接口**：`PUT /api/courses/chapters/{id}/`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |--------|------|------|------|
  | name | string | 否 | 章节名称 |
  | description | string | 否 | 章节描述 |
  | order | integer | 否 | 排序序号 |
- **响应示例**:
  ```json
  {
    "code": 200,
    "message": "更新成功",
    "data": {
      "id": 1,
      "name": "基础课程（更新）",
      "description": "更新后的课程描述",
      "order": 2
    }
  }
  ```

### 4.4 删除章节
- **接口**：`DELETE /api/courses/chapters/{id}/`
- **请求头**：`Authorization: Bearer <access_token>`
- **响应示例**：
  ```json
  {
    "code": 200,
    "message": "删除成功"
  }
  ```

## 5. 课程内容管理接口

### 5.1 获取课程内容列表
- **接口**：`GET /courses/{course_id}/contents/`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求参数**：
  - `page`: 页码（默认1）
  - `size`: 每页数量（默认10）
  - `order`: 排序字段（created_at/order）
- **响应**：
  ```json
  {
    "code": 200,
    "message": "成功",
    "data": {
      "total": 10,
      "pages": 1,
      "current_page": 1,
      "items": [
        {
          "id": 1,
          "title": "章节标题",
          "content": "章节内容",
          "order": 1,
          "created_at": "2024-03-20T10:00:00Z"
        }
      ]
    }
  }
  ```

### 5.2 获取课程内容详情
- **接口**：`GET /courses/{course_id}/contents/{content_id}/`
- **请求头**：`Authorization: Bearer <access_token>`
- **响应**：
  ```json
  {
    "code": 200,
    "message": "成功",
    "data": {
      "id": 1,
      "title": "章节标题",
      "content": "章节内容",
      "order": 1,
      "created_at": "2024-03-20T10:00:00Z"
    }
  }
  ```

### 5.3 添加课程内容
- **接口**：`POST /courses/{course_id}/contents/`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |--------|------|------|------|
  | title | string | 是 | 章节标题 |
  | content | string | 是 | 章节内容 |
  | order | integer | 否 | 排序序号，默认1 |
- **响应示例**：
  ```json
  {
    "code": 200,
    "message": "创建成功",
    "data": {
      "id": 1,
      "title": "章节标题",
      "content": "章节内容",
      "order": 1,
      "created_at": "2024-03-20T10:00:00Z"
    }
  }
  ```

### 5.4 更新课程内容
- **接口**：`PUT /courses/{course_id}/contents/{content_id}/`
- **请求头**：`Authorization: Bearer <access_token>`
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |--------|------|------|------|
  | title | string | 否 | 章节标题 |
  | content | string | 否 | 章节内容 |
  | order | integer | 否 | 排序序号 |
- **响应示例**：
  ```json
  {
    "code": 200,
    "message": "更新成功",
    "data": {
      "id": 1,
      "title": "新章节标题",
      "content": "新章节内容",
      "order": 2,
      "created_at": "2024-03-20T10:00:00Z"
    }
  }
  ```

### 5.5 删除课程内容
- **接口**：`DELETE /courses/{course_id}/contents/{content_id}/`
- **请求头**：`Authorization: Bearer <access_token>`
- **响应示例**：
  ```json
  {
    "code": 200,
    "message": "删除成功"
  }
  ```

## 6. 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |