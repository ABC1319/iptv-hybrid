# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import time
from typing import List, Tuple, Optional

from config import SPEED_CONFIG, AD_BLOCK_KEYWORDS


class SpeedTester:
    def __init__(self):
        self.timeout = SPEED_CONFIG["timeout"]
        self.read_timeout = SPEED_CONFIG["read_timeout"]
        self.concurrent_tasks = SPEED_CONFIG["concurrent_tasks"]
    
    def is_ad_url(self, url: str) -> bool:
        """检测是否为广告源"""
        url_lower = url.lower()
        for keyword in AD_BLOCK_KEYWORDS:
            if keyword.lower() in url_lower:
                return True
        return False
    
    async def test_single(self, session: aiohttp.ClientSession, 
                          name: str, url: str) -> Optional[Tuple[str, str, float]]:
        """
        测试单个流地址
        返回: (频道名称, 流地址, 延迟) 或 None（无效/广告）
        """
        # 1. 广告过滤
        if self.is_ad_url(url):
            return None
        
        # 2. 测速验证
        start = time.time()
        try:
            timeout_config = aiohttp.ClientTimeout(
                total=10, 
                connect=self.timeout, 
                sock_read=self.read_timeout
            )
            async with session.get(url, timeout=timeout_config, allow_redirects=True) as resp:
                if resp.status != 200:
                    return None
                
                # 读取一小部分数据确认流可用（带超时保护）
                try:
                    await asyncio.wait_for(resp.content.read(1024 * 512), timeout=3)
                except asyncio.TimeoutError:
                    # 虽然超时但可能流是好的，继续保留
                    pass
                
                delay = time.time() - start
                # 只保留延迟小于 8 秒的源
                if delay < 8:
                    return (name, url, round(delay, 2))
        except Exception:
            pass
        
        return None
    
    async def test_all(self, channels: List[Tuple[str, str]]) -> List[Tuple[str, str, float]]:
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
