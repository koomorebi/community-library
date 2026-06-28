#!/bin/bash
# 社区图书馆借阅管理系统 - 一键启动

echo "📚 启动社区图书馆借阅管理系统..."

# 启动后端
echo "🔧 启动后端服务..."
cd backend
source venv/bin/activate
python run.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 3

# 启动前端
echo "🔧 启动前端服务..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ 启动完成！"
echo ""
echo "访问地址："
echo "  前端页面: http://localhost:5174"
echo "  API 文档: http://localhost:8001/docs"
echo "  默认账号: admin / admin123"
echo ""
echo "按 Ctrl+C 停止服务"

# 捕获退出信号
trap "echo ''; echo '🛑 停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit 0" INT TERM

# 等待
wait
