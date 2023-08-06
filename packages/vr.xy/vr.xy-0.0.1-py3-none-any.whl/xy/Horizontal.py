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
        if round(1 - self.p, 2) != self.left + self.right:
            print(self)
            print('注意1-P=L+R')
            return
        x1 = (1 / 2 - self.left) * self.width * self.p
        x2 = (1 - self.p / 2 + self.p * self.right) * self.width
        print(self)
        print('x1:', round(x1, 2), '\nx2:', round(x2, 2))


if __name__ == '__main__':
    v = H(1920)
    v.p = 0.7
    v.left = 0.18
    v.right = 0.12
    v.cut()
