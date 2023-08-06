
import argparse
import sys

from xy.Horizontal import H


video_h = H(1920, 1080)

APP_DESC = """
**双屏视频坐标计算**
视频默认为1920*1080
p = 0.5
l,r = 0
"""


def v_h_xy(args=sys.argv):

    if len(args) == 1:
        sys.argv.append('--help')
    elif len(args) == 2 and '-' not in args[1]:
        p = sys.argv[1]
        video_h.p = p
        video_h.cut()
        return

    parser = argparse.ArgumentParser(description=APP_DESC)
    parser.add_argument('-W', '--width', type=int, help="the video pixel width")
    parser.add_argument('-H', '--height', type=int, help="the video pixel height")
    parser.add_argument('-p', '--zoom', type=float, help="the video zoom percent")
    parser.add_argument('-l', '--left', type=float, help="left cut percent")
    parser.add_argument('-r', '--right', type=float, help="right cut percent")

    _args = parser.parse_args(args[1:])

    w = _args.width
    h = _args.height
    p = _args.zoom
    l = _args.left
    r = _args.right
    if w is not None:
        video_h.width = w
    if h is not None:
        video_h.height = h
    if p is not None:
        video_h.p = p
    if l is not None:
        video_h.left = l
    if r is not None:
        video_h.right = r

    video_h.cut()


if __name__ == '__main__':
    v_h_xy()
