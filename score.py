#no_null 口径：双无 —— 地点和对象同时为"无"时判失败；只有一个为"无"仍算通过
import requests
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

        code=req.status_code
        exp=d["expect"]
        all_count+=1
        zero=0
        error=0

        for t in r["tasks"]:
            if "无" in t["地点"] and "无" in t["对象"]:
                zero+=1
            if not set(t.keys())=={"顺序","地点","对象","内容"}:
                error+=1

        if exp=="400":
            ok =(code==400)
        elif exp=="200":
            ok=(code==200) and error==0     
        else:
            ok=(code==200) and zero==0

        if ok:
            count+=1
        else:
            print(f"第{all_count}条失败，期望：{exp}，实际：{code}")
    print(f"通过 {count}/{all_count}")


        
        
