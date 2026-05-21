# IPTV 直播源自动测速整理服务

本服务自动从多个上游源采集 IPTV 直播地址，通过并发测速和媒体流完整性校验，过滤无效、低码率及广告源，并按央视、卫视、地方、体育、动漫等类别智能分类，最终输出标准 M3U 和 TXT 格式播放列表。

# IPTV Hybrid Builder

融合 [Guovin/iptv-api](https://github.com/Guovin/iptv-api) 与 [zilong7728/Collect-IPTV](https://github.com/zilong7728/Collect-IPTV) 的全自动 IPTV 播放列表生成方案。

## 功能特点

- **自动采集**：每6小时运行一次，获取 AI 优选直播源（Collect-IPTV）
- **智能聚合**：多源合并、去重、测速筛选、EPG 匹配（iptv-api）
- **一键部署**：仅需 GitHub Actions，无需服务器
- **结果直链**：最终播放列表位于 `output/result.m3u`

## 如何使用

1. **Fork 本仓库**（或按上述结构新建仓库）
2. **启用 GitHub Actions**：仓库 Settings → Actions → General → Allow all actions
3. **手动触发**：进入 Actions 选项卡，选择 "Hybrid IPTV Builder" → Run workflow
4. **获取播放地址**：
   - Raw 链接：`https://raw.githubusercontent.com/你的用户名/仓库名/main/output/result.m3u`
   - 若启用 Pages：`https://你的用户名.github.io/仓库名/result.m3u`

## 自定义频道列表

编辑 `config/demo.txt`，按行添加你想要的频道名。

## 更新频率

工作流默认每6小时运行一次。如需修改，编辑 `.github/workflows/hybrid.yml` 中的 `cron` 表达式。

## 故障排查

- 检查 Actions 运行日志，确认克隆和依赖安装成功。
- 若部分频道无结果，可调整 `config/alias.txt` 增加别名。
- 测速可能受 GitHub 网络影响，可关闭 `open_speed_test` 或调整超时参数。

## 致谢

- [Guovin/iptv-api](https://github.com/Guovin/iptv-api)
- [zilong7728/Collect-IPTV](https://github.com/zilong7728/Collect-IPTV)
