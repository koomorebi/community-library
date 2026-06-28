@echo off
chcp 65001 >nul
echo 📚 社区图书馆借阅管理系统 - 初始化
echo ==================================

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

:: 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Node.js，请先安装 Node.js 16+
    pause
    exit /b 1
)

:: 初始化后端
echo.
echo 🔧 初始化后端...
cd backend

:: 创建虚拟环境
if not exist "venv" (
    echo   创建虚拟环境...
    python -m venv venv
)

:: 激活虚拟环境并安装依赖
echo   安装 Python 依赖...
call venv\Scripts\activate.bat
pip install -r requirements.txt -q

:: 初始化数据库
echo   初始化数据库...
python -c "from app.database import engine, Base; from app.models import book, member, borrow, admin; Base.metadata.create_all(bind=engine); print('  ✅ 数据库表创建完成')"

:: 生成示例数据
echo   生成示例数据...
python seed_data.py

cd ..

:: 初始化前端
echo.
echo 🔧 初始化前端...
cd frontend

:: 安装依赖
echo   安装 Node 依赖...
npm install -q

cd ..

echo.
echo ✅ 初始化完成！
echo.
echo 启动方式：
echo   方式一：使用启动脚本
echo     start.bat
echo.
echo   方式二：手动启动
echo     后端: cd backend ^& venv\Scripts\activate ^& python run.py
echo     前端: cd frontend ^& npm run dev
echo.
echo 访问地址：
echo   前端页面: http://localhost:5174
echo   API 文档: http://localhost:8001/docs
echo   默认账号: admin / admin123
pause
