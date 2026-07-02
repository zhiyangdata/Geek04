from smolagents import CodeAgent, WebSearchTool, OpenAIModel
from dotenv import load_dotenv
import os

load_dotenv()

model = OpenAIModel(
    model_id="qwen3.7-max",
    api_key=os.getenv("ALI_API_KEY"),
    api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
agent = CodeAgent(tools=[], model=model, stream_outputs=False)

agent.run("计算1+2+3...+100的和")