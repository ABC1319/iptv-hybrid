# -*- coding: utf-8 -*-

import re
import aiohttp
import asyncio
from typing import List, Tuple

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
                    # 提取频道名称: #EXTINF:-1 tvg-name="CCTV1" group-title="央视",CCTV-1
                    # 支持两种常见格式: 逗号后面的部分, 或者 tvg-name 属性
                    match = re.search(r',([^,]+)$', line)
                    if match:
                        current_title = match.group(1).strip()
                    else:
                        # 尝试提取 tvg-name
                        tvg_match = re.search(r'tvg-name="([^"]+)"', line)
                        if tvg_match:
                            current_title = tvg_match.group(1).strip()
                elif line and not line.startswith('#') and current_title:
                    # 流地址行
                    if line.startswith(('http://', 'https://')):
                        channels.append((current_title, line))
                    current_title = None
    except Exception as e:
        print(f"  [M3U] 采集失败 {url}: {e}")
    return channels


async def fetch_txt(session: aiohttp.ClientSession, url: str) -> List[Tuple[str, str]]:
    """
    解析 TXT 格式播放列表（每行格式: 频道名称,流地址 或 频道名称 流地址）
    """
    channels = []
    try:
        async with session.get(url, timeout=15) as resp:
            if resp.status != 200:
                return []
            content = await resp.text()
            for line in content.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # 尝试按逗号分割
                if ',' in line:
                    parts = line.split(',', 1)
                else:
                    # 尝试按空格分割
                    parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    name = parts[0].strip()
                    stream_url = parts[1].strip()
                    if stream_url.startswith(('http://', 'https://')):
                        channels.append((name, stream_url))
    except Exception as e:
        print(f"  [TXT] 采集失败 {url}: {e}")
    return channels


async def fetch_all_sources() -> List[Tuple[str, str]]:
    """
    采集所有上游源的频道，返回去重后的列表（基于 (名称, URL) 去重）
    """
    all_channels = []
    seen = set()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in SOURCE_URLS:
            # 根据扩展名判断格式
            if url.endswith('.m3u') or url.endswith('.m3u8'):
                tasks.append(fetch_m3u(session, url))
            elif url.endswith('.txt'):
                tasks.append(fetch_txt(session, url))
            else:
                # 无扩展名，尝试两种解析
                tasks.append(fetch_m3u(session, url))
                tasks.append(fetch_txt(session, url))
        
        results = await asyncio.gather(*tasks)
        
        for channels in results:
            for name, stream_url in channels:
                # 去除名称中的空白和特殊字符
                name = re.sub(r'\s+', ' ', name).strip()
                key = f"{name}|{stream_url}"
                if key not in seen:
                    seen.add(key)
                    all_channels.append((name, stream_url))
    
    return all_channels
