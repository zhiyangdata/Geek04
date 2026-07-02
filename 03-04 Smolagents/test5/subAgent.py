from smolagents import ToolCallingAgent, OpenAIModel
from dotenv import load_dotenv
import os
from tools import BoChaWebSearch

load_dotenv()

model = OpenAIModel(
    model_id="qwen3.7-max",
    api_key=os.getenv("ALI_API_KEY"),
    api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    extra_body={"enable_thinking":False},
)

web_search_agent = ToolCallingAgent(
    name = "web_search_agent",
    description = "可以根据用户的问题，进行联网搜索，返回搜索结果",
    tools=[BoChaWebSearch()],
    model=model, 
    max_steps=10
)
