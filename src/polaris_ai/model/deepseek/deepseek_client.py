# -*- coding: utf-8 -*-

"""
descr: deepseek client
auther: lj.michale
create_date: 2025/10/23 15:54
file_name: deepseek_client.py
"""
from openai import OpenAI


class DeepseekClient:
    """
    Deepseek客户端
    """
    def __init__(self,base_url="https://api.deepseek.com",api_key="sk-96a9d87ee9e04dfcbe85b89ac9312531"):
        """
         初始化
        :param base_url:
        :param api_key:
        """
        self.base_url = base_url
        self.api_key = api_key

    def _create_client(self):
        """
        创建client实例
        :return:
        """
        client = OpenAI(
            base_url = self.base_url,
            api_key = self.api_key,
        )

        return client

    def call_model(self,
                   model_name="deepseek-chat",
                   messages=[{"role": "system", "content": "You are a helpful assistant"},{"role": "user", "content": "Hello"}]):
        """
        模型调用
        :param model_name: doubao-seed-1-6-251015
        :param reasoning_effort: medium
        :param messages: [{"role": "user", "content": "2024中国经济分析"}]
        :return:
        """
        client = self._create_client()
        completion = client.chat.completions.create(
            model = model_name,
            stream=False,
            messages = messages
        )

        return completion.choices[0].message.content


if __name__ == '__main__':
    deepseek_client = DeepseekClient()
    print(deepseek_client.call_model())

