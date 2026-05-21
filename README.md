# IPTV 直播源自动测速整理服务

本服务自动从多个上游源采集 IPTV 直播地址，通过并发测速和媒体流完整性校验，过滤无效、低码率及广告源，并按央视、卫视、地方、体育、动漫等类别智能分类，最终输出标准 M3U 和 TXT 格式播放列表。

## 功能特点

- ✅ 多源采集（支持 M3U 和 TXT 格式）
- ✅ 并发测速（HTTP + ffprobe 深度校验）
- ✅ 广告源过滤
- ✅ 智能分类（基于名称正则）
- ✅ 单频道择优（每个频道最多保留3个最佳源）
- ✅ 双格式输出（TXT / M3U）
- ✅ 全自动定时运行（GitHub Actions，每天两次）
- ✅ 免费部署在 GitHub Pages

## 部署步骤

1. Fork 或克隆本仓库到你的 GitHub 账号
2. （可选）修改 `config.py` 中的上游源、分类规则等
3. 进入仓库 Settings → Pages，将 Source 设为 `Deploy from branch`，分支 `main`，目录 `/docs`
4. GitHub Actions 会自动运行，首次可手动触发（Actions → IPTV Speed Checker → Run workflow）
5. 等待运行完成后，通过以下地址访问：
   - M3U: `https://你的用户名.github.io/仓库名/output/iptv.m3u`
   - TXT: `https://你的用户名.github.io/仓库名/output/iptv.txt`
   - 网页入口: `https://你的用户名.github.io/仓库名/`

## 自定义配置

- 修改 `config.py` 中的 `SOURCE_URLS` 可以增减上游源
- 修改 `CLASSIFY_RULES` 可以调整分类规则
- 修改 `CHANNEL_NORMALIZATION` 可以合并同名频道
- 修改 `SPEED_CONFIG` 可调整测速超时和并发数

## 本地运行

```bash
git clone https://github.com/你的用户名/iptv-speed-checker.git
cd iptv-speed-checker
pip install -r requirements.txt
# 需要安装 ffmpeg (用于 ffprobe)
sudo apt install ffmpeg   # Ubuntu/Debian
# 或 brew install ffmpeg  # macOS
python main.py
