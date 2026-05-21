# -*- coding: utf-8 -*-

from typing import Dict, List, Tuple
import datetime

from config import OUTPUT_TXT, OUTPUT_M3U


class OutputGenerator:
    """生成 TXT 和 M3U 格式的播放列表"""
    
    def generate(self, categorized: Dict[str, List[Tuple[str, str, float]]]):
        """生成所有格式的输出文件"""
        self.generate_txt(categorized)
        self.generate_m3u(categorized)
    
    def generate_txt(self, categorized: Dict[str, List[Tuple[str, str, float]]]):
        """生成 TXT 格式（播放器兼容）"""
        lines = []
        lines.append(f"# 更新时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        for category, channels in categorized.items():
            if not channels:
                continue
            lines.append(f"#----- {category}频道 ({len(channels)}个) -----")
            for name, url, delay in channels:
                lines.append(f"{name},{url}")
            lines.append("")
        
        with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def generate_m3u(self, categorized: Dict[str, List[Tuple[str, str, float]]]):
        """生成 M3U 格式（标准播放列表）"""
        lines = ["#EXTM3U"]
        lines.append(f"# 更新时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for category, channels in categorized.items():
            if not channels:
                continue
            lines.append(f"#----- {category}频道 ({len(channels)}个) -----")
            for name, url, delay in channels:
                # 标准 M3U 格式: #EXTINF:延迟,频道名称
                lines.append(f"#EXTINF:{delay},{name}")
                lines.append(url)
            lines.append("")
        
        with open(OUTPUT_M3U, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
