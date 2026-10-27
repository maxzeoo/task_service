"""step1_task_json.py —— 一句话 → 结构化任务 JSON。"""
import json
import os
import sys
import re

from openai import OpenAI

VAR = "DEEPSEEK_API_KEY"
MODEL = "deepseek-chat"
ACTIONS=["查看","检查","读取","看","测量","记录","拍照","拍摄","录像","探测","开启","关闭","启动","停止","重启","复位","调整","设置","配置","连接","断开","清理","维护","修复","更换","升级","下载","上传"]
INPUT = "去机房检查三号机柜的温度，然后到配电室看电压表"
TEXT="""我给你一个任务，你拆解并设计一个详细可执行且含有tasks的方案，
例如：{"tasks":[{"顺序": 1, "地点": "检查地点", "对象": "要检查的物品", "内容": "关闭进水阀门"},{"顺序": 2, "地点": "检查地点", "对象": "要检查的物品", "内容": "读取水表读数"}]}。
其中每一步只准以顺序，地点，对象，内容这四个键名输出，“内容”必须以白名单的某个动词开头，不许使用白名单以外的动词。
如果地点，对象，内容这几个有一个及以上指令没有或者模糊不定，无法精准定位到具体内容（比如"那个地方"，"那个设备"无法精确到具体的无可争议的那个实物或者地点，而机房、配电室这类楼宇内房间级名称即算明确地点，不需要精确到机柜编号），直接输出{"refuse": "具体原因"}，但是如果是"对象"这个键，虽未写全称或未指明，但能唯一确定且争议不大，例如“室内温度”“电压表读数”“水表读数”可以接受。
或者命令前后矛盾，前后要求截然相反，或者顺序不定，一会儿这个先，一会儿那个先的，直接输出{"refuse": "具体原因"}。
不准反问，只输出合法 JSON：双引号、花括号、逗号；不要 markdown 围栏、不要任何解释,动作只准从这几个里选：__动作__"""


def build_messages(text: str) -> list[dict]:
    messages=[{"role":"system","content":TEXT.replace("__动作__", "、".join(ACTIONS))},
              {"role": "user", "content": text}]
    return messages


def ask(client, messages) -> str:
    """T1：发一次，只返回模型的**原始文本**。不许在这里做任何清洗。"""
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        timeout=30,
        #检测是否支持json
        response_format={"type":"json_object"},
        temperature=0
    )
    return resp.choices[0].message.content


def check(raw: str) -> dict:
    orig=raw
    try:
        raw =raw.strip()
        i=raw.find("{")
        j=raw.rfind("}")
        raw=raw[i:j+1]
        d=json.loads(raw)
    #检查 JSON 格式是否正确
    except json.JSONDecodeError:
        print(orig)
        raise KeyError('不是json格式')
    if 'tasks'  in d:
        if not isinstance(d['tasks'],list) :
            raise ValueError('tasks不是列表')
    #空列表也不行（空列表算成功的话 80% 能刷到 100%）
        if not d['tasks']:
            raise ValueError('tasks是空列表')
        for key , row in enumerate(d['tasks'],start=1):
            if not isinstance(row,dict):
                raise ValueError('每一条不是字典')
            if set(row)!={"顺序","地点","对象","内容"}:
                raise KeyError("缺失键值")
            if not isinstance(row["顺序"],int):
                raise ValueError(f'顺序值不正确：{row["顺序"]}')
            if not row["内容"].startswith(tuple(ACTIONS)):
                raise ValueError(f"内容值不正确：{row['内容']},必须以白名单的某个动词:{', '.join(ACTIONS[:3])}开头")
    elif 'refuse' in d:
        raise KeyError(f'错误原因：{d['refuse']}')
    else:
        raise KeyError(f'模型给的是{list(d)}')
    return d


def selftest():
    count=0
    good = """ ```json
    {"tasks":[{"顺序":1,"地点":"a","对象":"b","内容":"查看c"}]}
      ```"""
    try:
        check(good)
        count+=1
        print("没报错")
    except Exception as e:
        print("报错了：", type(e).__name__, e)

    good1 = """{"tasks":[{"顺序":1,"地点":"a","对象":"b","内容":"查看c"}]}"""
    try:
        check(good1)
        count+=1
        print("没报错")
    except Exception as e:
        print("报错了：", type(e).__name__, e)

    bad="""{"task":[{"顺序":"1"}]}"""
    try:
        check(bad)
        print("bad:没报错")
    except Exception as e:
        print("报错了：", type(e).__name__, e)
        count+=1
    
    bad1="""{"tasks":[]}"""
    try:
        check(bad1)
        print("bad1:没报错")      
    except Exception as e:
        print("报错了：", type(e).__name__, e)
        count+=1

    bad2="""{"tasks":[{"顺序":"1","地点":"a","对象":"b","内容":"c"}]}"""
    try:
        check(bad2)
        print("bad2:没报错")
    except Exception as e:
        print("报错了：", type(e).__name__, e)
        count+=1

    bad3="""{"tasks":[{"顺序":"1","地点":"a"}]}"""
    try:
        check(bad3)
        print("bad3:没报错")
    except Exception as e:
        print("报错了：", type(e).__name__, e)
        count+=1

    bad4="""{"tasks":[{"顺序":1,"地点":"a","对象":"b","内容":"捣鼓c"}]}"""
    try:
        check(bad4)
        print("bad4:没报错")
    except Exception as e:
        print("报错了：", type(e).__name__, e)
        count+=1

    return count

def main() -> int:
    key = os.environ.get(VAR)
    if not key:
        print(f"[失败] 环境变量 {VAR} 没有设置")
        return 1
    client = OpenAI(api_key=key, base_url="https://api.deepseek.com", timeout=30)
    raw = ask(client, build_messages(INPUT))
    print("--- raw ---")
    print(raw)              # 这行是我加的验收要求，不是卡的
    print("--- parsed ---")
    print(json.dumps(check(raw), ensure_ascii=False, indent=2))
    print("--- selftest ---")
    count=selftest()
    print(f"selftest:{count}/7")
    if count<7:
        return 2

    return 0

if __name__ == "__main__":
    sys.exit(main())