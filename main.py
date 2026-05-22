import requests
import re
import time
from concurrent.futures import ThreadPoolExecutor
from urllib3.exceptions import InsecureRequestWarning

# 禁用SSL警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()

# ===================== 配置区 =====================
# 1. 采集源（整合zilong7728/Collect-IPTV 多平台源）
COLLECT_URLS = [
    "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/main/output/iptv.m3u",
    "https://raw.githubusercontent.com/Guovin/iptv-api/main/source/iptv.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cn.m3u",
]

# 2. 输出文件
OUTPUT_FILE = "iptv.m3u"
# 3. 并发校验线程数
MAX_WORKERS = 30
# 4. 校验超时时间（秒）
TIMEOUT = 5
# ===================================================

def get_urls_from_m3u(content):
    """解析m3u文件，提取频道名+播放地址"""
    lines = content.splitlines()
    result = []
    current_name = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 提取频道名称
        if line.startswith("#EXTINF"):
            name_match = re.search(r'tvg-name="([^"]+)"', line)
            if name_match:
                current_name = name_match.group(1)
            else:
                current_name = "未知频道"
        # 提取播放地址
        elif line.startswith("http"):
            result.append({"name": current_name, "url": line})
    
    return result

def check_url(item):
    """校验源是否可用（Guovin/iptv-api 校验逻辑）"""
    name = item["name"]
    url = item["url"]
    
    try:
        response = session.head(
            url,
            timeout=TIMEOUT,
            verify=False,
            allow_redirects=True
        )
        # 状态码200视为有效
        if response.status_code == 200:
            print(f"✅ 可用：{name}")
            return item
        else:
            print(f"❌ 失效：{name}")
            return None
    except:
        print(f"❌ 失效：{name}")
        return None

def collect_iptv():
    """采集所有IPTV源"""
    all_items = []
    print("🔍 开始采集IPTV源...")
    
    for url in COLLECT_URLS:
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                items = get_urls_from_m3u(resp.text)
                all_items.extend(items)
                print(f"✅ 采集成功：{url} | 数量：{len(items)}")
            else:
                print(f"❌ 采集失败：{url}")
        except Exception as e:
            print(f"❌ 采集异常：{url} | {str(e)}")
    
    # 去重（按播放地址）
    unique_dict = {item["url"]: item for item in all_items}
    unique_items = list(unique_dict.values())
    print(f"\n📊 采集完成：总源{len(all_items)}，去重后{len(unique_items)}")
    return unique_items

def filter_valid_iptv(items):
    """多线程校验有效源"""
    print("\n🚀 开始多线程校验源有效性...")
    valid_items = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = executor.map(check_url, items)
        for res in results:
            if res:
                valid_items.append(res)
    
    print(f"\n✅ 校验完成：有效源{len(valid_items)}个")
    return valid_items

def save_to_m3u(items):
    """保存为标准IPTV m3u文件"""
    header = """#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml"
"""
    content = header
    
    for item in items:
        content += f'#EXTINF:-1 tvg-name="{item["name"]}" ,{item["name"]}\n'
        content += f'{item["url"]}\n'
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"\n💾 已保存到：{OUTPUT_FILE}")

def main():
    # 1. 采集源
    items = collect_iptv()
    # 2. 校验有效源
    valid_items = filter_valid_iptv(items)
    # 3. 保存结果
    save_to_m3u(valid_items)
    print("\n🎉 全部任务完成！")

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"⏱ 总耗时：{round(end_time - start_time, 2)}秒")
