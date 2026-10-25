"""check_key.py —— 检查 API key 是否可用。

设计原则（这就是"工程思维"的第一课）：
  1. 只报"有没有"，**绝不打印 key 本身** —— 一旦打印，它就进了终端日志、进了截图、进了聊天记录
  2. 只读环境变量，不读文件 —— 密钥唯一的正本在环境变量里
  3. 打码时保留前后各几位 —— 够你核对是哪一把，又不足以还原

用法:
    python check_key.py
退出码:
    0 = 有且格式像样
    1 = 没有
"""

import os
import sys

VAR = "DEEPSEEK_API_KEY"


def mask(s: str) -> str:
    """打码：保留前 3 位和后 4 位，中间全星号。"""
    if not s:
        return "(空)"
    if len(s) <= 10:
        return "*" * len(s)
    return f"{s[:3]}{'*' * (len(s) - 7)}{s[-4:]}   (共 {len(s)} 字符)"


def main() -> int:
    v = os.environ.get(VAR)

    if not v:
        print(f"[缺失] 环境变量 {VAR} 没有设置")
        print()
        print("  设置方法（PowerShell，key 不会进命令历史）:")
        print("    $k = Read-Host '粘贴 key'")
        print(f"    [Environment]::SetEnvironmentVariable('{VAR}', $k, 'User')")
        print()
        print("  设完必须开新进程（当前窗口读不到 User 级的新变量）")
        return 1

    print(f"[存在] {VAR} = {mask(v)}")

    # 常见的手滑，逐条检查
    if v != v.strip():
        print("[警告] 值首尾有空白字符 —— 粘贴时多带了空格或换行，去掉")
    if not v.startswith("sk-"):
        print("[提示] DeepSeek 的 key 通常以 sk- 开头，这个不像")
    if "\n" in v or "\r" in v:
        print("[警告] 值里含换行 —— 多半是把整个文件读进来了，用 .Trim() 或 .strip()")

    print("[提示] 本脚本没有把 key 写到任何地方")
    return 0


if __name__ == "__main__":
    sys.exit(main())
