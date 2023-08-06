# Author: Acer Zhang
# Datetime:2021/11/21 
# Copyright belongs to the author.
# Please indicate the source for reprinting.


class Box:
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom


class Collector:
    def __init__(self, im, clip_im, box:Box, seg):
        self.c_im = im
        self.c_clip_im = clip_im
        self.c_box = box
        self.c_seg = seg
        self.out = None

    def set_out(self, out):
        self.out = out
