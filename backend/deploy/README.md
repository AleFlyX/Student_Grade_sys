# 后端 Docker 部署

## 目录说明

- `Dockerfile`：后端镜像构建文件
- `docker-compose.yml`：后端 + MySQL 联合启动
- `scheme.sql`：数据库结构初始化脚本
- `testData.sql`：测试数据初始化脚本
- `.env.example`：Compose 环境变量示例

## 启动方式

1. 复制 `.env.example` 为 `.env`，按需修改密码和端口。
2. 在 `backend/deploy` 目录执行：

```bash
docker compose up -d --build
```

3. 启动后访问：

- 登录接口：`http://localhost:8000/api/auth/login`
- 成绩查询：`http://localhost:8000/api/grades`

## 注意事项

- 数据库首次启动时会自动执行 `scheme.sql` 和 `testData.sql`。
- 后端容器通过 `DB_HOST=mysql` 连接 Compose 内部的 MySQL 服务。
