from smolagents import CodeAgent, OpenAIModel
from tools import ReadCSVTool, WriteMDTool
from dotenv import load_dotenv
import os

load_dotenv()

model = OpenAIModel(
    model_id="qwen3.7-max",
    api_key=os.getenv("ALI_API_KEY"),
    api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
agent = CodeAgent(tools=[ReadCSVTool(), WriteMDTool()], model=model, stream_outputs=False)

agent.run("针对D:\workspace\python\smol-test\yanjing_beer_daily_k_20250518_20260518.csv中的数据展开走势分析，并输出一份markdown格式的分析报告，写入到当前目录的report.md文件中")