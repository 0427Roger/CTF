import re
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 讀取並抽座標（mod 128）
# -----------------------------
text = open("v.v").read()

coords = re.findall(
    r"\(x == (?:7'd)?(\d+) && y == (?:7'd)?(\d+)\)",
    text
)

coords = [(int(x) % 128, int(y) % 128) for x, y in coords]
coords = list(set(coords))

# 建立 base 影像
base = np.zeros((128,128), dtype=np.uint8)
for x, y in coords:
    base[y, x] = 255


# -----------------------------
# Finder Pattern
# -----------------------------
finder = np.array([
[1,1,1,1,1,1,1],
[1,0,0,0,0,0,1],
[1,0,1,1,1,0,1],
[1,0,1,1,1,0,1],
[1,0,1,1,1,0,1],
[1,0,0,0,0,0,1],
[1,1,1,1,1,1,1]
], dtype=np.uint8) * 255


# -----------------------------
# QR size
# -----------------------------
def qr_size(version):
    return 21 if version == 1 else 25


def finder_positions(N):
    return [
        (0,0),
        (N-7,0),
        (0,N-7)
    ]


# -----------------------------
# 加入定位符
# -----------------------------
def add_finder(img, version):

    img = img.copy()
    N = qr_size(version)
    scale = 128 // N

    for (fx, fy) in finder_positions(N):

        px = fx * scale
        py = fy * scale

        scaled = np.kron(finder, np.ones((scale,scale)))

        h, w = scaled.shape
        if py+h <= 128 and px+w <= 128:
            img[py:py+h, px:px+w] = scaled

    return img


# -----------------------------
# 旋轉 + 反轉測試
# -----------------------------
versions = [1,2]

for v in versions:

    img = add_finder(base, v)

    # normal / invert
    for inv in [False, True]:

        test_img = 255 - img if inv else img

        # rotations
        for rot in range(4):

            rotated = np.rot90(test_img, rot)

            name = f"QR_v{v}_inv{int(inv)}_rot{rot*90}.png"

            plt.figure(figsize=(5,5))
            plt.imshow(rotated, cmap="gray")
            plt.axis("off")
            plt.savefig(name)
            plt.close()

print("Done.")
