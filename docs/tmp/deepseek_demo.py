# -*- coding: utf-8 -*-

"""
descr: deepseek client
auther: lj.michale
create_date: 2025/10/23 15:54
file_name: deepseek_client.py
"""
from openai import OpenAI

client = OpenAI(
    api_key="sk-96a9d87ee9e04dfcbe85b89ac9312531",
    base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)