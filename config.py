# -*- coding: utf-8 -*-

# 上游 IPTV 源列表（M3U 或 TXT 格式）
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

# 分类规则（正则匹配，按顺序优先匹配）
CLASSIFY_RULES = {
    "央视": r"(cctv|cctv\d+|中央|央视|CCTV)",
    "卫视": r"(卫视|卫视综合|卫视高清|卫视HD|官方卫视|湖南卫视|浙江卫视|江苏卫视|东方卫视|北京卫视|..卫视)",
    "地方": r"(地方|本地|省|市|县|频道|上海|广东|北京|深圳|浙江|江苏|湖南|湖北|安徽|四川|重庆|山东|辽宁|..台)",
    "体育": r"(体育|sports|NBA|足球|篮球|体育赛事|五星体育|劲爆体育|体育频道)",
    "动漫": r"(动漫|动画|卡通|少儿|儿童|kids|CCTV-少儿|金鹰卡通|炫动卡通)",
    "影视": r"(电影|电视剧|影视频道|movie|CHC|家庭影院|影院频道|第一剧场)",
}

# 频道名称归一化映射（用于单频道择优）
# 格式：正则 -> 标准名称
CHANNEL_NORMALIZATION = {
    r"(cctv[-\s]?1|CCTV-?1综合|CCTV-?1|央视一套|中央一台)": "CCTV-1",
    r"(cctv[-\s]?2|CCTV-?2财经|CCTV-?2|央视二套)": "CCTV-2",
    r"(cctv[-\s]?3|CCTV-?3综艺|CCTV-?3|央视三套)": "CCTV-3",
    r"(cctv[-\s]?4|CCTV-?4国际|CCTV-?4|央视四套)": "CCTV-4",
    r"(cctv[-\s]?5|CCTV-?5体育|CCTV-?5|央视五套)": "CCTV-5",
    r"(cctv[-\s]?6|CCTV-?6电影|CCTV-?6|央视六套)": "CCTV-6",
    r"(cctv[-\s]?7|CCTV-?7军事|CCTV-?7|央视七套)": "CCTV-7",
    r"(cctv[-\s]?8|CCTV-?8电视剧|CCTV-?8|央视八套)": "CCTV-8",
    r"(cctv[-\s]?9|CCTV-?9纪录|CCTV-?9|央视九套)": "CCTV-9",
    r"(cctv[-\s]?10|CCTV-?10科教|CCTV-?10|央视十套)": "CCTV-10",
    r"(cctv[-\s]?11|CCTV-?11戏曲|CCTV-?11)": "CCTV-11",
    r"(cctv[-\s]?12|CCTV-?12社会与法|CCTV-?12)": "CCTV-12",
    r"(cctv[-\s]?13|CCTV-?13新闻|CCTV-?13)": "CCTV-13",
    r"(cctv[-\s]?14|CCTV-?14少儿|CCTV-?14)": "CCTV-14",
    r"(cctv[-\s]?15|CCTV-?15音乐|CCTV-?15)": "CCTV-15",
    r"(cctv[-\s]?16|CCTV-?16奥运|CCTV-?16)": "CCTV-16",
    r"(cctv[-\s]?17|CCTV-?17农业|CCTV-?17)": "CCTV-17",
    r"(湖南卫视|hunantv|hunan tv)": "湖南卫视",
    r"(浙江卫视|zhjiangtv|浙江卫视)": "浙江卫视",
    r"(江苏卫视|jiangsu tv)": "江苏卫视",
    r"(东方卫视|上海卫视|dragontv)": "东方卫视",
    r"(北京卫视|北京电视台|brtv)": "北京卫视",
}

# 输出目录和文件路径
OUTPUT_DIR = "output"
OUTPUT_TXT = "output/iptv.txt"
OUTPUT_M3U = "output/iptv.m3u"
