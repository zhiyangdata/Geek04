import json
import os
from openai import OpenAI
from dotenv import load_dotenv
import subprocess
from utils import lined_print, framed_print
import sys

# 加载 .env 文件
load_dotenv()

client = OpenAI(
    api_key=os.getenv("MINIMAX_API_KEY"),  
    base_url="https://api.minimaxi.com/v1"
)

def send_messages(messages):
    response = client.chat.completions.create(
        model="MiniMax-M2.7",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        extra_body={"reasoning_split": True},
    )
    return response

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": "使用该工具执行Python代码",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python代码",
                    }
                },
                "required": ["code"]
            },
        }
    },
]

def execute_python(code: str) -> str:
    """执行Python代码并返回结果。"""
    try:
        print("##执行代码:\n",code)
        # 创建本地环境执行代码
        local_vars = {}
        exec(code, {}, local_vars)  # python可以动态 执行 代码
        result= local_vars.get('result', '执行成功')
        print("##执行结果:\n",result)
        return str(result)
    except Exception as e:
        return f"Error executing code: {str(e)}"

def agent_loop(messages):
    max_rounds = 20
    current_round = 0

    while True:
        current_round += 1
        lined_print(f"Calling LLM (round {current_round})")

        if current_round > max_rounds:
            print(f"Maximum rounds {max_rounds} reached, exiting")
            sys.exit(0)

        response = send_messages(messages)
        # 注意：以下基于 MiniMax API 的 reasoning_details 字段。若使用 Kimi 等其他模型，
        # reasoning 字段名和结构可能不同（例如 Kimi 使用字符串类型的 reasoning_content）。
        if response.choices[0].message.reasoning_details[0]['text'] != "":
            framed_print(f"Thinking", response.choices[0].message.reasoning_details[0]['text'], "info")

        if response.choices[0].message.content != "":
            framed_print(f"Answer", response.choices[0].message.content, "info")

        if response.choices[0].message.tool_calls != None:
            messages.append(response.choices[0].message)
            
            for tool_call in response.choices[0].message.tool_calls:
                if tool_call.function.name == "execute_python":
                    arguments_dict = json.loads(tool_call.function.arguments)
                    result = execute_python(arguments_dict['code'])
                    
                    messages.append({
                        "role": "tool",
                        "content": result,
                        "tool_call_id": tool_call.id
                    })
        else:
            break

if __name__ == "__main__":
    SYSTEM_MESSAGE = """
你是一个在 {os.getcwd()} 目录下的能够编写和执行代码的智能助手。当用户提出问题时，你需要：
1. 分析问题并确定需要编写什么代码
2. 编写能解决问题的Python代码
3. 使用execute_python工具执行代码
4. 分析执行结果，如果有错误则修改代码再次执行
5. 最终给用户提供答案

请确保你的代码能够正确执行并将最终结果存储在名为'result'的变量中。
    """
    history = [{"role": "system", "content": SYSTEM_MESSAGE}]
    while True:
        try:
            query = input("\033[36muser >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in ("q", "exit", ""):
            break
        history.append({"role": "user", "content": query})
        agent_loop(history)
        response_content = history[-1]["content"]
        print(response_content)
        print()
    
            