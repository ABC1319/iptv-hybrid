# -*- coding: utf-8 -*-

import re
import time
from datetime import datetime
from typing import List, Tuple, Optional

# ---------- 日志工具（简单封装）----------
class Logger:
    """简单的控制台日志输出，带时间戳"""
    
    @staticmethod
    def info(msg: str):
        print(f"[INFO] {datetime.now().strftime('%H:%M:%S')} - {msg}")
    
    @staticmethod
    def warn(msg: str):
        print(f"[WARN] {datetime.now().strftime('%H:%M:%S')} - {msg}")
    
    @staticmethod
    def error(msg: str):
        print(f"[ERROR] {datetime.now().strftime('%H:%M:%S')} - {msg}")
    
    @staticmethod
    def debug(msg: str):
        # 调试模式，可设置环境变量 DEBUG=1 开启
        import os
        if os.environ.get("DEBUG") == "1":
            print(f"[DEBUG] {datetime.now().strftime('%H:%M:%S')} - {msg}")


logger = Logger()

# ---------- URL 清洗 ----------
def clean_url(url: str) -> str:
    """
    去除 URL 中的多余空白、换行符等
    """
    if not url:
        return ""
    url = url.strip()
    # 去除潜在的尾部垃圾字符
    url = url.split()[0]  # 取第一个 token
    # 确保协议是小写
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return ""

# ---------- 频道名称清洗 ----------
def clean_channel_name(name: str) -> str:
    """
    去除频道名称中的多余信息，例如：
    - 去除分辨率标识 (HD, SD, 1080p)
    - 去除无关符号
    """
    if not name:
        return "未知频道"
    # 移除括号内容（常见于备注）
    name = re.sub(r'\([^)]*\)', '', name)
    name = re.sub(r'\[[^\]]*\]', '', name)
    # 移除常见质量标签
    name = re.sub(r'\s*(HD|高清|超清|标清|1080p|720p|4K)\s*', '', name, flags=re.I)
    return name.strip()

# ---------- 延迟分级 ----------
def speed_grade(delay: float) -> str:
    """根据延迟返回等级标识"""
    if delay < 1.0:
        return "极快"
    elif delay < 2.0:
        return "快速"
    elif delay < 4.0:
        return "一般"
    else:
        return "较慢"

# ---------- 文件大小格式化 ----------
def format_size(size_bytes: int) -> str:
    """字节转可读格式"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}TB"

# ---------- 去重工具（基于名称+URL）----------
def deduplicate_channels(channels: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """
    对原始频道列表去重（在测速前使用）
    返回: 去重后的列表
    """
    seen = set()
    result = []
    for name, url in channels:
        key = (name, url)
        if key not in seen:
            seen.add(key)
            result.append((name, url))
    return result

# ---------- 统计信息 ----------
def stats_summary(categorized: dict) -> str:
    """生成分类统计摘要"""
    lines = []
    total = 0
    for cat, chs in categorized.items():
        cnt = len(chs)
        total += cnt
        lines.append(f"  {cat}: {cnt} 个")
    lines.append(f"  总计: {total} 个")
    return "\n".join(lines)

# ---------- 时间测量装饰器 ----------
def timer(func):
    """简单的函数执行时间测量装饰器"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{func.__name__} 耗时 {elapsed:.2f} 秒")
        return result
    return wrapper
