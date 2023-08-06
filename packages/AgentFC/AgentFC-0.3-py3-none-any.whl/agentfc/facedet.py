# Author: Acer Zhang
# Datetime:2021/11/21 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import paddlehub as hub
import cv2
import numpy as np

from agentfc.collector import Box

# face_detector = hub.Module(name="ultra_light_fast_generic_face_detector_1mb_640")
human_seg = hub.Module(name="ace2p")


# def face_det(img):
#     result = face_detector.face_detection(images=[img])[0]["data"][0]
#     left, right, top, bottom, cf = result.values()
#     return int(left), int(right), int(top), int(bottom), cf
def face_det(img):
    x, y, w, h = cv2.boundingRect(img)
    return x, x + w, y, y + h


def face_seg(img, pad=32):
    img = img.copy()
    img = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    result = human_seg.segmentation(images=[img])[0]["data"]
    result[result == 2] = 13
    result[result != 13] = 0
    result[result == 13] = 1

    result = result[pad:-pad, pad:-pad]
    return result.astype("uint8")


def get_face(ori_img, mask=True):
    img = ori_img.copy()
    # 获取面部分割
    c_mask = face_seg(img)
    img[np.array([c_mask] * img.shape[-1], dtype="uint8").transpose([1, 2, 0]) == 0] = 0
    # 获取外接正矩形
    left, right, top, bottom = face_det(c_mask)
    # 裁剪
    if mask:
        clip = img[top:bottom, left:right, :]
    else:
        clip = ori_img[top:bottom, left:right, :]
    box = Box(left, right, top, bottom)
    return clip, box, mask
