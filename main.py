from fastapi import FastAPI
from fastapi.responses import JSONResponse
from step1_task_json import build_messages, check,ask,VAR
import os
from openai import OpenAI
import sys
from uuid import uuid4
from fastapi import FastAPI, BackgroundTasks, HTTPException

app=FastAPI()
key = os.environ.get(VAR)
if not key:
    print(f"[失败] 环境变量 {VAR} 没有设置")
    sys.exit(1)
client = OpenAI(api_key=key, base_url="https://api.deepseek.com", timeout=30)
results = {}



@app.get("/")
def read_root():
    return {"ok": True}

def run_task(task_id, text):
    try:
        raw = ask(client, build_messages(text))
        back = check(raw)
        results[task_id] = {"task_id": task_id, "status": "done", "tasks": back["tasks"]}
    except Exception as e:
        results[task_id] = {"task_id": task_id, "status": "failed", "error": e.args[0]}

@app.post("/tasks")
def make_tasks(body:dict,background: BackgroundTasks):
    if "text" not in body:
        return JSONResponse(status_code=400,content={"error": "KeyError","detail":"缺少text"})
    t=body["text"]
    if not isinstance(t,str) or not t.strip():
        return JSONResponse(status_code=400, content={"error": "ValueError", "detail": "text 不能为空"})
    tid = uuid4().hex[:8]
    results[tid] = {"task_id": tid, "status": "pending"}
    background.add_task(run_task, tid, t)
    return JSONResponse(status_code=202, content={"task_id": tid, "status": "pending"})
    # try:
    #     raw=ask(client, build_messages(t))
    #     back=check(raw)
        
    # except Exception as e:
    #     return JSONResponse(status_code=400, content={"error": type(e).__name__,"detail":str(e).strip("'")})
    # return back

@app.get("/result/{task_id}")
def get_result(task_id: str):
    item = results.get(task_id)
    if item is None:
        raise HTTPException(status_code=404, detail="task not found")
    return item