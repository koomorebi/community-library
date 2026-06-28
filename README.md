# 📚 社区图书馆借阅管理系统

一个面向社区居民的图书借阅管理平台，支持图书管理、会员管理、借阅管理、统计报表等功能。

## ✨ 功能特性

- 📖 **图书管理** — 图书的增删改查、分类管理、副本管理
- 👥 **会员管理** — 居民注册、信息维护、邮箱管理
- 📋 **借阅管理** — 借书、还书、续借、撤销、逾期自动检测
- 📊 **数据统计** — 仪表盘概览、借阅热度排行榜（月榜/年榜/总榜）
- 🔍 **图书历史** — 查看每本书的完整借阅记录
- 👤 **会员详情** — 查看会员借阅统计和历史记录
- ⏰ **提醒设置** — 逾期提醒配置（UI 已实现，后期待接入通知服务）
- 🔐 **权限认证** — 管理员登录、JWT Token 认证

## 🛠️ 技术栈

### 后端
- **框架**: FastAPI
- **ORM**: SQLAlchemy
- **数据库**: SQLite
- **认证**: JWT + bcrypt

### 前端
- **框架**: Vue 3
- **UI 组件**: Element Plus
- **构建工具**: Vite
- **状态管理**: Pinia
- **HTTP 客户端**: Axios

## 📁 项目结构

```
community-library/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── models/            # 数据模型
│   │   ├── routers/           # API 路由
│   │   ├── schemas/           # 数据模式
│   │   ├── middleware/        # 中间件（认证、错误处理）
│   │   ├── config.py          # 配置
│   │   ├── database.py        # 数据库连接
│   │   └── main.py            # 应用入口
│   ├── seed_data.py           # 示例数据生成脚本
│   ├── requirements.txt       # Python 依赖
│   └── run.py                 # 启动脚本
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── api/               # API 请求
│   │   ├── views/             # 页面组件
│   │   ├── stores/            # 状态管理
│   │   ├── router/            # 路由配置
│   │   └── main.js            # 入口文件
│   ├── package.json           # Node 依赖
│   └── vite.config.js         # Vite 配置
├── setup.sh / setup.bat       # 一键初始化脚本
├── start.sh / start.bat       # 一键启动脚本
└── PRD.md                      # 产品需求文档
```

## 🚀 快速开始

### 方式一：一键初始化（推荐）

```bash
# 克隆项目
git clone https://github.com/koomorebi/community-library.git
cd community-library

# Linux/Mac
./setup.sh

# Windows
setup.bat
```

初始化脚本会自动：
- ✅ 创建 Python 虚拟环境
- ✅ 安装所有依赖
- ✅ 创建数据库并生成示例数据

### 方式二：一键启动

```bash
# Linux/Mac
./start.sh

# Windows
start.bat
```

### 方式三：手动启动

```bash
# 后端
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py

# 前端（新终端）
cd frontend
npm install
npm run dev
```

### 访问系统

- **前端页面**: http://localhost:5174
- **API 文档**: http://localhost:8001/docs
- **默认账号**: admin / admin123

## 📡 API 接口

### 认证模块
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/auth/login` | 管理员登录 |

### 图书模块
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/categories` | 获取分类列表 |
| POST | `/api/v1/categories` | 新增分类 |
| PUT | `/api/v1/categories/{id}` | 修改分类 |
| DELETE | `/api/v1/categories/{id}` | 删除分类 |
| GET | `/api/v1/books` | 获取图书列表 |
| POST | `/api/v1/books` | 新增图书 |
| GET | `/api/v1/books/{id}` | 获取图书详情 |
| PUT | `/api/v1/books/{id}` | 修改图书 |
| DELETE | `/api/v1/books/{id}` | 删除图书 |

### 会员模块
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/members` | 获取会员列表 |
| POST | `/api/v1/members` | 新增会员 |
| GET | `/api/v1/members/{id}` | 获取会员信息 |
| PUT | `/api/v1/members/{id}` | 修改会员 |
| DELETE | `/api/v1/members/{id}` | 删除会员 |

### 借阅模块
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/borrows/borrow` | 借书 |
| POST | `/api/v1/borrows/return` | 还书 |
| POST | `/api/v1/borrows/renew` | 续借 |
| GET | `/api/v1/borrows` | 获取借阅记录 |
| POST | `/api/v1/borrows/undo` | 撤销借阅 |

### 统计模块
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/stats` | 获取统计数据 |
| GET | `/api/v1/stats/ranking` | 获取借阅排行榜 |

### 扩展模块
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/books/{id}/history` | 获取图书借阅历史 |
| GET | `/api/v1/members/{id}/detail` | 获取会员详情 |

## 📊 示例数据

系统内置以下示例数据：

| 类型 | 数量 | 说明 |
|------|------|------|
| 管理员 | 1 | admin / admin123 |
| 图书分类 | 8 | 文学小说、科技计算机、历史传记等 |
| 图书 | 20 | 涵盖各类经典书籍 |
| 图书副本 | 48 | 每本书 2-3 个副本 |
| 会员 | 10 | 北京地区居民 |
| 借阅记录 | 15 | 7条已还、5条借阅中、3条逾期 |

## 📸 界面预览

### 仪表盘
- 总藏书、借出中、逾期未还、今日借还统计
- 借阅热度排行榜（月榜/年榜/总榜）

### 图书管理
- 图书列表、搜索、新增、编辑、删除
- 借阅历史查看

### 会员管理
- 会员列表、搜索、新增、编辑、删除
- 会员详情（借阅统计、历史记录）

### 借阅管理
- 借阅记录列表、状态筛选（全部/借阅中/已归还/逾期）
- 借书、还书、续借、撤销操作

### 提醒设置
- 提醒方式配置（短信、邮件、微信）
- 提醒时间设置
- 测试发送功能

## 🗄️ 数据库设计

### 核心表

- `books` — 图书信息（书名、作者、ISBN、价格）
- `book_copies` — 图书副本（条码、状态）
- `categories` — 图书分类
- `members` — 会员信息（姓名、手机、邮箱、地址）
- `borrows` — 借阅记录（借书日期、应还日期、实还日期、状态）
- `admins` — 管理员账号

### 借阅状态

- `borrowed` — 借阅中
- `returned` — 已归还
- `overdue` — 逾期（系统自动检测）

## 🔧 配置说明

### 后端配置 (`backend/app/config.py`)

```python
DATABASE_URL = "sqlite:///./community_library.db"  # 数据库路径
SECRET_KEY = "your-secret-key"  # JWT 密钥
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # Token 有效期（分钟）
```

### 前端配置 (`frontend/vite.config.js`)

```javascript
server: {
  port: 5174,  // 开发服务器端口
  proxy: {
    '/api': 'http://localhost:8001'  # API 代理
  }
}
```

## 📝 开发说明

### 添加新接口

1. 在 `backend/app/routers/` 创建路由文件
2. 在 `backend/app/schemas/` 定义数据模式
3. 在 `backend/app/main.py` 注册路由

### 添加新页面

1. 在 `frontend/src/views/` 创建页面组件
2. 在 `frontend/src/api/` 添加 API 请求
3. 在 `frontend/src/router/index.js` 注册路由

## 📄 许可证

MIT License

## 👨‍💻 作者

- GitHub: [@koomorebi](https://github.com/koomorebi)

---

如有问题或建议，欢迎提交 Issue 或 Pull Request！
