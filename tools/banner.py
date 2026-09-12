#!/usr/bin/env python3
"""生成主页 README 的 ASCII 字标横幅。

把文字先渲成位图，再喂进 ~/cachyOS-config/wallpaper/tokyonight/_ascii.py 的
采样与调色板吸附管线 —— 字形本身由 ASCII 字符拼出来，配色走 Tokyo Night。

之所以不用 <pre> 里的盒绘字符：GitHub 的等宽字体会把 ┌─┐ 渲染得极小且糊成
一片，还带一个灰色底块。做成图片才可控。

用法：python3 banner.py
"""
import os
import html

from PIL import Image, ImageDraw, ImageFont

from _tn import (BG, BLUE, PURPLE, CYAN, MUTED, MONO_FONT as MONO,
                 load_ascii, write_png)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
FONT = "/usr/share/fonts/TTF/MesloLGSNerdFont-Bold.ttf"
A = load_ascii()

W, H = 1200, 260
COLS = 150                       # 字符列数；越高笔画越细腻


def text_bitmap(text, path, wfrac=0.46, ycenter=0.5):
    """把文字渲成黑底白字的高分辨率位图，供 ASCII 采样。

    wfrac 控制字标占画布宽度的比例 —— 撑满画布会让整幅过重，
    留白才是这套视觉的底色。ycenter 是竖向中心位置。
    """
    w, h = 3000, int(3000 * H / W)
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    lo, hi = 10, h
    while lo < hi:                       # 二分字号，撑到目标宽度为止
        mid = (lo + hi + 1) // 2
        f = ImageFont.truetype(FONT, mid)
        b = d.textbbox((0, 0), text, font=f)
        if b[2] - b[0] <= w * wfrac and b[3] - b[1] <= h * 0.72:
            lo = mid
        else:
            hi = mid - 1
    f = ImageFont.truetype(FONT, lo)
    b = d.textbbox((0, 0), text, font=f)
    d.text(((w - (b[2] - b[0])) / 2 - b[0],
            h * ycenter - (b[3] - b[1]) / 2 - b[1]),
           text, font=f, fill=255)
    im.save(path)
    return path


def render(src, dest, text_rows=()):
    """阈值化成 4 级块字符，颜色按横向位置走渐变。

    不能沿用 _ascii.py 的调色板吸附：源图是灰度的，snap() 拿不到色相，
    只会按明度退化成单色。而 70 级斜坡在 20 倍降采样后会把笔画中间调
    映射成稀疏标点，字形直接碎掉 —— 字标要的是实心，不是层次。
    """
    cellw = W / COLS
    rows = max(1, round(H / (cellw / 0.6)))
    cellh = H / rows
    grid = A.sample(src, COLS, rows, sig=3)
    # Tokyo Night 冷调渐变：蓝 → 紫 → 青
    hexrgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
    stops = [(0.0, hexrgb(BLUE)), (0.5, hexrgb(PURPLE)), (1.0, hexrgb(CYAN))]

    def grad(t):
        for i in range(len(stops) - 1):
            a, b = stops[i], stops[i + 1]
            if a[0] <= t <= b[0]:
                k = (t - a[0]) / (b[0] - a[0])
                return "#%02x%02x%02x" % tuple(
                    round(a[1][j] + (b[1][j] - a[1][j]) * k) for j in range(3))
        return BLUE

    LEVELS = [(0.62, "█"), (0.40, "▓"), (0.20, "▒"), (0.08, "░")]
    lum = [[(0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]) / 255 for p in r]
           for r in grid]
    # 渐变按字标的实际横向范围映射，不是画布宽度 ——
    # 字标只占中间一段，按画布算会把蓝、青两端全浪费掉，只剩中间的紫。
    inked = [x for r in lum for x, n in enumerate(r) if n >= LEVELS[-1][0]]
    x0, x1 = (min(inked), max(inked)) if inked else (0, COLS - 1)
    span = max(1, x1 - x0)
    body = []
    for y, row in enumerate(grid):
        ty = (y + 0.82) * cellh
        runs, cur, xs, col = [], [], [], None
        for x, rgb in enumerate(row):
            n = lum[y][x]
            ch = next((c for thr, c in LEVELS if n >= thr), " ")
            if ch == " ":
                if cur:
                    runs.append((col, xs, cur)); cur, xs = [], []
                col = None
                continue
            c = grad(min(1.0, max(0.0, (x - x0) / span)))
            if c != col and cur:
                runs.append((col, xs, cur)); cur, xs = [], []
            col = c
            cur.append(ch)
            xs.append(f"{x * cellw:g}")
        if cur:
            runs.append((col, xs, cur))
        for c, xs, chs in runs:
            body.append(f'<tspan x="{" ".join(xs)}" y="{ty:g}" fill="{c}">'
                        f'{html.escape("".join(chs))}</tspan>')

    extra = "".join(
        f'<text x="{W/2:g}" y="{y}" font-family="{MONO}" font-size="{sz}" '
        f'fill="{fill}" text-anchor="middle" letter-spacing="{ls}">'
        f'{html.escape(t)}</text>'
        for t, y, sz, fill, ls in text_rows)

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{BG}"/>'
           f'<text font-family="{MONO}" font-size="{cellh:g}" '
           f'xml:space="preserve">{"".join(body)}</text>{extra}</svg>')
    return write_png(svg, dest, W, H)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    bmp = text_bitmap("numb747", "/tmp/_wordmark.png", wfrac=0.46, ycenter=0.44)
    dest = os.path.join(OUT, "banner.png")
    rows = (("reverse engineering  ·  scraping  ·  linux ricing",
             int(H * 0.78), 17, MUTED, 2.4),)
    print(f"  banner.png  {render(bmp, dest, rows)/1024:.0f} KB  {dest}")
