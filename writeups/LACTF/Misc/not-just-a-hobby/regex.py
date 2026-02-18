import re
import matplotlib.pyplot as plt

text = open("v.v").read()

coords = re.findall(
    r"\(x == (?:7'd)?(\d+) && y == (?:7'd)?(\d+)\)",
    text
)

# 轉成整數並做 mod128
coords = [(int(x) % 128, int(y) % 128) for x, y in coords]

xs = [c[0] for c in coords]
ys = [c[1] for c in coords]

plt.scatter(xs, ys, s=2)
plt.gca().invert_yaxis()
plt.savefig("QRcode.png")
plt.show()
