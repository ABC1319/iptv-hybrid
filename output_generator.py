# -*- coding: utf-8 -*-

import datetime
from typing import Dict, List, Tuple

from config import OUTPUT_TXT, OUTPUT_M3U


class OutputGenerator:
    """生成 TXT 和 M3U 格式的播放列表"""
    
    def generate(self, categorized: Dict[str, List[Tuple[str, str, float, int]]]):
        """生成所有格式的输出文件"""
        self.generate_txt(categorized)
        self.generate_m3u(categorized)
    
    def generate_txt(self, categorized: Dict[str, List[Tuple[str, str, float, int]]]):
        """生成 TXT 格式（频道名,URL）"""
        lines = []
        lines.append(f"# 更新时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("# 格式: 频道名称,流地址")
        lines.append("")
        
        for category, channels in categorized.items():
            if not channels:
                continue
            lines.append(f"#----- {category}频道 ({len(channels)}个) -----")
            for name, url, delay, bitrate in channels:
                # TXT 格式保持简洁
                lines.append(f"{name},{url}")
            lines.append("")
        
        with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def generate_m3u(self, categorized: Dict[str, List[Tuple[str, str, float, int]]]):
        """生成增强型 M3U 格式，包含分组、延迟、码率信息"""
        lines = ["#EXTM3U"]
        lines.append(f"# 更新时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("# 每个频道的延迟和码率信息已附在 #EXTINF 行\n")
        
        # 分组映射（确保英文分组名，部分播放器需要）
        group_map = {
            "央视": "央视",
            "卫视": "卫视",
            "地方": "地方",
            "体育": "体育",
            "动漫": "少儿",
            "影视": "影视",
            "其他": "其他"
        }
        
        for category, channels in categorized.items():
            if not channels:
                continue
            group_title = group_map.get(category, category)
            for name, url, delay, bitrate in channels:
                # 构建扩展信息：显示延迟和码率
                info = f"{name} [延迟:{delay}s"
                if bitrate > 0:
                    info += f" 码率:{bitrate}kbps"
                info += "]"
                lines.append(f'#EXTINF:-1 tvg-id="" tvg-name="{name}" tvg-logo="" group-title="{group_title}",{info}')
                lines.append(url)
            lines.append("")  # 分类间空行
        
        with open(OUTPUT_M3U, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
