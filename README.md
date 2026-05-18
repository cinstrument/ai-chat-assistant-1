```markdown
# AI 聊天助手

一个基于 DeepSeek API 的命令行 AI 聊天程序。

## 功能

- 调用 DeepSeek 大模型 API 进行智能对话
- 支持连续对话，上下文记忆
- 输入 `quit` 退出程序

## 技术栈

- Python 3.x
- DeepSeek API
- Requests 库

## 运行方法

1. **克隆项目**
   ```bash
   git clone https://github.com/cinstrument/ai-chat-assistant-1.git
   cd ai-chat-assistant-1
```

2. 安装依赖
   ```bash
   pip install requests
   ```
3. 配置 API Key
   · 在 DeepSeek 开放平台 注册并获取 API Key
   · 打开 chat.py，将 API_KEY 变量改为你的 Key
4. 运行程序
   ```bash
   python chat.py
   ```

使用示例

```
AI聊天助手启动！输入 'quit' 退出

你: 你好，请介绍一下自己
AI: 你好！我是 DeepSeek AI 助手...

你: Python 有什么优点？
AI: Python 语法简洁、生态丰富...

你: quit
再见！
```