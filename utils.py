import requests
import os
from dotenv import load_dotenv
import re

# 加载环境变量
load_dotenv()

def fetch_github_readme(url):
    """
    获取GitHub仓库的README内容
    输入: https://github.com/owner/repo
    输出: {"owner": "owner", "repo": "repo", "readme": "内容"}
    """
    # 解析URL提取owner和repo
    pattern = r'https://github\.com/([^/]+)/([^/]+)'
    match = re.match(pattern, url.strip())
    
    if not match:
        raise ValueError("无效的GitHub URL格式")
    
    owner, repo = match.groups()
    
    # 调用GitHub API
    api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitChat/1.0"
    }
    
    # 如果有GitHub token，添加认证
    github_token = os.getenv('GITHUB_TOKEN')
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()  # 抛出HTTP错误
    
    # 解码base64内容
    import base64
    content = base64.b64decode(response.json()['content']).decode('utf-8')
    
    return {
        "owner": owner,
        "repo": repo,
        "project_name": f"{owner}/{repo}",
        "readme": content
    }

def call_llm(prompt):
    """
    调用DeepSeek API
    输入: prompt字符串
    输出: AI回答字符串
    """
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        raise ValueError("请设置DEEPSEEK_API_KEY环境变量")
    
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    return response.json()['choices'][0]['message']['content']

# 测试函数
if __name__ == "__main__":
    # 测试GitHub API
    try:
        result = fetch_github_readme("https://github.com/microsoft/vscode")
        print(f"项目: {result['project_name']}")
        print(f"README长度: {len(result['readme'])}")
    except Exception as e:
        print(f"GitHub API测试失败: {e}")
    
    # 测试LLM API
    try:
        response = call_llm("你好，请简单介绍一下自己")
        print(f"LLM回答: {response}")
    except Exception as e:
        print(f"LLM API测试失败: {e}")