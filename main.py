import requests
import re
import json
import time
from concurrent.futures import ThreadPoolExecutor
from urllib3.exceptions import InsecureRequestWarning

# 全局配置
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()

# ===================== 配置区 =====================
# 采集源
COLLECT_URLS = [
    "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/main/output/iptv.m3u",
    "https://raw.githubusercontent.com/Guovin/iptv-api/main/source/iptv.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cn.m3u"
]

# 输出文件
OUTPUT_FILE = "iptv.m3u"
# 频道信息库
CHANNEL_DB_FILE = "channels.json"
# 并发&超时
MAX_WORKERS = 30
TIMEOUT = 5
# ===================================================

def load_channel_database():
    """加载频道信息库"""
    try:
        with open(CHANNEL_DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        channel_map = {}
        for category in data.values():
            for item in category:
                channel_map[item["raw_name"]] = item
        return channel_map
    except:
        return {}

def parse_m3u(content):
    """修复M3U解析，解决【未知频道】问题"""
    lines = content.splitlines()
    items = []
    current_name = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 解析频道名称（增强版）
        if line.startswith("#EXTINF"):
            # 方案1：提取 tvg-name
            tvg_match = re.search(r'tvg-name="([^"]+)"', line)
            # 方案2：提取逗号后名称
            name_match = re.search(r',([^,]+)$', line)
            
            if tvg_match:
                current_name = tvg_match.group(1).strip()
            elif name_match:
                current_name = name_match.group(1).strip()
            else:
                current_name = "未知频道"

        # 解析播放地址
        elif line.startswith(("http://", "https://", "rtp://", "rtsp://")):
            items.append({
                "name": current_name,
                "url": line
            })
    return items

def match_channel_info(item, channel_db):
    """自动匹配频道信息库"""
    origin_name = item["name"]
    url = item["url"]

    # 模糊匹配
    for key in channel_db:
        if key in origin_name:
            info = channel_db[key]
            return {
                "name": info["name"],
                "url": url,
                "logo": info.get("logo", ""),
                "tvg_id": info.get("tvg_id", key)
            }

    # 无匹配则使用原始名称
    return {
        "name": origin_name,
        "url": url,
        "logo": "",
        "tvg_id": origin_name
    }

def check_stream(item):
    """校验源是否有效"""
    try:
        res = session.head(
            item["url"],
            timeout=TIMEOUT,
            verify=False,
            allow_redirects=True
        )
        if res.status_code == 200:
            print(f"✅ 可用：{item['name']}")
            return item
        else:
            print(f"❌ 失效：{item['name']}")
            return None
    except:
        print(f"❌ 失效：{item['name']}")
        return None

def collect_streams():
    """采集所有源"""
    all_items = []
    channel_db = load_channel_database()

    for url in COLLECT_URLS:
        try:
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                items = parse_m3u(resp.text)
                all_items.extend(items)
                print(f"✅ 采集成功：{url} | 数量：{len(items)}")
        except Exception as e:
            print(f"❌ 采集失败：{url} | {str(e)}")

    # 去重
    unique_dict = {i["url"]: i for i in all_items}
    unique_items = list(unique_dict.values())
    print(f"\n📊 采集完成：去重后总计 {len(unique_items)} 个")
    
    # 匹配频道信息
    matched_items = [match_channel_info(i, channel_db) for i in unique_items]
    return matched_items

def save_playlist(items):
    """输出标准IPTV文件（带LOGO+EPG）"""
    header = """#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml"
"""
    content = header

    for item in items:
        tvg_id = f'tvg-id="{item["tvg_id"]}"' if item["tvg_id"] else ""
        tvg_logo = f'tvg-logo="{item["logo"]}"' if item["logo"] else ""

        content += f'#EXTINF:-1 {tvg_id} {tvg_logo},{item["name"]}\n'
        content += f'{item["url"]}\n'

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n💾 已保存：{OUTPUT_FILE}")

def main():
    start = time.time()
    print("🚀 开始采集IPTV源...")
    
    # 1. 采集+匹配频道
    items = collect_streams()
    # 2. 多线程校验
    print("\n🔍 开始校验源有效性...")
    with ThreadPoolExecutor(MAX_WORKERS) as executor:
        valid_items = list(filter(None, executor.map(check_stream, items)))
    # 3. 保存结果
    save_playlist(valid_items)
    
    print(f"\n🎉 全部完成！有效源：{len(valid_items)} 个")
    print(f"⏱ 总耗时：{round(time.time() - start, 2)} 秒")

if __name__ == "__main__":
    main()
