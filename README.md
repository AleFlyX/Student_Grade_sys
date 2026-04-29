# 学生成绩查询系统

这是一个基于 **Vue 3 + TypeScript + Element Plus + Axios** 的前端，配合 **Sanic + MySQL** 后端的学生成绩查询系统 MVP，支持登录、成绩查询、学年/学期筛选，以及 Docker 一键部署。

## 功能

- 学生登录
- 成绩查询
- 学年、学期筛选
- 绩点与总学分统计
- 后端 Docker 部署

## 项目结构

- `frontend/`：Vue 3 前端项目
- `backend/`：Sanic 后端项目
- `backend/deploy/`：Docker 部署文件与数据库脚本
- `docs/`：设计与实施文档

## 技术栈

- 前端：Vue 3、TypeScript、Vite、Element Plus、Pinia、Vue Router、Axios
- 后端：Sanic、aiomysql、PyJWT、python-dotenv
- 数据库：MySQL 8

## 本地运行

### 1. 启动后端

进入 `backend/` 后，先复制环境变量文件：

```bash
copy .env.example .env
```

安装依赖并启动：

```bash
pip install -r requirements.txt
python app.py
```

后端默认地址：`http://localhost:8000`

### 2. 启动前端

进入 `frontend/` 后：

```bash
npm install
npm run dev
```

前端默认地址：`http://localhost:5173`

## Docker 部署

后端 Docker 部署文件位于 `backend/deploy/`，其中 `docker-compose.yml` 会同时启动 MySQL 和后端服务。

在 `backend/deploy/` 目录下执行：

```bash
docker compose up -d --build
```

启动后可访问：

- 登录接口：`http://localhost:8000/api/auth/login`
- 成绩查询接口：`http://localhost:8000/api/grades`

## 数据初始化

`backend/deploy/scheme.sql` 用于初始化数据库表结构，`backend/deploy/testData.sql` 用于插入测试数据。Docker 首次启动时会自动执行这两个脚本。

## 说明

- 前端默认登录页为 `/login`。
- 登录成功后跳转到成绩查询页 `/grades`。
- 根路径 `/` 保留为 Vue 项目初始化时的首页。
