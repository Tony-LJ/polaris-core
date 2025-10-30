# -*- coding: utf-8 -*-
import requests

from polaris_message.massage_push_bot import WechatBot
from openai import OpenAI

webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
bot = WechatBot(webhook_url)

# 初始化Openai客户端，从环境变量中读取您的API Key;请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="85f07a75-6d74-4c43-b3cf-f82a3a5024f1",
)

# Non-streaming:
print("----- image input request -----")
completion = client.chat.completions.create(
    # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
    model="doubao-seed-1-6-251015",
    messages=[
        {"role": "user", "content": "SQL开窗函数介绍"}
    ],
    reasoning_effort="medium"
)

if hasattr(completion.choices[0].message, 'reasoning_content'):
    print(completion.choices[0].message.reasoning_content)
print(completion.choices[0].message.content)

# generated_text = completion.choices[0].message.content.strip()
# print(generated_text)
# headers = { 'Content-Type': 'application/json' }
# data = { "msgtype": "markdown", "markdown": { "content": generated_text } }

# response = requests.post(webhook_url, json=data, headers=headers)
# print("Response from WeChat Work Bot:", response.text)

bot.send_text(content=completion.choices[0].message.content, mentioned_list=["@all"])






