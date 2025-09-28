# GitChat - GitHub项目智能对话工具

## 🎯 项目简介
GitChat 是一个简洁的CLI工具，帮助开发者快速理解GitHub开源项目。输入项目地址，自动获取README并生成摘要，支持基于项目内容的AI对话。

## ✨ 核心功能
- 📥 **自动获取**: 输入GitHub URL，自动抓取README.md
- 🤖 **智能摘要**: 使用ChatGPT生成项目概要和关键信息  
- 💬 **项目对话**: 基于项目内容与AI进行深度对话

## 🛠️ 预期技术栈
- **核心框架**: PocketFlow (轻量级LLM工作流)
- **AI模型**: DeepSeek API
- **HTTP请求**: requests  github API

### 核心灵感来源
- **[GitMCP](https://github.com/idosal/git-mcp)** - MCP协议的GitHub文档服务，提供了文档抓取和AI集成的核心思路
- **[PocketFlow](https://github.com/The-Pocket/PocketFlow)** -一个100行极简LLM框架。 

##项目结构：
gitchat/
├── main.py              # 程序入口
├── nodes.py             # 3个核心节点
├── flow.py              # 流程定义
├── utils.py             # 工具函数（GitHub API + LLM调用）
├── requirements.txt     # 依赖包

## 📝 项目流程图
3个核心节点：
GitHubFetchNode - 获取URL + 验证 + 抓取README
SummaryNode - 生成摘要 + 显示结果
ChatNode - 无限对话循环

    flowchart LR
    A[GitHubFetchNode] --> B[SummaryNode] 
    B --> C[ChatNode]
    C -->|循环| C
    

## 最终效果 （这是一个示例，你可以做的漂亮点以及增加报错输出）
你好开发者，请输入GitHub项目URL：
正在抓取README.md...
文档已抓取，正在生成摘要...
项目名称：[项目名称]
项目摘要：[项目摘要]
请输入你的问题：
[用户问题]
AI回答：[AI回答]


## 数据结构
shared = {
    "github_url": "",           # 用户输入
    "project_name": "",         # owner/repo 
    "readme": "",               # README原始内容
    "summary": "",              # AI生成的摘要
    "chat_context": "",         # 对话上下文
    "user_question": "",        # 用户问题
    "ai_response": ""           # AI回答
}

main.py -程序入口

from flow import create_gitchat_flow

def main():
    shared = {
        "github_url": "",
        "project_name": "",
        "readme": "",
        "summary": "",
        "chat_context": "",
        "user_question": "",
        "ai_response": ""
    }
    
    # 获取用户输入
    shared["github_url"] = input("请输入GitHub项目URL: ")
    
    # 运行流程
    flow = create_gitchat_flow()
    flow.run(shared)

if __name__ == "__main__":
    main()

nodes.py - 三个核心节点

from pocketflow import Node
from utils import fetch_github_readme, call_llm

class GitHubFetchNode(Node):
    # prep + exec + post

class SummaryNode(Node):
    # prep + exec + post

class ChatNode(Node):
    # prep + exec + post (处理循环)

flow.py - 流程连接

from pocketflow import Flow
from nodes import GitHubFetchNode, SummaryNode, ChatNode

def create_gitchat_flow():
    fetch = GitHubFetchNode()
    summary = SummaryNode()
    chat = ChatNode()
    
    fetch >> summary >> chat
    chat >> chat  # 循环
    
    return Flow(start=fetch)

utils.py - 工具函数
import requests

def fetch_github_readme(url):
    # GitHub API调用
    pass

def call_llm(prompt):
    # DeepSeek API调用  
    pass