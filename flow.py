from pocketflow import Flow
from nodes import GitHubFetchNode, SummaryNode, ChatNode

def create_gitchat_flow():
    """创建GitChat工作流"""
    # 创建节点
    fetch = GitHubFetchNode()
    summary = SummaryNode()
    chat = ChatNode()
    
    # 连接流程
    fetch >> summary >> chat  # 线性流程
    chat >> chat  # 对话循环
    
    return Flow(start=fetch)