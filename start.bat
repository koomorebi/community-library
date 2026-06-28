@echo off
chcp 65001 >nul
echo 📚 启动社区图书馆借阅管理系统...

:: 启动后端
echo 🔧 启动后端服务...
cd backend
call venv\Scripts\activate.bat
start "后端服务" python run.py
cd ..

:: 等待后端启动
timeout /t 3 /nobreak >nul

:: 启动前端
echo 🔧 启动前端服务...
cd frontend
start "前端服务" npm run dev
cd ..

echo.
echo ✅ 启动完成！
echo.
echo 访问地址：
echo   前端页面: http://localhost:5174
echo   API 文档: http://localhost:8001/docs
echo   默认账号: admin / admin123
echo.
echo 关闭此窗口不会停止服务
echo 请手动关闭"后端服务"和"前端服务"窗口
pause
