# -*- coding: utf-8 -*-

import re
from typing import Dict, List, Tuple
from collections import defaultdict

from config import CLASSIFY_RULES, CHANNEL_NORMALIZATION


class Classifier:
    def __init__(self):
        self.rules = CLASSIFY_RULES
        self.normalization_rules = CHANNEL_NORMALIZATION
    
    def normalize_name(self, name: str) -> str:
        """应用归一化规则，获取标准频道名"""
        for pattern, normalized in self.normalization_rules.items():
            if re.search(pattern, name, re.IGNORECASE):
                return normalized
        return name
    
    def classify(self, channels: List[Tuple[str, str, float, int]]) -> Dict[str, List[Tuple[str, str, float, int]]]:
        """
        对频道进行分类，并执行单频道择优（每个标准频道最多保留3个最佳源）
        输入: [(频道名, url, 延迟, 码率), ...]
        返回: {分类名: [(频道名, url, 延迟, 码率), ...]}
        """
        # 1. 按归一化后的标准频道名分组
        groups: Dict[str, List[Tuple[str, str, float, int]]] = defaultdict(list)
        for name, url, delay, bitrate in channels:
            std_name = self.normalize_name(name)
            groups[std_name].append((name, url, delay, bitrate))
        
        # 2. 每组内按质量排序，择优保留最多3个
        final_channels = []
        for std_name, sources in groups.items():
            # 排序：延迟升序、码率降序
            sources.sort(key=lambda x: (x[2], -x[3]))
            best_sources = sources[:3]   # 每个频道最多3个源
            final_channels.extend(best_sources)
        
        # 3. 按分类规则分配到类别
        categorized = {cat: [] for cat in self.rules.keys()}
        categorized["其他"] = []
        
        for name, url, delay, bitrate in final_channels:
            name_lower = name.lower()
            matched = False
            for category, pattern in self.rules.items():
                if re.search(pattern, name_lower, re.IGNORECASE):
                    categorized[category].append((name, url, delay, bitrate))
                    matched = True
                    break
            if not matched:
                categorized["其他"].append((name, url, delay, bitrate))
        
        return categorized
