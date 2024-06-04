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

import os
import platform
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

from ....utils.fonts import PINGFANG_FONT_FILE_PATH


def deep_analyse(dataset_dir, output_dir, label_col='label'):
    """class analysis for dataset"""
    tags = ['train', 'val', 'test']
    label_unique = None
    for tag in tags:
        csv_path = os.path.abspath(os.path.join(dataset_dir, tag + '.csv'))
        if tag == 'test' and not os.path.exists(csv_path):
            cls_test = None
            continue
        df = pd.read_csv(csv_path)
        if label_col not in df.columns:
            if tag == 'test':
                cls_test = None
                continue
            raise ValueError(
                f"default label_col: {label_col} not in {tag} dataset")
        if label_unique is None:
            label_unique = df[label_col].unique()
        cls_dict = {}
        for label in label_unique:
            vis_df = df[df[label_col].isin([label])]
            cls_dict[label] = len(vis_df)
        if tag == 'train':
            cls_train = [label_num for label_col, label_num in cls_dict.items()]
        elif tag == 'val':
            cls_val = [label_num for label_col, label_num in cls_dict.items()]
        else:
            cls_test = [label_num for label_col, label_num in cls_dict.items()]
    sorted_id = sorted(
        range(len(cls_train)), key=lambda k: cls_train[k], reverse=True)
    cls_train_sorted = sorted(cls_train, reverse=True)
    cls_val_sorted = [cls_val[index] for index in sorted_id]
    if cls_test:
        cls_test_sorted = [cls_test[index] for index in sorted_id]
    classes_sorted = [label_unique[index] for index in sorted_id]
    x = np.arange(len(label_unique))
    width = 0.5 if not cls_test else 0.333

    # bar
    os_system = platform.system().lower()
    if os_system == "windows":
        plt.rcParams['font.sans-serif'] = 'FangSong'
    else:
        font = font_manager.FontProperties(fname=PINGFANG_FONT_FILE_PATH)
    fig, ax = plt.subplots(
        figsize=(max(8, int(len(label_unique) / 5)), 5), dpi=120)
    ax.bar(x,
           cls_train_sorted,
           width=0.5 if not cls_test else 0.333,
           label='train')
    ax.bar(x + width,
           cls_val_sorted,
           width=0.5 if not cls_test else 0.333,
           label='val')
    if cls_test:
        ax.bar(x + 2 * width, cls_test_sorted, width=0.333, label='test')
    plt.xticks(
        x + width / 2 if not cls_test else x + width,
        classes_sorted,
        rotation=90,
        fontproperties=None if os_system == "windows" else font)
    ax.set_ylabel('Counts')
    plt.legend()
    fig.tight_layout()
    fig_path = os.path.join(output_dir, "histogram.png")
    fig.savefig(fig_path)
    return {"histogram": "histogram.png"}