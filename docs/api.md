
# 大学生成绩查询系统（MVP）API 文档 v1.0

## 1. 基本信息
- **Base URL**：`http://your-domain.com/api`
- **所有接口均需使用 HTTPS**。
- **请求与响应数据格式**：`application/json`
- **字符编码**：UTF-8

## 2. 认证方式
- 登录成功后返回 **Bearer Token**（JWT 格式）。
- 后续请求需在 Header 中携带：
  ```
  Authorization: Bearer <token>
  ```
- Token 有效期：24 小时。

## 3. 接口列表

### 3.1 学生登录

**接口描述**：学生使用学号和密码登录，获取访问令牌。

- **URL**：`/auth/login`
- **Method**：`POST`
- **请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| studentId | string | 是 | 学号，如 `2021001234` |
| password | string | 是 | 密码（明文，后台加密验证） |

**请求示例**：
```json
{
  "studentId": "2021001234",
  "password": "123456"
}
```

**响应成功（200 OK）**：
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 86400,
    "studentInfo": {
      "studentId": "2021001234",
      "name": "张三",
      "major": "计算机科学与技术",
      "grade": "2021级"
    }
  }
}
```

**响应失败（401 Unauthorized）**：
```json
{
  "code": 401,
  "message": "学号或密码错误",
  "data": null
}
```

---

### 3.2 学生注册

**接口描述**：学生使用学号、姓名和密码注册账号，注册成功后返回访问令牌。

- **URL**：`/auth/register`
- **Method**：`POST`
- **请求体**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| studentId | string | 是 | 学号，如 `2021001234` |
| name | string | 是 | 姓名 |
| password | string | 是 | 密码（明文，后台加密存储） |
| major | string | 否 | 专业 |
| grade | string | 否 | 年级，如 `2021级` |

**请求示例**：
```json
{
  "studentId": "2021009999",
  "name": "赵六",
  "password": "123456",
  "major": "软件工程",
  "grade": "2023级"
}
```

**响应成功（200 OK）**：
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 86400,
    "studentInfo": {
      "studentId": "2021009999",
      "name": "赵六",
      "major": "软件工程",
      "grade": "2023级"
    }
  }
}
```

**响应失败（409 Conflict）**：
```json
{
  "code": 409,
  "message": "学号已存在",
  "data": null
}
```

---

### 3.3 查询学生成绩

**接口描述**：学生登录后查询本人的课程成绩列表，支持按学年、学期筛选（可选）。只返回已发布的成绩。

- **URL**：`/grades`
- **Method**：`GET`
- **Headers**：`Authorization: Bearer <token>`
- **Query 参数（可选）**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| academicYear | string | 否 | 学年，如 `2024-2025` |
| semester | string | 否 | 学期：`AUTUMN`（秋季）、`SPRING`（春季）、`SUMMER`（夏季） |

若不传任何筛选参数，则返回该生所有学期成绩。

**请求示例**（查询2024-2025学年秋季学期成绩）：
```
GET /api/grades?academicYear=2024-2025&semester=AUTUMN
```

**响应成功（200 OK）**：
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "studentId": "2021001234",
    "name": "张三",
    "grades": [
      {
        "courseId": "CS101",
        "courseName": "程序设计基础",
        "credit": 3.5,
        "courseNature": "必修",
        "academicYear": "2024-2025",
        "semester": "AUTUMN",
        "score": 88.5,
        "gradePoint": 3.7,
        "status": "正常"
      },
      {
        "courseId": "MA102",
        "courseName": "高等数学A",
        "credit": 5.0,
        "courseNature": "必修",
        "academicYear": "2024-2025",
        "semester": "AUTUMN",
        "score": 72.0,
        "gradePoint": 2.3,
        "status": "正常"
      },
      {
        "courseId": "PE001",
        "courseName": "大学体育",
        "credit": 1.0,
        "courseNature": "必修",
        "academicYear": "2024-2025",
        "semester": "AUTUMN",
        "score": 95.0,
        "gradePoint": 4.0,
        "status": "正常"
      }
    ],
    "summary": {
      "totalCredit": 9.5,
      "gpa": 3.41
    }
  }
}
```

**字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| courseId | string | 课程编号 |
| courseName | string | 课程名称 |
| credit | float | 学分 |
| courseNature | string | 必修 / 选修 / 公选 |
| academicYear | string | 学年 |
| semester | string | 学期（AUTUMN/SPRING/SUMMER） |
| score | float | 总评成绩（百分制） |
| gradePoint | float | 该课程绩点（按学校规则换算） |
| status | string | 成绩状态（正常/补考/重修） |
| summary.totalCredit | float | 所选课程总学分（筛选范围内的） |
| summary.gpa | float | 加权平均绩点（筛选范围内的） |

**响应失败（401 Unauthorized）**：
```json
{
  "code": 401,
  "message": "Token无效或已过期",
  "data": null
}
```

**响应失败（404 Not Found）**：
```json
{
  "code": 404,
  "message": "未查询到成绩数据",
  "data": null
}
```

**响应失败（400 参数错误）**：
```json
{
  "code": 400,
  "message": "semester参数值无效，允许值：AUTUMN, SPRING, SUMMER",
  "data": null
}
```

---

## 4. 通用错误码

| 错误码 | 含义 | 说明 |
|--------|------|------|
| 200 | 成功 | 请求处理成功 |
| 400 | 请求参数错误 | 参数缺失、格式不正确或值非法 |
| 401 | 未授权 | Token无效、过期或未提供 |
| 403 | 无权限 | 已认证但无权访问该资源（MVP不会出现） |
| 404 | 资源不存在 | 未找到成绩数据或用户不存在 |
| 409 | 资源冲突 | 学号已存在 |
| 500 | 服务器内部错误 | 后端服务异常 |

---

## 5. 补充说明（MVP 简易实现）

- **密码验证**：后台存储密码的哈希值（如 bcrypt），不存储明文。
- **成绩数据来源**：可预先通过脚本或后台导入历史数据，学生登录后只返回本人数据。
- **筛选逻辑**：`academicYear` 和 `semester` 可组合使用；若只传其中一个，则按该条件过滤。
- **GPA 计算**：按学校规则实时计算（例如：分数≥90→4.0，85~89→3.7 等），在 MVP 中可使用简单公式。
- **无须实现**：教师端、教务端、成绩录入/审核、补考重修复杂逻辑、成绩单打印等。

---

## 6. 快速验证流程

1. 调用 `POST /auth/login` 获取 token。
2. 将 token 放在 Header 中调用 `GET /grades` 查看成绩。
3. 尝试带查询参数 `?academicYear=2024-2025&semester=AUTUMN` 测试筛选。

---
