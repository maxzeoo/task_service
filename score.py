#no_null 口径：双无 —— 地点和对象同时为"无"时判失败；只有一个为"无"仍算通过
import requests
import time
from pathlib import Path
import sys
import json

file_path = Path(__file__).resolve().parent / "golden.jsonl"
url="http://127.0.0.1:8000/tasks"

count=0
all_count=0

with open(file_path,encoding="utf-8") as f:
    for line in f:
        line =line .strip()
        if not line:
            continue
        d=json.loads(line)
        try:
            req=requests.post(url,json={"text":d["text"]},timeout=30)
            r=req.json()
        except requests.exceptions.ConnectionError:
            print("服务没起,先跑:python -m uvicorn main:app --port 8000")
            sys.exit(1)
        except ValueError:
            print("返回的不是json格式")
            continue

        tid =r['task_id']
        death=time.time()+60
        item={"status":"pending"}
        GET=f"http://127.0.0.1:8000/result/{tid}"
        exp=d["expect"]
        all_count+=1
        zero=0
        error=0

        while item.get("status")=="pending" and time.time()<death:
            respose = requests.get(GET)
            item=respose.json()
            time.sleep(2)
        if item["status"]=="done":
            tag="ok"
        elif item["status"]=="failed" and "错误原因" in item["error"]:
            tag="refuse"
        elif item["status"]=="failed"and "错误原因" not in item["error"]:
            tag="fail"
        else:
            tag="timeout"


        if "tasks" in r:
            for t in r["tasks"]:
                if  t["地点"]=="无" and t["对象"]=="无":
                    zero+=1
                if not set(t.keys())=={"顺序","地点","对象","内容"}:
                    error+=1

        if exp=="400":
            ok =(tag=="refuse")
        elif exp=="200":
            ok=(tag=="ok") and error==0     
        else:
            ok=(tag=="ok") and zero==0

        if tag=="timeout":
            y='timeout'
        if tag=='refuse':
            y='refuse'
        if tag=="fail":
            y='fail'
        if tag=='ok' and zero>0:
            y='no_null'
        if tag=='ok' and zero==0:
            y='200'

        if ok:
            count+=1
            print(f"{all_count} 通过 {exp}")
        else:
            print(f"{all_count} 不通过 expect={exp} 实际={y}")
    print(f"{count}/{all_count}")


        
        
