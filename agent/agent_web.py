# ！python3
# -*-coding:utf_8-*-
# @author CLQ
# @date 2026/5/18
# @file agent_web
import streamlit as st
import requests
import json
import time

# ===== 配置 =====
API_KEY = ""  # 本地运行时填你的真实Key
URL = "https:sk-3e5ec4aebc96//api.deepseek.com/v1/chat/completions"

# ===== 天气（带重试）=====
def get_weather(city):
    """稳定版天气：完全可控的模拟数据，永不失败"""
    # 你可以随时修改这里的天气数据
    weather_db = {
        "北京": "晴 ☀️ 24°C",
        "上海": "多云 ⛅ 26°C",
        "西安": "阴 ☁️ 22°C",
        "南京": "晴 ☀️ 25°C",
        "广州": "多云 ⛅ 28°C",
        "深圳": "晴 ☀️ 29°C",
        "成都": "阴 ☁️ 21°C",
        "杭州": "晴 ☀️ 23°C",
    }

    # 如果城市在数据库里，返回对应天气；否则返回默认
    if city in weather_db:
        return f"{city}：{weather_db[city]}"
    else:
        return f"{city}：晴 🌤️ 23°C"

# ===== 计算 =====
def calculate(expr):
    try:
        expr = expr.replace("加", "+").replace("减", "-")
        expr = expr.replace("乘", "*").replace("除", "/")
        return str(eval(expr))
    except:
        return "计算失败"

# ===== AI对话（带重试 + 限流处理）=====
def chat_with_ai(message):
    if not API_KEY:
        return "请先在代码中配置 API Key（本地运行）"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": message}]
    }

    for i in range(2):
        try:
            resp = requests.post(URL, headers=headers, json=data, timeout=15)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            if resp.status_code == 429:
                time.sleep(2)
                continue
            return f"AI调用失败（{resp.status_code}）"
        except requests.exceptions.Timeout:
            if i == 0:
                time.sleep(1)
                continue
            return "AI思考超时，请简化问题"
        except Exception:
            return "AI服务异常"
    return "多次失败，请稍后再试"

# ===== 路由：天气 / 计算 / AI =====
def agent(user_input):
    if "天气" in user_input:
        city = user_input.split("天气")[0].strip()
        if not city:
            city = "北京"
        return get_weather(city)
    elif any(op in user_input for op in ["+", "-", "*", "/", "加", "减", "乘", "除"]):
        return calculate(user_input)
    else:
        return chat_with_ai(user_input)

# ===== Streamlit UI =====
st.set_page_config(page_title="我的AI助手", page_icon="🤖")
st.title("🤖 我的AI智能助手")
st.markdown("我能查天气、做计算、陪你聊天～")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("输入你的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = agent(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})