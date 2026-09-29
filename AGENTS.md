# AGENTS.md - 智能体协作与项目上下文规范

> **目标受众**：Hermes、Codex、Claude Code 或任何接入本项目的 AI Coding Agent。  
> **核心原则**：进入项目后优先阅读本文件，禁止脱离本文档与已有架构自作主张重构。

---

## 1. 项目基本画像 (Project Profile)
- **项目名称**：社区图书馆借阅管理系统 (Community Library Management System)
- **项目定位**：面向中小型社区/机构的轻量化图书借还与读者管理系统。
- **技术栈**：
  - **后端**：Python 3.10+ / FastAPI / SQLite (SQLAlchemy ORM) / Uvicorn
  - **前端**：Vue 3 (Composition API / `<script setup>`) / Vite / Element Plus / Axios / Vue Router
  - **样式规范**：莫兰迪暖米色/极简质感，内置多套浅色主题切换。

---

## 2. 运行与环境配置 (Run & Dev Specs)
- **本地服务端口规范**：
  - **后端服务**：`http://localhost:8001`（注意：避免占用 8000 端口）
  - **前端服务**：`http://localhost:5174`（Vite 代理 `/api` -> `http://localhost:8001`）
  - **API 交互文档**：`http://localhost:8001/docs`
- **默认凭据**：
  - 角色：系统管理员
  - 账号：`admin`
  - 密码：`admin123`
- **一键启动方式**：
  - Linux/WSL: `./start.sh` (或分别在 `backend/` 下 `./venv/bin/python run.py`，在 `frontend/` 下 `npm run dev`)
  - Windows: `start.bat`

---

## 3. 核心业务与数据模型 (Data Schema & Domain)
- **核心数据表** (SQLite)：
  1. `books`: 图书基础信息（ISBN、书名、作者、分类、总藏书量、可借册数 `available_copies`）。
  2. `book_copies`: 单册实体副本（条形码、架位、状态：在馆/借出/损坏）。
  3. `members`: 读者会员（姓名、手机号、卡号、最大借书上限、状态）。
  4. `categories`: 图书分类字典。
  5. `borrows`: 借阅记录（借出时间、应还时间、实还时间、逾期状态、续借次数）。
  6. `operators`: 管理员账号。

---

## 4. 关键架构设计与避坑指南 (Architecture & Pitfalls)
1. **可借册数同步 (`available_copies`)**：
   - 借书与还书操作**必须保证原子性更新** `books.available_copies`。严禁绕过业务逻辑直接往 `borrows` 插入记录导致副本数不同步。
2. **API 前缀路径与拦截器**：
   - 前端 Axios 已统一封装 baseURL 与响应拦截解包，编写新 API 时路径必须为相对路径（如 `/borrows`，严禁叠加双重 `/api/api/...`）。
3. **分类删除保护**：
   - 当分类下仍有关联图书时，后端拦截物理删除，前端需给出友好阻断提示。
4. **长列表布局规范**：
   - 禁止在表格内部嵌套局部硬截断滚动条，应自适应撑开由外层右侧单轨滑块统一接管。

---

## 5. 当前功能完成度与演进路线 (Current State & Backlog)

### ✅ 已完成功能
- [x] 图书 CRUD、ISBN 自动录入与分类联动
- [x] 读者会员建档、借阅额度管控
- [x] 借书、还书、续借、撤销借阅完整闭环
- [x] 逾期状态自动判定与借阅记录多维度筛选
- [x] 图书热度总榜与借阅统计
- [x] 6 款浅色主题切换系统
- [x] 逾期记录一键「催还」前端交互按钮 (`BorrowList.vue`)

### ⚠️ 待接入功能 (Next Steps for Next Agent)
1. **催还通知后端服务**：
   - 当前状态：前端 `BorrowList.vue` 的 `doRemind` 函数仅完成了前端确认框与成功提示（模拟逻辑）。
   - 待办：后端新增 `POST /api/borrows/{id}/remind` 接口，支持记录最后催还时间、催还次数，预留短信/邮件 Webhook 通道。
2. **借阅凭条/二维码打印**：借阅成功后支持导出或打印借阅小票。
3. **数据报表导出**：支持 Excel/CSV 导出月度借阅统计与逾期明细。

---

## 6. Agent 交付规则 (Agent Instructions)
- 修改任何代码前，必须检查前后端端口与数据一致性。
- 新增功能后，必须更新 `DEV_LOG.md` 记录本次迭代内容与技术决策，并保持本 `AGENTS.md` 的路线图同步。
