#!/usr/bin/env python3
"""生成 GitHub Social preview 图（1280×640，Tokyo Night）。

文字在左，视觉在右。右侧两种来源：
  - 图像派生 ASCII：复用 ~/cachyOS-config/wallpaper/tokyonight/_ascii.py 的
    采样与调色板吸附，渲进右侧区域后用横向渐变遮罩淡出与文字的交界。
  - 手写 ASCII 示意图：线条细的源图在这个分辨率下会退化成噪点，直接画更清楚。

用法：python3 social-card.py            # 生成全部
      python3 social-card.py mitmweb-mcp
"""
import importlib.util
import os
import subprocess
import sys
import html

ASCII_PY = os.path.expanduser(
    "~/cachyOS-config/wallpaper/tokyonight/_ascii.py")
POOL = os.path.expanduser("~/Pictures/Wallpapers/tokyonight")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "social")

spec = importlib.util.spec_from_file_location("_ascii", ASCII_PY)
assert spec and spec.loader, f"读不到 {ASCII_PY}"
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)

W, H = 1280, 640
BG = "#1a1b26"
MONO_FONT = "MesloLGS Nerd Font Mono, Sarasa Mono SC"

# Tokyo Night
FG = "#c0caf5"
BLUE = "#7aa2f7"
PURPLE = "#bb9af7"
MUTED = "#565f89"
DIM = "#a9b1d6"


def crop_ratio(path, ratio):
    """居中裁成指定宽高比，避免强制 resize 把画面压扁。"""
    out = subprocess.run(["magick", "identify", "-format", "%w %h", path],
                         capture_output=True, check=True).stdout.split()
    w, h = int(out[0]), int(out[1])
    if w / h > ratio:
        cw, ch = int(h * ratio), h
    else:
        cw, ch = w, int(w / ratio)
    return f"{cw}x{ch}+{(w - cw) // 2}+{(h - ch) // 2}"


def ascii_layer(src, ramp, pal, x0, cols=60, crop=None, **kw):
    """把 ASCII 渲染进 [x0, W] 这块区域，返回 tspan 串。

    主体必须落在右区，所以按区域宽高比裁源图 —— 满幅铺开再靠遮罩挡左边
    会让主体停在渐变过渡带里，右半边反而是空的。
    crop: 显式 magick geometry。这批壁纸是极简构图，主体只占画面中央一小块，
          按比例居中裁会得到一大片空背景，必须按主体框裁。
    """
    rw = W - x0
    cellw = rw / cols
    rows = max(1, round(H / (cellw / 0.6)))
    cellh = H / rows                      # 反算，保证正好铺满高度
    grid = A.sample(src, cols, rows, kw.get("sig", 4),
                    crop or crop_ratio(src, rw / H), kw.get("sharp"))
    snap = A.build_snap(pal)
    gamma, boost, floor = (kw.get("gamma", 1.0), kw.get("boost", 1.0),
                           kw.get("floor", 0.0))
    body = []
    for y, row in enumerate(grid):
        ty = (y + 0.82) * cellh
        runs, cur, xs, col = [], [], [], None
        for x, rgb in enumerate(row):
            lum = .2126 * rgb[0] + .7152 * rgb[1] + .0722 * rgb[2]
            n = (lum / 255) ** gamma * boost
            n = 0.0 if n <= floor else (n - floor) / (1 - floor)
            ch = ramp[min(len(ramp) - 1,
                          int(min(255, n * 255) / 256 * len(ramp)))]
            if ch == " ":
                if cur:
                    runs.append((col, xs, cur))
                    cur, xs = [], []
                col = None
                continue
            c = snap(rgb, n)
            if c != col and cur:
                runs.append((col, xs, cur))
                cur, xs = [], []
            col = c
            cur.append(ch)
            xs.append(f"{x0 + x * cellw:g}")
        if cur:
            runs.append((col, xs, cur))
        for c, xs, chs in runs:
            body.append(f'<tspan x="{" ".join(xs)}" y="{ty:g}" fill="{c}">'
                        f'{html.escape("".join(chs))}</tspan>')
    return (f'<text font-family="{MONO_FONT}" font-size="{cellh:g}" '
            f'xml:space="preserve">{"".join(body)}</text>')


