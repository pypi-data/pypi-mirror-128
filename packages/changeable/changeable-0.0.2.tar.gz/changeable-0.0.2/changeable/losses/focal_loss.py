# -*- coding: utf-8 -*-
# @Author  : LG

from torch import nn
import torch
from torch.nn import functional as F

__all__ = ["FocalLoss"]

class FocalLoss(nn.Module):
    def __init__(self, gamma=2, weight=None, reduction="mean"):
        """
        focal_loss损失函数, -w(1-yi)**γ *ce_loss(xi,yi)
        :param gamma:       伽马γ,难易样本调节参数.
        :param weight:      权重
        :param reduction:   mean or sum or none
        """
        super(FocalLoss, self).__init__()
        assert reduction in ["mean", "sum", "none"]
        self.reduction = reduction
        self.gamma = gamma
        self.weight = weight

    def forward(self, preds, labels):
        """
        focal_loss损失计算
        :param preds:   预测类别. size:[B,N,C] or [B,C]    分别对应与检测与分类任务, B 批次, N检测框数, C类别数
        :param labels:  实际类别. size:[B,N] or [B]
        :return:
        """
        preds = preds.view(-1,preds.size(-1))
        preds_logsoft = F.log_softmax(preds, dim=1)
        preds_softmax = torch.exp(preds_logsoft)

        preds_softmax = preds_softmax.gather(1,labels.view(-1,1))
        preds_logsoft = preds_logsoft.gather(1,labels.view(-1,1))
        loss = -torch.mul(torch.pow((-preds_softmax+1), self.gamma), preds_logsoft).t()

        if self.weight is not None:
            self.weight = self.weight.to(preds.device)
            loss = loss * self.weight

        if self.reduction == "mean":
            loss = loss.mean()
        elif self.reduction == "sum":
            loss = loss.sum()
        elif self.reduction == "none":
            loss = loss
        return loss
