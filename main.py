from flow import create_gitchat_flow

def main():
    # 初始化数据
    shared = {
        "github_url": input("🚀 请输入GitHub项目URL: "),
        "project_name": "",
        "readme": "",
        "summary": "",
        "chat_context": "",
        "user_question": "",
        "ai_response": ""
    }
    
    # 运行流程
    create_gitchat_flow().run(shared)

if __name__ == "__main__":
    main()