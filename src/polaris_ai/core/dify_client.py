# -*- coding: utf-8 -*-

"""
descr: Dify client客户端
auther: lj.michale
create_date: 2025/10/18 09:54
file_name: dify_client.py
"""
import requests
import os
import mimetypes
import json
from typing import Optional


class DifyClient:

    def __init__(self,
                 api_key: str,
                 base_url: str,
                 user_id: str):
        """
        初始化
        :param api_key:
        :param base_url:
        :param user_id:
        """
        self.api_key = api_key
        self.base_url = base_url
        self.user_id = user_id

    def upload_file(self, file_path: str) -> Optional[str]:
        """
        dify文件上传
        :param file_path:
        :return:
        """
        if not os.path.exists(file_path):
            print(f"[错误] 文件未找到: {file_path}")
            return None
        url = f"{self.base_url}/v1/files/upload"
        headers = { 'Authorization': f'Bearer {self.api_key}' }
        data = { 'user': self.user_id }
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        print(f"准备上传文件 '{os.path.basename(file_path)}' (类型: {mime_type}) 至 {url}...")
        try:
            with open(file_path, 'rb') as f:
                files = { 'file': (os.path.basename(file_path), f, mime_type) }
                resp = requests.post(url, headers=headers, data=data, files=files, timeout=30)
            if resp.status_code in (200, 201):
                body = resp.json()
                print("[成功] 文件上传成功!")
                print("服务器返回:", body)
                return body.get('id')
            print(f"[失败] 文件上传失败，状态码: {resp.status_code}")
            print("错误详情:", resp.text)
            return None
        except Exception as e:
            print(f"[错误] 上传请求异常: {e}")
            return None

    def send(self,
             query: str,
             conversation_id: Optional[str] = None,
             file_path: Optional[str] = None,
             language: Optional[str] = "中文") -> Optional[dict]:
        """
        发送
        :param query:
        :param conversation_id:
        :param file_path:
        :param language:
        :return:
        """
        file_id = None
        # 允许 file_path 传入已存在的 upload_file_id（UUID 形式），则不再上传
        def looks_like_uuid(value: str) -> bool:
            parts = value.split("-")
            return len(parts) == 5 and all(parts)
        if file_path:
            if os.path.exists(file_path):
                file_id = self.upload_file(file_path)
                if not file_id:
                    print("[错误] 文件上传失败，无法发送消息。")
                    return None
            elif looks_like_uuid(file_path):
                file_id = file_path
            else:
                print(f"[错误] 文件不存在，且不是有效的文件ID: {file_path}")
                return None
        elif conversation_id:
             # 无缓存模式：对话流若要求 upload，则必须显式传 --file（可为文件ID以避免重复上传）
             print("[错误] 该对话流需要提供文件，请在命令中使用 --file 传入本地文件或已上传文件ID(UUID)。")
             return None
        url = f"{self.base_url}/v1/chat-messages"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        inputs = {}
        if language:
            inputs["target_language"] = language
        if file_id:
            inputs["upload"] = {
                "type": "document",
                "transfer_method": "local_file",
                "upload_file_id": file_id
            }
            payload = {
                "inputs": inputs,
                "query": query,
                "response_mode": "blocking",
                "conversation_id": conversation_id or"",
                "user": self.user_id
            }
            print("准备执行对话流（继续会话或纯文本）..."if not file_id else f"准备执行对话流，文件ID: {file_id}")
            try:
                resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
                if resp.status_code in (200, 201):
                    body = resp.json()
                    print("[成功] 对话流执行成功!")
                    print("服务器返回:", body)
                    return body
                print(f"[失败] 对话流执行失败，状态码: {resp.status_code}")
                print("错误详情:", resp.text)
                return None
            except Exception as e:
                print(f"[错误] 对话请求异常: {e}")
                return None



