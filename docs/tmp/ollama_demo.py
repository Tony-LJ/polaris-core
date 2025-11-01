# -*- coding: utf-8 -*-
import ollama

# 创建 Ollama 客户端
client = ollama.Client(host="http://localhost:11434")

# 获取模型列表
models = client.list()

for model in models.models:
    print(f"模型名称: {model.model}")
    print(f"模型详情:{client.show(model.model)}")

# 获取正在运行的模型
ps = client.ps()

for model in ps.models:
    print(f"正在运行的模型名称: {model.model}")
    print(f"正在运行的模型详情:{client.show(model.model)}")

# 对话
while True:
    prompt = input("请输入对话内容：")
    resp = client.chat(
        model="deepseek-r1:1.5b",
        messages=[{"role":"user","content":prompt}]
    )
    print(resp["message"]["content"])