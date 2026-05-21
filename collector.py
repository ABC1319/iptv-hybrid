# -*- coding: utf-8 -*-

import re
import aiohttp
import asyncio
from typing import List, Tuple
from urllib.parse import urlparse

from config import SOURCE_URLS

async def fetch_m3u(session: aiohttp.ClientSession, url: str) -> List[Tuple[str, str]]:
    """
    解析 M3U 格式播放列表
    返回: [(频道名称, 流地址), ...]
    """
    channels = []
    try:
        async with session.get(url, timeout=15) as resp:
            if resp.status != 200:
                return []
            content = await resp.text()
            lines = content.split('\n')
            current_title = None
            for line in lines:
                line = line.strip()
                if line.startswith('#EXTINF:'):
                    # 提取频道名称: #EXTINF:-1,CCTV-1 综合
                    match = re.search(r',([^,]+)$', line)
                    if match:
                        current_title = match.group(1).strip()
                elif line and not line.startswith('#'):
                    # 流地址行
                    if current_title and (line.startswith('http://') or line.startswith('https://')):
                        channels.append((current_title, line))
                    current_title = None
    except Exception as e:
        print(f"  [M3U] 采集失败 {url}: {e}")
    return channels

async def fetch_txt(session: aiohttp.ClientSession, url: str) -> List[Tuple[str, str]]:
    """
    解析 TXT 格式播放列表（每行格式: 频道名称,流地址）
    """
    channels = []
    try:
        async with session.get(url, timeout=15) as resp:
            if resp.status != 200:
                return []
            content = await resp.text()
            for line in content.split('\n'):
                line = line.strip()
                if ',' in line and not line.startswith('#'):
                    parts = line.split(',', 1)
                    name = parts[0].strip()
                    stream_url = parts[1].strip()
                    if stream_url.startswith('http'):
                        channels.append((name, stream_url))
    except Exception as e:
        print(f"  [TXT] 采集失败 {url}: {e}")
    return channels

async def fetch_all_sources() -> List[Tuple[str, str]]:
    """
    采集所有上游源的频道
    去重：基于 (频道名称, 流地址) 的去重逻辑
    """
    all_channels = []
    seen = set()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in SOURCE_URLS:
            if url.endswith('.m3u') or url.endswith('.m3u8'):
                tasks.append(fetch_m3u(session, url))
            elif url.endswith('.txt'):
                tasks.append(fetch_txt(session, url))
            else:
                # 尝试两种格式
                tasks.append(fetch_m3u(session, url))
                tasks.append(fetch_txt(session, url))
        
        results = await asyncio.gather(*tasks)
        
        for channels in results:
            for name, stream_url in channels:
                key = f"{name}|{stream_url}"
                if key not in seen:
                    seen.add(key)
                    all_channels.append((name, stream_url))
    
    return all_channels
