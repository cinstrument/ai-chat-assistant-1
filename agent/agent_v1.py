# ！python3
# -*-coding:utf_8-*-
# @author CLQ
# @date 2026/5/18
# @file agent_v1
import requests
import json
import re

API_KEY = "你的Key"
URL = "https://api.deepseek.com/v1/chat/completions"


def get_weather(city):
    """从 wttr.in 获取任意城市真实天气"""
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"{city}天气：{response.text.strip()}"
        else:
            return f"天气查询失败（{response.status_code}）"
    except Exception as e:
        return f"天气服务异常：{str(e)}"


def calculate(expr):
    try:
        expr = expr.replace("加", "+").replace("减", "-")
        expr = expr.replace("乘", "*").replace("除", "/")
        result = eval(expr)
        return str(result)
    except:
        return "计算失败，请检查表达式"


def chat_with_ai(message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": message}]
    }
    try:
        response = requests.post(URL, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"AI调用失败（{response.status_code}）"
    except Exception as e:
        return f"AI服务异常：{str(e)}"


def extract_city(text):
    """从用户输入中提取城市名"""
    if "天气" not in text:
        return None
    # 取“天气”前面的部分
    parts = text.split("天气")
    city = parts[0].strip()
    # 去掉常见的干扰词
    for word in ["查", "问", "下", "一下", "看看", "告诉我", "查一下", "查询"]:
        city = city.replace(word, "")
    city = city.strip()
    return city if city else None


def agent(user_input):
    # 1. 天气判断
    if "天气" in user_input:
        city = extract_city(user_input)
        if city:
            return get_weather(city)
        else:
            return "请告诉我城市名，比如「北京天气」或「东京天气」"

    # 2. 计算判断
    elif any(op in user_input for op in ["+", "-", "*", "/", "加", "减", "乘", "除"]):
        return calculate(user_input)

    # 3. 普通聊天
    else:
        return chat_with_ai(user_input)


if __name__ == "__main__":
    print("简易 Agent 启动！输入 'quit' 退出")
    while True:
        user = input("你：")
        if user.lower() == "quit":
            print("再见！")
            break
        response = agent(user)
        print(f"Agent：{response}\n")