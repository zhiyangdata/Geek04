from smolagents import CodeAgent, OpenAIModel
from tools import ReadCSVTool, WriteMDTool
from subAgent import web_search_agent
from dotenv import load_dotenv
import os

load_dotenv()

model = OpenAIModel(
    model_id="qwen3.7-max",
    api_key=os.getenv("ALI_API_KEY"),
    api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
agent = CodeAgent(
    tools=[ReadCSVTool(), WriteMDTool()], 
    model=model, 
    stream_outputs=False,
    managed_agents=[web_search_agent]
)

prompt = """
#角色设定：你是一位专业的金融数据分析师。
#任务目标：请结合本地数据与最新网络资讯，对“燕京啤酒”进行全面的行情与基本面分析，并生成一份 Markdown 格式的投资分析报告。
#具体执行步骤：
1. 本地数据走势分析：
  - 读取并分析文件 D:\workspace\python\smol-test\yanjing_beer_daily_k_20250518_20260518.csv。
  - 提取关键指标（如开盘价、收盘价、最高/最低价、成交量等），分析近一年的股价整体走势、波动特征及关键时间节点。
2. 联网搜索与资讯挖掘：
  - 搜索燕京啤酒近期的财经新闻、公司公告及研报。
  - 重点梳理近期的利好因素（如业绩预增、新品发布、机构评级等）与潜在风险（如市场竞争、资金流向、原材料成本等）。
3. 综合分析与总结：
  - 将本地技术面数据与网络基本面消息相结合，进行交叉验证与统一分析。
  - 给出客观的总结性观点。
4. 输出报告：
  - 整合以上所有分析内容整合成一份结构清晰、排版美观的 Markdown 报告。
  - 将报告内容完整写入当前工作目录下的 report.md 文件中。
"""
agent.run(prompt)
