# -*- coding: utf-8 -*-

import re
from typing import Dict, List, Tuple

from config import CLASSIFY_RULES


class Classifier:
    def __init__(self):
        self.rules = CLASSIFY_RULES
    
    def classify(self, channels: List[Tuple[str, str, float]]) -> Dict[str, List[Tuple[str, str, float]]]:
        """
        对频道进行分类
        返回: {分类名: [(频道名, 流地址, 延迟), ...]}
        """
        categorized = {category: [] for category in self.rules.keys()}
        categorized["其他"] = []
        
        for name, url, delay in channels:
            name_lower = name.lower()
            matched = False
            
            for category, pattern in self.rules.items():
                if re.search(pattern, name_lower, re.IGNORECASE):
                    categorized[category].append((name, url, delay))
                    matched = True
                    break
            
            if not matched:
                categorized["其他"].append((name, url, delay))
        
        return categorized
