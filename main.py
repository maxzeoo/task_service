from fastapi import FastAPI
from fastapi.responses import JSONResponse
from step1_task_json import build_messages, check,ask,VAR
import os
from openai import OpenAI
import sys

app=FastAPI()
key = os.environ.get(VAR)
if not key:
    print(f"[失败] 环境变量 {VAR} 没有设置")
    sys.exit(1)
client = OpenAI(api_key=key, base_url="https://api.deepseek.com", timeout=30)



@app.get("/")
def read_root():
    return {"ok": True}

@app.post("/tasks")
def make_tasks(body:dict):
    if "text" not in body:
        return JSONResponse(status_code=400,content={"error": "KeyError","detail":"缺少text"})
    t=body["text"]
    if not isinstance(t,str) or not t.strip():
        return JSONResponse(status_code=400, content={"error": "ValueError", "detail": "text 不能为空"})
    try:
        raw=ask(client, build_messages(t))
        back=check(raw)
        
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": type(e).__name__,"detail":str(e)})
    return back