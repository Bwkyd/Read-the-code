from pocketflow import Node
from utils import fetch_github_readme, call_llm

class GitHubFetchNode(Node):
    """获取GitHub README"""
    
    def prep(self, shared):
        return shared["github_url"]
    
    def exec(self, github_url):
        print("🔄 正在抓取README.md...")
        return fetch_github_readme(github_url)
    
    def post(self, shared, prep_res, exec_res):
        shared["project_name"] = exec_res["project_name"]
        shared["readme"] = exec_res["readme"]
        print(f"✅ 已获取项目: {shared['project_name']}")

class SummaryNode(Node):
    """生成项目摘要"""
    
    def prep(self, shared):
        return {
            "project_name": shared["project_name"],
            "readme": shared["readme"]
        }
    
    def exec(self, data):
        print("🤖 正在生成摘要...")
        prompt = f"""
请为以下GitHub项目生成简洁的中文摘要：

项目名称：{data['project_name']}
README内容：
{data['readme'][:3000]}  

请按以下格式输出：
项目简介：[一句话介绍]
主要功能：[核心功能列表]
技术栈：[使用的技术]
适用场景：[适合什么人使用]
"""
        return call_llm(prompt)
    
    def post(self, shared, prep_res, exec_res):
        shared["summary"] = exec_res
        print(f"\n📋 项目摘要：")
        print(exec_res)
        print("\n" + "="*50 + "\n")

class ChatNode(Node):
    """对话循环节点"""
    
    def prep(self, shared):
        # 获取用户问题
        question = input("💬 请输入你的问题（输入'退出'结束对话）：")
        shared["user_question"] = question
        
        return {
            "question": question,
            "project_name": shared["project_name"],
            "readme": shared["readme"],
            "summary": shared["summary"],
            "chat_context": shared.get("chat_context", "")
        }
    
    def exec(self, data):
        if data["question"].lower() in ["退出", "exit", "quit", "q"]:
            return "QUIT"
        
        prompt = f"""
你是一个GitHub项目分析助手。基于以下项目信息回答用户问题：

项目：{data['project_name']}
摘要：{data['summary']}
README：{data['readme'][:2000]}

历史对话：{data['chat_context']}

用户问题：{data['question']}

请用中文简洁回答：
"""
        return call_llm(prompt)
    
    def post(self, shared, prep_res, exec_res):
        if exec_res == "QUIT":
            print("👋 再见！")
            return "end"  # 结束流程
        
        shared["ai_response"] = exec_res
        print(f"\n🤖 AI回答：{exec_res}\n")
        
        # 更新对话历史
        chat_history = shared.get("chat_context", "")
        chat_history += f"\n用户：{shared['user_question']}\nAI：{exec_res}\n"
        shared["chat_context"] = chat_history[-1000:]  # 保留最近1000字符
        
        return "default"  # 继续循环