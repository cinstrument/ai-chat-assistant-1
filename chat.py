# ！python3
# -*-coding:utf_8-*-
# @author CLQ
# @date 2026/5/17
# @file chat
import requests
import json

API_KEY = "你的API-Key"  # 把星号部分换成完整的
URL = "https://api.deepseek.com/v1/chat/completions"


def chat_with_ai(user_input):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个有帮助的AI助手，回答简洁准确。"},
            {"role": "user", "content": user_input}
        ],
        "stream": False
    }

    response = requests.post(URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"错误: {response.status_code} - {response.text}"


print("AI聊天助手启动！输入 'quit' 退出\n")
while True:
    user_input = input("你: ")
    if user_input.lower() == 'quit':
        print("再见！")
        break

    reply = chat_with_ai(user_input)
    print(f"AI: {reply}\n")