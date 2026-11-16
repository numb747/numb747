<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/portrait-night.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/portrait-dusk.svg" />
  <img src="assets/portrait-dusk.svg" width="100%" alt="numb747 — pixel art: a young man with glasses, chin on his hand, watching a monitor; at night the screen light breathes, at dusk sunset light fills the room; dust drifts and he blinks now and then." />
</picture>

**AI 工具链 · 逆向工程 · Linux 折腾**

<br>

![Claude Code](https://img.shields.io/badge/Claude_Code-1a1b26?style=flat-square&logo=claude&logoColor=bb9af7)
![MCP](https://img.shields.io/badge/MCP-1a1b26?style=flat-square&logo=modelcontextprotocol&logoColor=bb9af7)
![Python](https://img.shields.io/badge/Python-1a1b26?style=flat-square&logo=python&logoColor=7aa2f7)
![TypeScript](https://img.shields.io/badge/TypeScript-1a1b26?style=flat-square&logo=typescript&logoColor=7aa2f7)
![Go](https://img.shields.io/badge/Go-1a1b26?style=flat-square&logo=go&logoColor=7aa2f7)
![Frida](https://img.shields.io/badge/Frida-1a1b26?style=flat-square&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjM3LjE1IC0yLjAgNDMuMCA0My4wIj48cGF0aCBmaWxsPSIjYmI5YWY3IiBkPSJNNTEuNCwzOUg0MS4zbDguNC0xMi45Yy00LjgtMi4zLTcuNC02LjUtNy40LTEyLjZDNDIuMyw0LjgsNDguMiwwLDU4LjUsMEg3NnYzOWgtOVYyOGgtOC41aC0wLjhMNTEuNCwzOXogTTY3LDIwVjdoLTguNWMtNC45LDAtNy43LDItNy43LDYuNGMwLDQuNSwyLjgsNi42LDcuNyw2LjZINjd6Ii8%2BPC9zdmc%2B)
![mitmproxy](https://img.shields.io/badge/mitmproxy-1a1b26?style=flat-square&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABgAAAAYBAMAAAASWSDLAAAAElBMVEW9vr%2Fb2dbp6ens6OPYg0jv7%2B6kN8aVAAAABnRSTlMLWJ7Hv9VQmfEmAAAAk0lEQVQY032QQQ6DMAwE16G9W9AHGEfcifkAlfwA1P8%2FprJD6Y0cEm%2B8mngD3K7Rqv3qKkA5VZHc5xSKsm0C52yUBlSmaAzQOFp30RvEGDTuVtrJFgamEMDTfQUKgz6q5l5Vl0toF5K2AyjBJJBVfuxDoPUI9IvzuWRCAwswGTBJzkveB%2B2uUf5BznDtimp1vv%2BYL5QwD8yDdnjOAAAAAElFTkSuQmCC)
![Arch](https://img.shields.io/badge/Arch_Linux-1a1b26?style=flat-square&logo=archlinux&logoColor=7dcfff)
![Hyprland](https://img.shields.io/badge/Hyprland-1a1b26?style=flat-square&logo=hyprland&logoColor=7dcfff)

</div>

<br>

## `$ whoami`

```
agents    MCP & Claude Code tooling: the model sees my proxy, debugger, sessions
智能体    MCP 与 Claude Code 工具链：让模型看见我看见的东西

reverse   VMP · signature reproduction · Android unpacking · protocol rebuilds
逆向      VMP 还原 · 签名算法复刻 · Android 加固脱壳 · 协议级复刻

network   NAT traversal and P2P hole punching, with measured numbers
网络      NAT 穿透与 UDP 打洞，数据都是实测

desktop   CachyOS + Hyprland, where the config is the documentation
桌面      CachyOS + Hyprland，配置即文档

method    AI does the legwork; the key step I verify by hand
做法      AI 跑腿，关键那一步我亲手验证
```

<br>

## `$ ls ~/works/ai`

**[mitmweb-mcp](https://github.com/numb747/mitmweb-mcp)** · `Python`<br>
An MCP server that reads the mitmweb session you already have open — one UI, shared by you and your AI.<br>
MCP server：让模型直接读你正在看的那个 mitmweb 会话 —— 一个 UI，你和 AI 共用。

**[ccmon](https://github.com/numb747/ccmon)** · `Python`<br>
Watch every Claude Code session on your machine from another device, as pixel Clawds. LAN-only, read-only, stdlib only.<br>
在另一台设备上看本机所有 Claude Code 会话，每个会话是一只像素 Clawd。只走局域网、只读、零依赖。

**[claude-discord-sync](https://github.com/Cnyn0403/claude-discord-sync/pulls?q=is%3Apr+author%3Anumb747)** · `TypeScript` · contributor<br>
Mirrors Claude Code sessions into Discord. 5 merged PRs upstream: zh-CN, Markdown rewriting, message order, permission prompts, console confirms.<br>
把 Claude Code 会话镜像到 Discord。向上游合入 5 个 PR：简体中文、Markdown 改写、消息顺序、权限提示、控制台确认。

<br>

## `$ ls ~/works/reverse`

**[uu-remote-study](https://github.com/numb747/uu-remote-study)** · `Go`<br>
How two devices behind NAT connect directly: UDP hole punching explained, implemented in Go, measured.<br>
NAT 后面的两台设备怎么直连：UDP 打洞原理、Go 实现、实测数据。

**[qq-music-api-Reverse](https://github.com/numb747/qq-music-api-Reverse)** · `JavaScript`<br>
QQ Music's web crypto chain rebuilt in Node: VMP lifted out of its sandbox, AES-GCM → SHA-1 → decrypt.<br>
QQ 音乐 web 版加密链路的 Node 复刻。把 VMP 引擎抽出沙箱，还原 AES-GCM → SHA-1 签名 → 解密全链。

**[qiyou-Reverse](https://github.com/numb747/qiyou-Reverse)** · `Frida`<br>
Reversing a packed Android APK: unpacking → decompile → native layer → crypto, plus a frida script set.<br>
Android 加固 APK 逆向方法论。动态脱壳 → 反编译 → Native 层 → 加密验证，配一套 frida 脚本。

**[cachyOS-config](https://github.com/numb747/cachyOS-config)** · `Shell`<br>
CachyOS + Hyprland desktop config. Idempotent installer + 10 docs on *why* each choice was made.<br>
CachyOS + Hyprland 桌面配置。幂等安装器，外加 10 篇记录「为什么这么选」的文档。

<br>

## `$ finger seven`

<div align="center">

[![Gmail](https://img.shields.io/badge/Gmail-cannonewhy123%40gmail.com-1a1b26?style=flat-square&logo=gmail&logoColor=7aa2f7&labelColor=1a1b26)](mailto:cannonewhy123@gmail.com)
[![Discord](https://img.shields.io/badge/Discord-numb1093-1a1b26?style=flat-square&logo=discord&logoColor=bb9af7&labelColor=1a1b26)](https://discord.com/users/1079010844505030707)

<sub>Happy to talk AI tooling, reverse engineering, or build something together. Gray-market / paid-content cracking requests — please don't.<br>聊 AI 工具链、聊逆向、一起做点东西都欢迎；灰产、破解付费内容之类的就别来了 🙏</sub>

</div>

<br>

## `$ stat`

<div align="center">

<p><img width="350" alt="top languages by repo" src="https://raw.githubusercontent.com/numb747/numb747/main/profile-summary-card-output/tokyonight/1-repos-per-language.svg" /><img width="350" alt="commits per hour" src="https://raw.githubusercontent.com/numb747/numb747/main/profile-summary-card-output/tokyonight/4-productive-time.svg" /></p>

<br>

<sub>7️⃣ Seven</sub>

![visitors](https://komarev.com/ghpvc/?username=numb747&style=flat-square&color=7aa2f7&label=visitors)

</div>
