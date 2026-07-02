from smolagents import ToolCallingAgent, OpenAIModel
from dotenv import load_dotenv
import os

load_dotenv()

model = OpenAIModel(
    model_id="qwen3.7-max",
    api_key=os.getenv("ALI_API_KEY"),
    api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    extra_body={"enable_thinking":False},
)
agent = ToolCallingAgent(tools=[], model=model, max_steps=10)

agent.run("搜索一下关于燕京啤酒近三个月的相关财经新闻")