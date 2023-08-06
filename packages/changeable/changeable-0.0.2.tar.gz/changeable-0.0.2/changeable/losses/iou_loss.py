# -*- coding: utf-8 -*-
# @Author  : LG

import numpy as np
import torch
from torch import nn
from typing import Union
import math

__all__ = ["IoULoss", "GIoULoss", "DIoULoss", "CIoULoss"]

def boxes_area(boxes: torch.Tensor) -> torch.Tensor:
    """
    计算包围盒面积     框体格式[xmin, ymin, xmax, ymax]
    :param boxes:   shape[..., 4]
    :return:
    """
    area_wh = boxes[..., 2:] - boxes[..., :2]
    area_wh[area_wh<0] = 0
    return area_wh[..., 0] * area_wh[..., 1]

def cal_iou(boxes1: Union[torch.Tensor, np.ndarray],
            boxes2: Union[torch.Tensor, np.ndarray],
            eps = 1e-6) -> torch.Tensor:
    """
    iou损失   框体格式[xmin, ymin, xmax, ymax]
    :param boxes1:  shape[..., 4]
    :param boxes2:  shape[..., 4]
    :return:
    """
    area1 = boxes_area(boxes1)
    area2 = boxes_area(boxes2)

    # 交叉区域左上右下角
    lt = torch.max(boxes1[..., :2], boxes2[..., :2])
    rb = torch.min(boxes1[..., 2:], boxes2[..., 2:])
    wh = torch.clamp(rb-lt, 0)
    overlap_area = wh[..., 0] * wh[...,1]
    ious = overlap_area / (area1 + area2 - overlap_area)
    return -ious.clamp(eps).log()

def cal_giou(boxes1: Union[torch.Tensor, np.ndarray],
             boxes2: Union[torch.Tensor, np.ndarray],
             eps = 1e-7) -> torch.Tensor:
        """
        giou损失   框体格式[xmin, ymin, xmax, ymax]
        :param boxes1:  shape[..., 4]
        :param boxes2:  shape[..., 4]
        :eps:           1e-7
        :return:
        """
        area1 = boxes_area(boxes1)
        area2 = boxes_area(boxes2)

        # 交叉区域左上右下角
        lt = torch.max(boxes1[..., :2], boxes2[..., :2])
        rb = torch.min(boxes1[..., 2:], boxes2[..., 2:])
        wh = torch.clamp(rb - lt, 0)
        overlap_area = wh[..., 0] * wh[..., 1]

        # 最小包围区域，左上右下角
        lt = torch.min(boxes1[..., :2], boxes2[..., :2])
        rb = torch.max(boxes1[..., 2:], boxes2[..., 2:])
        wh = torch.clamp(rb-lt, 0)
        enclosed_area = torch.clamp(wh[..., 0] * wh[...,1], eps)

        ious = overlap_area / (area1 + area2 - overlap_area)
        gious = ious - (enclosed_area - (area1 + area2 - overlap_area)) / enclosed_area
        return -(gious-1)

def cal_diou(boxes1: Union[torch.Tensor, np.ndarray],
             boxes2: Union[torch.Tensor, np.ndarray],
             eps = 1e-7) -> torch.Tensor:
    """
    diou损失   框体格式[xmin, ymin, xmax, ymax]
    :param boxes1:  shape[..., 4]
    :param boxes2:  shape[..., 4]
    :eps:           1e-7
    :return:
    """
    area1 = boxes_area(boxes1)
    area2 = boxes_area(boxes2)

    # 交叉区域左上右下角
    lt = torch.max(boxes1[..., :2], boxes2[..., :2])
    rb = torch.min(boxes1[..., 2:], boxes2[..., 2:])
    wh = torch.clamp(rb - lt, 0)
    overlap_area = wh[..., 0] * wh[..., 1]

    ious = overlap_area / (area1 + area2 - overlap_area)

    # 最小包围区域，左上右下角
    lt = torch.min(boxes1[..., :2], boxes2[..., :2])
    rb = torch.max(boxes1[..., 2:], boxes2[..., 2:])
    wh = torch.clamp(rb-lt, 0)
    c2 = wh[..., 0] ** 2 + wh[..., 1] ** 2 + eps

    boxes1_cxcy = (boxes1[:, :2] + boxes1[:, 2:]) / 2
    boxes2_cxcy = (boxes2[:, :2] + boxes2[:, 2:]) / 2
    p2 = (boxes1_cxcy[..., 0] - boxes2_cxcy[..., 0]) ** 2 + \
         (boxes1_cxcy[..., 1] - boxes2_cxcy[..., 1]) ** 2
    dious = ious - p2 / c2
    return 1-dious

