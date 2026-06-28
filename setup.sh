#!/bin/bash
# 社区图书馆借阅管理系统 - 初始化脚本

echo "📚 社区图书馆借阅管理系统 - 初始化"
echo "=================================="

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未找到 Node.js，请先安装 Node.js 16+"
    exit 1
fi

# 初始化后端
echo ""
echo "🔧 初始化后端..."
cd backend

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "  创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境并安装依赖
echo "  安装 Python 依赖..."
source venv/bin/activate
pip install -r requirements.txt -q

# 初始化数据库
echo "  初始化数据库..."
python -c "
from app.database import engine, Base
from app.models import book, member, borrow, admin
Base.metadata.create_all(bind=engine)
print('  ✅ 数据库表创建完成')
"

# 生成示例数据
echo "  生成示例数据..."
python seed_data.py

cd ..

# 初始化前端
echo ""
echo "🔧 初始化前端..."
cd frontend

# 安装依赖
echo "  安装 Node 依赖..."
npm install -q

cd ..

echo ""
echo "✅ 初始化完成！"
echo ""
echo "启动方式："
echo "  方式一：使用启动脚本"
echo "    Linux/Mac: ./start.sh"
echo "    Windows:   start.bat"
echo ""
echo "  方式二：手动启动"
echo "    后端: cd backend && source venv/bin/activate && python run.py"
echo "    前端: cd frontend && npm run dev"
echo ""
echo "访问地址："
echo "  前端页面: http://localhost:5174"
echo "  API 文档: http://localhost:8001/docs"
echo "  默认账号: admin / admin123"
