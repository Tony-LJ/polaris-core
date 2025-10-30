# -*- coding: utf-8 -*-

"""
descr: doubao client
auther: lj.michale
create_date: 2025/10/23 15:54
file_name: doubao_client.py
"""
from openai import OpenAI


class DoubaoClient:
    """
    豆包客户端
    """
    def __init__(self,base_url="https://ark.cn-beijing.volces.com/api/v3",api_key="85f07a75-6d74-4c43-b3cf-f82a3a5024f1"):
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
                   model_name="doubao-seed-1-6-251015",
                   reasoning_effort="medium",
                   messages=[{"role": "user", "content": "景旺电子2025年经营分析"}]):
        """
        模型调用
        :param model_name: doubao-seed-1-6-251015
        :param reasoning_effort: medium
        :param messages: [{"role": "user", "content": "景旺电子2025年经营分析"}]
        :return:
        """
        client = self._create_client()
        completion = client.chat.completions.create(
            model = model_name,
            messages = messages,
            reasoning_effort = reasoning_effort
        )

        return completion.choices[0].message.content


if __name__ == '__main__':
    doubao = DoubaoClient()
    print(doubao.call_model())






































