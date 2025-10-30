# -*- coding: utf-8 -*-

import os
from openai import OpenAI
# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Openai客户端，从环境变量中读取您的API Key
client = OpenAI(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    api_key="85f07a75-6d74-4c43-b3cf-f82a3a5024f1",
)
# Non-streaming:
print("----- image input request -----")
completion = client.chat.completions.create(
    # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
    model="doubao-seed-1-6-251015",
    # messages=[
    #     {
    #         "role": "user",
    #         "content": [
    #             {
    #                 "type": "image_url",
    #                 "image_url": {
    #                     "url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg"
    #                 },
    #             },
    #             {"type": "text", "text": "这是哪里？"},
    #         ],
    #     }
    # ],
    messages=[
        {"role": "user", "content": "我要研究深度思考模型与非深度思考模型区别的课题，体现出我的专业性"}
    ],
    reasoning_effort="medium"
)
if hasattr(completion.choices[0].message, 'reasoning_content'):
    print(completion.choices[0].message.reasoning_content)
print(completion.choices[0].message.content)

# Streaming:
print("----- streaming request -----")
stream = client.chat.completions.create(
    # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
    model="doubao-seed-1-6-251015",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg"
                    },
                },
                {"type": "text", "text": "这是哪里？"},
            ],
        }
    ],
    # 响应内容是否流式返回
    stream=True,
    reasoning_effort="medium"
)
reasoning_content = ""
content = ""
with stream:
    for chunk in stream:
        if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
            reasoning_content += chunk.choices[0].delta.reasoning_content
            print(chunk.choices[0].delta.reasoning_content, end="")
        delta_content = chunk.choices[0].delta.content
        if delta_content is not None:
            content += delta_content
            print(delta_content, end="")