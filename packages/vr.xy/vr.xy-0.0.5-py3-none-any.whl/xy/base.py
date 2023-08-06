from abc import ABCMeta, abstractmethod


class Base(metaclass=ABCMeta):

    def __init__(self, width, height):
        """
        初始化
        :param width: 视频总宽度
        """
        self.width = width
        self.height = height
        self._p = 0.5
        self._l = 0
        self._r = 0

    @staticmethod
    def _check_float(value):
        if isinstance(value, str):
            try:
                value = float(value)
            except Exception:
                return False, -1
        if not isinstance(value, float):
            return False, -1
        if value > 1 or value < 0:
            return False, -1
        return True, round(value, 2)

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, value):
        state, self._p = self._check_float(value)
        if state is False:
            print('注意0<=P<=1')

    @property
    def left(self):
        return self._l

    @left.setter
    def left(self, value):
        state, self._l = self._check_float(value)
        if state is False:
            print('注意0<=L<=1')

    @property
    def right(self):
        return self._r

    @right.setter
    def right(self, value):
        state, self._r = self._check_float(value)
        if state is False:
            print('注意0<=R<=1')

    @abstractmethod
    def cut(self):
        pass

    def __repr__(self):
        return '[H-MSG] W=%s, H=%s, P=%s%%, L=%s%%, R=%s%%' % \
               (self.width, self.height, self.p * 100, self.left * 100, self.right * 100)

    def __str__(self):
        return '[H-MSG] W=%s, H=%s, P=%s%%, L=%s%%, R=%s%%' % \
               (self.width, self.height, self.p * 100, self.left * 100, self.right * 100)
