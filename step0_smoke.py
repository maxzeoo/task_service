"""step0_smoke.py —— 唯一目标：确认"能用代码调通 API"。

这一步不产生任何"作品"。它只排除环境问题：
装包、网络、key、模型名，任何一样不通，后面全是空转。

key 从环境变量读，绝不写死在文件里。
"""

import os
import sys

VAR = "DEEPSEEK_API_KEY"

key = os.environ.get(VAR)
if not key:
    print(f"[失败] 环境变量 {VAR} 没有设置")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("[失败] openai 没装：python -m pip install openai")
    sys.exit(1)

client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

try:
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "只回两个字：通了"}],
        timeout=30,
    )
except Exception as e:
    # 只打印异常类型和消息，绝不打印 key
    print(f"[失败] 调用出错：{type(e).__name__}: {e}")
    sys.exit(2)

print("[成功] 模型回：", resp.choices[0].message.content)
print("[信息] 本次用量：", resp.usage)
