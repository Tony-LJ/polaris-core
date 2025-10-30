# -*- coding: utf-8 -*-

"""
descr: Dify对话流API
auther: lj.michale
create_date: 2025/10/18 09:54
file_name: chatflow_api.py
"""
import requests
import os
import mimetypes
import json
from typing import Optional
import argparse


class DifyChatflowClient:
    """
    Dify对话流API
    """
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


if __name__ == '__main__':
    """
    python chatflow_api.py --query "请翻译文件" --lang "中文" --file "谷歌提示词.txt"
    python chatflow_api.py --query "请翻译的口语化一点" --lang "中文" --file b6a6b8cb-4059-4ded-92d3-1caa2f4cab6b --conv 7a2ccab4-4e6c-4493-b42a-ae36fe418206
    """
    parser = argparse.ArgumentParser(description="Dify 对话流CLI")
    parser.add_argument("--query", required=False, default="请翻译文件", help="要发送的消息内容")
    parser.add_argument("--lang", required=False, default="中文", help="目标语言，如 中文/English/日本語 等")
    parser.add_argument("--conv", required=False, default=None, help="已有的conversation_id，用于继续会话")
    parser.add_argument("--file", required=False, default=None, help="文件名/绝对路径，或已上传的文件ID(UUID)")
    args = parser.parse_args()

    # 直接明文写API Key（仅示例，生产环境建议用环境变量）
    DIFY_API_KEY = "你的API KEY"
    DIFY_BASE_URL = "http://127.0.0.1"
    USER_ID = "luojie"
    client = DifyChatflowClient(DIFY_API_KEY, DIFY_BASE_URL, USER_ID)
    # 解析文件参数：
    # - 若用户显式提供 --file，则优先使用（支持文件名/绝对路径/UUID）
    # - 若用户未提供 --file 且也未提供 --conv，则使用默认同目录下的 "谷歌提示词.txt"
    base_dir = os.path.dirname(__file__)
    file_path = None
    def _looks_like_uuid(value: str) -> bool:
        parts = value.split("-")
        return len(parts) == 5 and all(parts)
    if args.file:
        # 用户显式提供：若看起来像UUID则直传；否则按文件路径解析
        file_arg = args.file
        file_path = file_arg if _looks_like_uuid(file_arg) or os.path.isabs(file_arg) else os.path.join(base_dir, file_arg)
    elif not args.conv:
        # 首次便捷默认
        file_path = os.path.join(base_dir, "谷歌提示词.txt")

    # 发送
    resp = client.send(query=args.query, conversation_id=args.conv, file_path=file_path, language=args.lang)
    if resp and isinstance(resp, dict):
        conv = resp.get("conversation_id") or args.conv
        if conv:
            print(f"[信息] 会话ID: {conv}")
