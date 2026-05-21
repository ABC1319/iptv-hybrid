# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import time
import subprocess
import re
from typing import List, Tuple, Optional

from config import SPEED_CONFIG, AD_BLOCK_KEYWORDS


class SpeedTester:
    def __init__(self):
        self.timeout = SPEED_CONFIG["timeout"]
        self.read_timeout = SPEED_CONFIG["read_timeout"]
        self.concurrent_tasks = SPEED_CONFIG["concurrent_tasks"]
        self.has_ffprobe = self._check_ffprobe()
    
    def _check_ffprobe(self) -> bool:
        """检查系统中是否安装了 ffprobe"""
        try:
            subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            print("  警告: 未找到 ffprobe，将降级为轻量级 HTTP 测速")
            return False
    
    def is_ad_url(self, url: str) -> bool:
        """检测是否为广告源"""
        url_lower = url.lower()
        for keyword in AD_BLOCK_KEYWORDS:
            if keyword.lower() in url_lower:
                return True
        return False
    
    async def _lightweight_test(self, session: aiohttp.ClientSession, 
                                name: str, url: str) -> Optional[Tuple[str, str, float, int]]:
        """
        轻量级测速（仅HTTP探测，无码率）
        """
        start = time.time()
        try:
            timeout = aiohttp.ClientTimeout(total=8, connect=self.timeout)
            async with session.get(url, timeout=timeout, allow_redirects=True) as resp:
                if resp.status != 200:
                    return None
                # 检查Content-Type
                content_type = resp.headers.get('Content-Type', '')
                if 'video' not in content_type and 'application/vnd.apple.mpegurl' not in content_type:
                    return None
                # 尝试读取一小段数据
                try:
                    await asyncio.wait_for(resp.content.read(1024 * 256), timeout=3)
                except asyncio.TimeoutError:
                    pass
                delay = time.time() - start
                if delay < 8:
                    return (name, url, round(delay, 2), 0)  # 码率未知
        except Exception:
            pass
        return None
    
    async def _ffprobe_test(self, session: aiohttp.ClientSession,
                            name: str, url: str) -> Optional[Tuple[str, str, float, int]]:
        """
        使用 ffprobe 深度检测，返回 (名称, URL, 延迟, 码率kbps)
        """
        start = time.time()
        # 先做快速HTTP检查
        try:
            timeout = aiohttp.ClientTimeout(total=5, connect=self.timeout)
            async with session.head(url, timeout=timeout, allow_redirects=True) as resp:
                if resp.status != 200:
                    return None
                content_type = resp.headers.get('Content-Type', '')
                if 'video' not in content_type and 'application/vnd.apple.mpegurl' not in content_type:
                    return None
        except Exception:
            return None
        
        # 调用 ffprobe
        try:
            process = await asyncio.create_subprocess_exec(
                'ffprobe', '-v', 'error', '-show_entries',
                'format=bit_rate', '-of', 'default=noprint_wrappers=1:nokey=1',
                url,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=10)
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return None
            
            if process.returncode != 0:
                return None
            
            output = stdout.decode().strip()
            # 提取码率（单位 bps）
            bitrate_match = re.search(r'(\d+)', output)
            if bitrate_match:
                bitrate = int(bitrate_match.group(1)) // 1000  # 转为 kbps
            else:
                bitrate = 0
            
            # 只保留码率大于 500 kbps 的源
            if bitrate < 500:
                return None
            
            delay = time.time() - start
            if delay < 8:
                return (name, url, round(delay, 2), bitrate)
        except Exception:
            pass
        return None
    
    async def test_single(self, session: aiohttp.ClientSession,
                          name: str, url: str) -> Optional[Tuple[str, str, float, int]]:
        """测试单个流地址，优先使用 ffprobe，否则轻量级"""
        if self.is_ad_url(url):
            return None
        if not (url.startswith('http://') or url.startswith('https://')):
            return None
        
        if self.has_ffprobe:
            return await self._ffprobe_test(session, name, url)
        else:
            return await self._lightweight_test(session, name, url)
    
    async def test_all(self, channels: List[Tuple[str, str]]) -> List[Tuple[str, str, float, int]]:
        """并发测试所有频道"""
        valid = []
        semaphore = asyncio.Semaphore(self.concurrent_tasks)
        
        async def limited_test(session, name, url):
            async with semaphore:
                return await self.test_single(session, name, url)
        
        connector = aiohttp.TCPConnector(limit=self.concurrent_tasks, limit_per_host=5)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [limited_test(session, name, url) for name, url in channels]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result is not None:
                    valid.append(result)
        
        # 按延迟排序（快的在前）
        valid.sort(key=lambda x: x[2])
        return valid
