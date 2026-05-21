# -*- coding: utf-8 -*-

# 上游 IPTV 源列表（您提供的 6 个源已全部整合在此）
SOURCE_URLS = [
    "https://raw.githubusercontent.com/iptv-org/iptv/gh-pages/countries/cn.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cn.m3u",
    "https://raw.githubusercontent.com/suxuang/myIPTV/main/ipv4.m3u",
    "https://raw.githubusercontent.com/vbskycn/iptv/master/tv/iptv4.txt",
    "https://raw.githubusercontent.com/zzgpy1/Collect-IPTV/main/best_sorted.m3u",
    "https://raw.githubusercontent.com/dogwalkerg/IPTV-collect-tv-txt/main/others_output.txt",
]

# 测速配置
SPEED_CONFIG = {
    "timeout": 5,           # 连接超时（秒）
    "read_timeout": 8,      # 读取超时（秒）
    "max_redirects": 5,     # 最大重定向次数
    "concurrent_tasks": 20, # 并发测速数量
}

# 广告过滤关键词（域名/URL 关键词）
AD_BLOCK_KEYWORDS = [
    "ad.", "doubleclick", "googlesyndication", "adservice",
    "zjcdn", "advertisement", "exe", ".exe", "广告", "guanggao"
]

# 分类关键词映射（频道名称正则）
CLASSIFY_RULES = {
    "央视": r"cctv|cctv\d+",
    "卫视": r"(卫视|卫视综合|卫视高清|卫视HD|官方卫视)",
    "地方": r"地方|本地|省|市|县|频道",
    "体育": r"(体育|sports|NBA|足球|篮球|体育赛事)",
    "动漫": r"(动漫|动画|卡通|少儿|儿童|kids)",
    "影视": r"(电影|电视剧|影视频道|movie)",
}

# 输出文件路径
OUTPUT_DIR = "output"
OUTPUT_M3U = "output/iptv.m3u"
OUTPUT_TXT = "output/iptv.txt"
