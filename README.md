# task_service
需要 Python 3.11+，以下命令都在本项目根目录（含 main.py 的目录）执行


## 本地运行（三步）
```
#前提：Python 3.11+，首次 clone 后先建环境（下面命令都在项目根目录执行）
python -m venv .venv
# 安装依赖
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# 设置key，这是临时设置，只对当前窗口有效；不要写进任何文件，也不要提交。
$env:DEEPSEEK_API_KEY = "sk-换成你自己的key"
# 以特定端口打开main.py
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
# 期望相似输出
INFO:     Started server process [21456]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## 检验
```
# 另开窗口输入
curl.exe http://127.0.0.1:8000
# 期望相似输出
{"ok":true}
# 第一个窗口输出
INFO:     127.0.0.1:59059 - "GET / HTTP/1.1" 200 OK
```

## 停止服务
```
# 在第一个窗口按 CTRL+c，输出
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [36364]
```

## 已知局限
- golden #4「去机房看一下热不热」单条实测 6/6 被拒；当前成绩是 9/10，不是 10/10
- 「口语化指代」的口径未定；扩到 50 条时单列一类，暂不并入主集