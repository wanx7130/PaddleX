# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Author: PaddlePaddle Authors
"""
from ..object_detection import DetTrainer
from .support_models import SUPPORT_MODELS


class InstanceSegTrainer(DetTrainer):
    """ Instance Segmentation Model Trainer """
    support_models = SUPPORT_MODELS

    def _update_dataset(self):
        """update dataset settings
        """
        self.pdx_config.update_dataset(
            self.global_config.dataset_dir,
            "COCOInstSegDataset",
            data_fields=[
                'image', 'gt_bbox', 'gt_class', 'gt_poly', 'is_crowd'
            ])