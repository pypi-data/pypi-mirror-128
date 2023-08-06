"""
des: 水平方向 双屏计算
author: mr52hz
date: 2021-11-24
"""
from xy.base import Base


class H(Base):

    def __init__(self, w=1920, h=1080):
        super(H, self).__init__(width=w, height=h)

    def cut(self):
        if self.p == -1 or self.left == -1 or self.right == -1:
            return
        # 保持屏幕切割 缩放后占width差不多一半
        rate = round(1 - self.left - self.right, 2) * self.p
        if rate < 0.45 or rate > 0.55:
            l_r = 1 - (0.5 / self.p)
            print('缩放切割后占半屏 [1-(l+r)]*p=0.5 建议l+r=%s' % round(l_r, 2))
        x1 = (1 / 2 - self.left) * self.width * self.p
        x2 = (1 - self.p / 2 + self.p * self.right) * self.width
        print(self)
        print('x1:', round(x1, 2), '\nx2:', round(x2, 2))


if __name__ == '__main__':
    v = H(1920)
    v.p = 0.7
    # v.left = 0.18
    # v.right = 0.12
    v.cut()
