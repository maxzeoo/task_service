# task_service

# python 安装代码
```
# 安装 fastapi uvicorn
.\.venv\Scripts\python.exe -m pip install fastapi uvicorn
# 检验版本
.\.venv\Scripts\python.exe -c "import fastapi, uvicorn; print('fastapi', fastapi.__version__); print('uvicorn', uvicorn.__version__)"
# 期望相似输出
fastapi 0.162.0
uvicorn 0.54.0
```
# 启动
```
# 以特定端口打开main.py
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
# 期望相似输出
INFO:     Started server process [21456]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

# 检验
```
# 另开窗口输入
curl.exe http://127.0.0.1:8000
# 期望相似输出
{"ok":true}
# 第一个窗口输出
INFO:     127.0.0.1:59059 - "GET / HTTP/1.1" 200 OK
```

# 停止服务
```
# 在第一个窗口按 CTRL+c，输出
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [36364]
```
