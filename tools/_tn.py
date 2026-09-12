"""tools/ 下两个生成脚本共用的底座。

放这里的东西只有一个标准：改一次就该两边都生效。配色首当其冲 —— 之前
social-card.py 和 banner.py 各存一份 Tokyo Night 色值，调色得改两处。
"""
import importlib.util
import os
import subprocess

# Tokyo Night
BG = "#1a1b26"
FG = "#c0caf5"
BLUE = "#7aa2f7"
PURPLE = "#bb9af7"
CYAN = "#7dcfff"
MUTED = "#565f89"
DIM = "#a9b1d6"

# CJK 由 Sarasa 兜底：MesloLGS 没有汉字字形，缺了它中文会掉成方框
MONO_FONT = "MesloLGS Nerd Font Mono, Sarasa Mono SC"

ASCII_PY = os.path.expanduser(
    "~/cachyOS-config/wallpaper/tokyonight/_ascii.py")


def load_ascii():
    """加载 cachyOS-config 里那份 ASCII 管线（采样 / 调色板吸附 / 亮度斜坡）。

    它不是包，只能按路径加载。两个脚本都要用，所以收在这里。
    """
    spec = importlib.util.spec_from_file_location("_ascii", ASCII_PY)
    assert spec and spec.loader, f"读不到 {ASCII_PY}"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_png(svg, dest, w, h):
    """SVG 字符串 → PNG。rsvg-convert 只吃文件，所以先落临时 svg 再删。"""
    sp = dest + ".svg"
    open(sp, "w").write(svg)
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), "-o", dest, sp],
                   check=True)
    os.remove(sp)
    return os.path.getsize(dest)
