# Author: Acer Zhang
# Datetime:2021/11/22 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import cv2
import numpy as np

from agentfc.collector import Collector
from agentfc.facedet import get_face, face_seg


class FaceCollector:
    def __init__(self,
                 inp,
                 save_path: str,
                 op,
                 mask=True):
        if isinstance(inp, str):
            inp = cv2.imread(inp)
        self.inp = inp
        self.save_path = save_path
        self.mask = mask
        assert hasattr(op, "__call__"), AssertionError("op不可调用，请检查传入的op是否支持op()操作")
        self.op = op

    def pretreatment(self, frame):
        clip, box, seg = get_face(frame, self.mask)
        cr = Collector(frame, clip, box, seg)
        return cr

    @staticmethod
    def mix(cr):
        seg = face_seg(cr.out)
        box = cr.c_box
        clip = cr.c_im[box.top:box.bottom, box.left:box.right, :]
        c_seg = np.array([seg] * clip.shape[-1], dtype="uint8").transpose([1, 2, 0])
        clip[c_seg == 1] = cr.out[c_seg == 1]
        cr.c_im[box.top:box.bottom, box.left:box.right, :] = clip.copy()
        return cr.c_im

    def mk_img(self):
        cr = self.pretreatment(self.inp)
        # 自定义操作
        out = self.op(cr.c_clip_im)
        cr.set_out(out)
        # 后处理
        final = self.mix(cr)
        if self.save_path:
            cv2.imwrite(self.save_path, final)
        return final

    def mk_mp4(self):
        cap = cv2.VideoCapture(self.inp)
        fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        output_movie = cv2.VideoWriter(self.save_path, fourcc, fps, (height, width))
        idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if frame is None:
                break
            print(f"正在处理{idx}帧")
            idx += 1
            # 前处理
            cr = self.pretreatment(frame)
            # 自定义操作
            out = self.op(cr.c_clip_im)
            cr.set_out(out)
            # 后处理
            final = self.mix(cr)
            output_movie.write(final)
        cap.release()
        output_movie.release()
        print("处理完毕")
