# -*- coding: utf-8 -*-

import asyncio
import sys
import time
from pathlib import Path

from config import OUTPUT_DIR
from collector import fetch_all_sources
from speed_tester import SpeedTester
from classifier import Classifier
from output_generator import OutputGenerator


async def main():
    """主流程：采集 → 测速 → 分类 → 输出"""
    
    # 1. 确保输出目录存在
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # 2. 采集所有上游源的频道
    print("[1/4] 正在采集上游源...")
    channels = await fetch_all_sources()
    print(f"  采集完成，共获取 {len(channels)} 个频道")
    
    # 3. 并发测速，过滤无效源
    print("[2/4] 正在并发测速验证...")
    tester = SpeedTester()
    valid_channels = await tester.test_all(channels)
    print(f"  测速完成，有效频道: {len(valid_channels)} 个")
    
    # 4. 智能分类
    print("[3/4] 正在智能分类...")
    classifier = Classifier()
    categorized = classifier.classify(valid_channels)
    for category, channels_list in categorized.items():
        print(f"  {category}: {len(channels_list)} 个")
    
    # 5. 生成输出文件（TXT 和 M3U）
    print("[4/4] 正在生成输出文件...")
    output_gen = OutputGenerator()
    output_gen.generate(categorized)
    print(f"  输出完成: {OUTPUT_DIR}/iptv.txt 和 {OUTPUT_DIR}/iptv.m3u")


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print(f"\n✅ 全部完成，耗时 {time.time() - start:.2f} 秒")
