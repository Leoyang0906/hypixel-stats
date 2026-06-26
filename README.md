# hypixel-stats

这是一个用于显示 Hypixel Bedwars 数据的简易桌面 HUD（基于 tkinter）。我在 opt/hypixel-hud 分支中对原代码做了以下改进：

改动摘要
- 把对 Mojang API 的 eval 替换为安全的 json 解析（apitools.py）。
- 将 Hypixel / Mojang 请求移到后台线程池，避免阻塞 tkinter 主循环（bedwarsinfo.py）。
- 从环境变量 HYPIXEL_API_KEY 读取 Hypixel API Key（不在仓库中保存密钥）。
- 增加错误处理（玩家不存在、网络错误、API 错误提示）。
- 添加 config.example.json 示例并在 README 中说明如何配置。

如何使用
1. 在本地设置环境变量 HYPIXEL_API_KEY：

   - Linux / macOS (bash):
     export HYPIXEL_API_KEY=your_api_key_here

   - Windows (PowerShell):
     $env:HYPIXEL_API_KEY = "your_api_key_here"

   或者把密钥放到 config.json（但不要提交到仓库）。

2. 可选：设置刷新间隔（秒），默认 2 秒：
   - 使用环境变量 HS_REFRESH，例如：
     export HS_REFRESH=5

3. 运行脚本：
   python3 bedwarsinfo.py

快捷键
- 按 Ctrl+/ 开始录入玩家名，输入完成后按 Enter 开始获取并显示数据。

注意与速率限制
- 脚本在 AUTO_REFRESH 模式下会每 HS_REFRESH 秒自动刷新当前玩家的数据。请注意 Hypixel API 的速率限制，过低的刷新间隔可能导致被限流或封禁。建议把刷新间隔设为 5 秒或更高以降低风险。

安全
- 不要把你的 API Key 提交到公共仓库。使用环境变量或本地 config.json 存放密钥。

开发者说明
- 我在分支 `opt/hypixel-hud` 中做了修改并将提交放到该分支。请检查并在合并前确认你自己的 API key 管理方式。
