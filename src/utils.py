import sys
from os import path
import math
from pygame import font

HEIGHT = 1000
WIDTH = 1000
X_CORNER = 100
Y_CORNER = 100
BLOCK_SIZE = 180
BLOCK_PADDING = 16
FPS = 60

COLORS = (
    (238, 228, 218), # 2
    (237, 224, 200), # 4
    (242, 177, 121), # 8
    (245, 149, 99),  # 16
    (246, 124, 95),  # 32
    (246, 94, 59),   # 64
    (237, 207, 114), # 128
    (237, 204, 97),  # 256
    (237, 200, 80),  # 512
    (237, 197, 63),  # 1024
    (237, 194, 46),  # 2048
    (62, 57, 51)     # 4096 and next
)

FONT_COLORS = (
    (119, 110, 101), # 2 and 4
    (249, 246, 242) # 8 and next
)

def get_color(val: int) -> tuple[int, int, int]:
    index = int(math.log2(val)) - 1
    if index >= len(COLORS):
        return COLORS[len(COLORS) - 1]
    else:
        return COLORS[index]
    
def get_font_color(val: int) -> tuple[int, int, int]:
    return FONT_COLORS[0] if val in (2, 4) else FONT_COLORS[1]

def lerp_quadratic(a: float, b: float, s: int) -> tuple[int]:
    values = []
    diff = b - a
    for i in range(s+1):
        x = i / s
        value = a + diff * math.pow(x, 2)
        values.append(int(value))
    return tuple(values)

def res_path(rel_path: str) -> str:
    """
    Return path to file modified by auto_py_to_exe path if packed to exe already
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = sys.path[0]
    return path.normpath(path.join(base_path, rel_path))