def cal_ciou(boxes1: Union[torch.Tensor, np.ndarray],
             boxes2: Union[torch.Tensor, np.ndarray],
             eps = 1e-7) -> torch.Tensor:
    """
    ciou损失   框体格式[xmin, ymin, xmax, ymax]
    :param boxes1:  shape[..., 4]
    :param boxes2:  shape[..., 4]
    :eps:           1e-7
    :return:
    """
    area1 = boxes_area(boxes1)
    area2 = boxes_area(boxes2)

    # 交叉区域左上右下角
    lt = torch.max(boxes1[..., :2], boxes2[..., :2])
    rb = torch.min(boxes1[..., 2:], boxes2[..., 2:])
    wh = torch.clamp(rb - lt, 0)
    overlap_area = wh[..., 0] * wh[..., 1]

    ious = overlap_area / (area1 + area2 - overlap_area)

    # 最小包围区域，左上右下角
    lt = torch.min(boxes1[..., :2], boxes2[..., :2])
    rb = torch.max(boxes1[..., 2:], boxes2[..., 2:])
    wh = torch.clamp(rb - lt, 0)
    c2 = wh[..., 0] ** 2 + wh[..., 1] ** 2 + eps

    boxes1_cxcy = (boxes1[:, :2] + boxes1[:, 2:]) / 2
    boxes2_cxcy = (boxes2[:, :2] + boxes2[:, 2:]) / 2
    p2 = (boxes1_cxcy[..., 0] - boxes2_cxcy[..., 0]) ** 2 + \
         (boxes1_cxcy[..., 1] - boxes2_cxcy[..., 1]) ** 2
    dious = ious - p2 / c2

    boxes1_wh = (boxes1[:, 2:] - boxes1[:, :2]) / 2
    boxes2_wh = (boxes2[:, 2:] - boxes2[:, :2]) / 2

    factor = 4 / math.pi ** 2
    v = factor * torch.pow(torch.atan(boxes1_wh[:, 0] / boxes1_wh[:, 1]) - torch.atan(boxes2_wh[:, 0]/boxes2_wh[:, 1]), 2)

    return 1 - dious + v ** 2 / (-ious + 1 + v)

class IoULoss(nn.Module):
    def __init__(self, eps=1e-6, weight=None, reduction='mean'):
        super(IoULoss, self).__init__()
        assert reduction in ["mean", "sum", "none"]
        self.eps = eps
        self.weight = weight
        self.reduction = reduction

    def forward(self, pred_bbox, gt_bbox):
        iou = cal_iou(pred_bbox, gt_bbox)

        if self.weight is not None:
            self.weight = self.weight.to(pred_bbox.device)
            iou = iou * self.weight

        if self.reduction == "mean":
            iou = iou.mean()
        elif self.reduction == "sum":
            iou = iou.sum()
        elif self.reduction == "none":
            iou = iou

        return iou

class GIoULoss(nn.Module):
    def __init__(self, eps=1e-6, weight=None, reduction='mean'):
        super(GIoULoss, self).__init__()
        assert reduction in ["mean", "sum", "none"]
        self.eps = eps
        self.weight = weight
        self.reduction = reduction

    def forward(self, pred_bbox, gt_bbox):
        giou = cal_giou(pred_bbox, gt_bbox)

        if self.weight is not None:
            self.weight = self.weight.to(pred_bbox.device)
            giou = giou * self.weight

        if self.reduction == "mean":
            giou = giou.mean()
        elif self.reduction == "sum":
            giou = giou.sum()
        elif self.reduction == "none":
            giou = giou

        return giou

class DIoULoss(nn.Module):
    def __init__(self, eps=1e-6, weight=None, reduction='mean'):
        super(DIoULoss, self).__init__()
        assert reduction in ["mean", "sum", "none"]
        self.eps = eps
        self.weight = weight
        self.reduction = reduction

    def forward(self, pred_bbox, gt_bbox):
        diou = cal_diou(pred_bbox, gt_bbox)

        if self.weight is not None:
            self.weight = self.weight.to(pred_bbox.device)
            diou = diou * self.weight

        if self.reduction == "mean":
            diou = diou.mean()
        elif self.reduction == "sum":
            diou = diou.sum()
        elif self.reduction == "none":
            diou = diou

        return diou

class CIoULoss(nn.Module):
    def __init__(self, eps=1e-6, weight=None, reduction='mean'):
        super(CIoULoss, self).__init__()
        assert reduction in ["mean", "sum", "none"]
        self.eps = eps
        self.weight = weight
        self.reduction = reduction

    def forward(self, pred_bbox, gt_bbox):
        ciou = cal_ciou(pred_bbox, gt_bbox)

        if self.weight is not None:
            self.weight = self.weight.to(pred_bbox.device)
            ciou = ciou * self.weight

        if self.reduction == "mean":
            ciou = ciou.mean()
        elif self.reduction == "sum":
            ciou = ciou.sum()
        elif self.reduction == "none":
            ciou = ciou

        return ciou