def diagram_layer(rows, x0, size=27):
    """手写 ASCII 示意图。逐字符显式指定 x，不依赖字体 advance。

    rows: [[(文本, 颜色), ...], ...]，每行按列索引累加定位。
    图像派生的 ASCII 只适合本来就有视觉主体的源图；线条细的剪影在低分辨率下
    会退化成噪点，这种就该直接画图。
    """
    charw = size * 0.6
    ncol = max(sum(len(t) for t, _ in r) for r in rows)
    lead = x0 + ((W - x0) - ncol * charw) / 2
    top = (H - len(rows) * size * 1.6) / 2 + size
    body = []
    for y, row in enumerate(rows):
        ty = top + y * size * 1.6
        col = 0
        for text, color in row:
            if text.strip():
                xs = " ".join(f"{lead + (col + i) * charw:g}"
                              for i in range(len(text)))
                body.append(f'<tspan x="{xs}" y="{ty:g}" fill="{color}">'
                            f'{html.escape(text)}</tspan>')
            col += len(text)
    return (f'<text font-family="{MONO_FONT}" font-size="{size}" '
            f'xml:space="preserve">{"".join(body)}</text>')


def card(name, title, en, cn, x0=660, src=None, ramp=None, pal=None,
         rows=None, **kw):
    if rows:
        art = diagram_layer(rows, x0)
        layer = art                       # 手写图是完整构图，不该被遮罩切一刀
    else:
        assert src and ramp and pal, f"{name}: 缺 src/ramp/pal"
        art = ascii_layer(os.path.join(POOL, src), ramp, pal, x0, **kw)
        layer = f'<g mask="url(#m)">{art}</g>'
    e = html.escape
    f0, f1 = (x0 - 80) / W, (x0 + 130) / W
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="{f0:.3f}" stop-color="#000000"/>
    <stop offset="{f1:.3f}" stop-color="#ffffff"/>
  </linearGradient>
  <mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
</defs>
<rect width="{W}" height="{H}" fill="{BG}"/>
{layer}
<g font-family="{MONO_FONT}">
  <text x="80" y="176" font-size="19" fill="{MUTED}">~/numb747</text>
  <text x="80" y="268" font-size="56" fill="{FG}">{e(title)}</text>
  <rect x="80" y="304" width="72" height="3" fill="{PURPLE}"/>
  <text x="80" y="368" font-size="23" fill="{BLUE}">{e(en)}</text>
  <text x="80" y="410" font-size="21" fill="{DIM}">{e(cn)}</text>
  <text x="80" y="548" font-size="18" fill="{MUTED}">github.com/numb747/{e(name)}</text>
</g>
</svg>'''
    os.makedirs(OUT, exist_ok=True)
    sp = os.path.join(OUT, name + ".svg")
    dp = os.path.join(OUT, name + ".png")
    open(sp, "w").write(svg)
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-o", dp, sp],
                   check=True)
    os.remove(sp)
    return dp, os.path.getsize(dp)


CARDS = {
    "cachyOS-config": dict(
        title="cachyOS-config",
        en="CachyOS + Hyprland · Tokyo Night",
        cn="幂等安装器 · 10 篇记录「为什么」的文档",
        src="A-最搭/11-w55gjr.png", ramp=A.RAMP70, pal=A.PALETTE,
        crop="854x880+1454+620", cols=64,
        gamma=.70, boost=1.25, floor=.17, sig=5),
    "mitmweb-mcp": dict(
        title="mitmweb-mcp",
        en="One UI. You watch it, your AI reads it.",
        cn="把你正在看的 mitmweb 会话接给模型",
        rows=[
            [("        ╭─────────────╮", MUTED)],
            [("  you ", BLUE), ("──┤", MUTED), ("   ", MUTED),
             ("mitmweb", FG), ("   ", MUTED), ("├──", MUTED), (" AI", PURPLE)],
            [("        ╰─────────────╯", MUTED)],
            [("          one session", MUTED)],
        ]),
    "qiyou-Reverse": dict(
        title="qiyou-Reverse",
        en="Unpacking a hardened Android APK, end to end.",
        cn="腾讯乐固加固 APK 的完整逆向方法论",
        x0=600,
        rows=[
            [("     packed APK", FG)],
            [("         │", MUTED)],
            [("         ├─ ", MUTED), ("unpack", BLUE),
             ("      frida-dexdump", MUTED)],
            [("         ├─ ", MUTED), ("decompile", BLUE),
             ("   jadx", MUTED)],
            [("         ├─ ", MUTED), ("native", BLUE),
             ("      IDA Pro", MUTED)],
            [("         └─ ", MUTED), ("verify", PURPLE),
             ("      reproduce", MUTED)],
            [("         ▼", MUTED)],
            [("     methodology", FG)],
        ]),
}

if __name__ == "__main__":
    want = sys.argv[1:] or list(CARDS)
    for n in want:
        p, sz = card(n, **CARDS[n])
        print(f"  {n:18s} {sz/1024:6.0f} KB  {p}")
