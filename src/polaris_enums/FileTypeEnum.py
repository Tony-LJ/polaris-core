# -*- coding: utf-8 -*-
"""
descr : 文件类型枚举
auther : zengsg
create_date : 2025/10/20 14:40
file_name : FileTypeEnum.py
"""
from enum import Enum, unique
from typing import Dict, Optional


@unique  # 确保枚举值唯一
class FileTypeEnum(Enum):
    """文件类型枚举（按内容分类）"""
    TEXT = "text"  # 文本文件
    IMAGE = "image"  # 图像文件
    AUDIO = "audio"  # 音频文件
    VIDEO = "video"  # 视频文件
    DOCUMENT = "document"  # 文档文件（如PDF、Word）
    ARCHIVE = "archive"  # 压缩包文件
    OTHER = "other"  # 其他类型


@unique
class FileExtEnum(Enum):
    """文件扩展名枚举（映射常见扩展名与类型）"""
    # 文本文件
    TXT = (".txt", FileTypeEnum.TEXT, "text/plain")
    CSV = (".csv", FileTypeEnum.TEXT, "text/csv")
    MD = (".md", FileTypeEnum.TEXT, "text/markdown")

    # 图像文件
    PNG = (".png", FileTypeEnum.IMAGE, "image/png")
    JPG = (".jpg", FileTypeEnum.IMAGE, "image/jpeg")
    JPEG = (".jpeg", FileTypeEnum.IMAGE, "image/jpeg")
    GIF = (".gif", FileTypeEnum.IMAGE, "image/gif")
    SVG = (".svg", FileTypeEnum.IMAGE, "image/svg+xml")

    # 音频文件
    MP3 = (".mp3", FileTypeEnum.AUDIO, "audio/mpeg")
    WAV = (".wav", FileTypeEnum.AUDIO, "audio/wav")
    M4A = (".m4a", FileTypeEnum.AUDIO, "audio/mp4")

    # 视频文件
    MP4 = (".mp4", FileTypeEnum.VIDEO, "video/mp4")
    AVI = (".avi", FileTypeEnum.VIDEO, "video/x-msvideo")
    MOV = (".mov", FileTypeEnum.VIDEO, "video/quicktime")

    # 文档文件
    PDF = (".pdf", FileTypeEnum.DOCUMENT, "application/pdf")
    DOC = (".doc", FileTypeEnum.DOCUMENT, "application/msword")
    DOCX = (".docx", FileTypeEnum.DOCUMENT, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    XLS = (".xls", FileTypeEnum.DOCUMENT, "application/vnd.ms-excel")
    XLSX = (".xlsx", FileTypeEnum.DOCUMENT, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # 压缩包文件
    ZIP = (".zip", FileTypeEnum.ARCHIVE, "application/zip")
    RAR = (".rar", FileTypeEnum.ARCHIVE, "application/vnd.rar")
    TAR = (".tar", FileTypeEnum.ARCHIVE, "application/x-tar")
    GZ = (".gz", FileTypeEnum.ARCHIVE, "application/gzip")

    def __init__(self, ext: str, file_type: FileTypeEnum, mime_type: str):
        self.ext = ext  # 扩展名（带点，如".txt"）
        self.file_type = file_type  # 文件类型（关联FileTypeEnum）
        self.mime_type = mime_type  # MIME类型（用于HTTP传输等场景）

    @classmethod
    def get_by_ext(cls, ext: str) -> Optional["FileExtEnum"]:
        """根据扩展名（如".txt"）获取枚举实例"""
        ext = ext.lower()  # 忽略大小写
        for item in cls:
            if item.ext == ext:
                return item
        return None

    @classmethod
    def get_mime_type(cls, ext: str) -> str:
        """根据扩展名获取MIME类型，未知类型返回默认值"""
        file_enum = cls.get_by_ext(ext)
        return file_enum.mime_type if file_enum else "application/octet-stream"


@unique
class FileModeEnum(Enum):
    """文件操作模式枚举（规范文件打开模式）"""
    READ_TEXT = "r"  # 读取文本（默认编码）
    READ_BINARY = "rb"  # 读取二进制
    WRITE_TEXT = "w"  # 写入文本（覆盖）
    WRITE_BINARY = "wb"  # 写入二进制（覆盖）
    APPEND_TEXT = "a"  # 追加文本
    APPEND_BINARY = "ab"  # 追加二进制
    READ_WRITE_TEXT = "r+"  # 读写文本（不覆盖）
    READ_WRITE_BINARY = "rb+"  # 读写二进制（不覆盖）

# if __name__ == '__main__':
#     # 1. 获取文件类型信息
#     ext = ".png"
#     file_enum = FileExtEnum.get_by_ext(ext)
#     if file_enum:
#         print(f"扩展名 {ext} 属于 {file_enum.file_type.value} 类型，MIME类型为 {file_enum.mime_type}")
#         # 输出：扩展名 .png 属于 image 类型，MIME类型为 image/png
#
#     # 2. 获取未知扩展名的MIME类型
#     print(FileExtEnum.get_mime_type(".unknown"))  # 输出：application/octet-stream
#
#     # 3. 使用文件操作模式
#     with open("test.txt", FileModeEnum.WRITE_TEXT.value, encoding="utf-8") as f:
#         f.write("枚举模式更安全")