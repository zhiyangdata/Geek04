from smolagents import Tool
import csv
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class ReadCSVTool(Tool):
    name = "read_csv"
    description = """
    用于读取指定的 csv 文件"""
    inputs = {
        "file_path": {
            "type": "string",
            "description": "csv 文件的路径",
        }
    }
    output_type = "any"

    def forward(self, file_path: str) -> any:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        if not path.suffix.lower() == ".csv":
            raise ValueError(f"不是CSV文件: {file_path}")

        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

class WriteMDTool(Tool):
    name = "write_md"
    description = """
    用于写入指定的 md 文件中"""
    inputs = {
        "file_path": {
            "type": "string",
            "description": "md 文件的路径",
        },
        "content": {
            "type": "string",
            "description": "要写入的markdown内容",
        }
    }
    output_type = "string"

    def forward(self, file_path: str, content: str) -> str:
        path = Path(file_path)
        if path.suffix.lower() != ".md":
            raise ValueError(f"目标文件必须是.md后缀: {file_path}")

        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            f.write(content)
        return f"成功写入 {file_path}"

class BoChaWebSearch(Tool):
    name = "bocha_web_search"
    description = """
    用于根据搜索词调用Bocha Web Search API 进行联网搜索"""
    inputs = {
        "query": {
            "type": "string",
            "description": "要搜索的查询",
        }
    }
    output_type = "string"

    def forward(self, query: str) -> str:
        data = {
            "query":query,
            "summary":True,
            "count":10,
            "page":1
        }
        endpoint = "https://api.bochaai.com/v1/web-search"
        API_KEY = os.getenv("BOCHA_API_KEY")
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(endpoint, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        search_ret = response.json()
        return self.bocha_for_list(search_ret)

    def bocha_for_list(self, search_ret: dict):
        data = search_ret["data"]
        pages = data["webPages"]["value"]
        ret=[]
        for page in pages:
            ret.append({"title":page["name"],"summary":page["summary"],"url":page["url"]})
        return ret