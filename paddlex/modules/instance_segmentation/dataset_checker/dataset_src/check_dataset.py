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
import json
import os
import os.path as osp
from collections import defaultdict, Counter
from pathlib import Path

from PIL import Image, ImageOps
from pycocotools.coco import COCO

from .utils.visualizer import draw_bbox, draw_mask
from .....utils.errors import DatasetFileNotFoundError


def check(dataset_dir, output_dir, sample_num=10):
    """ check dataset """
    print(dataset_dir)
    dataset_dir = osp.abspath(dataset_dir)
    if not osp.exists(dataset_dir) or not osp.isdir(dataset_dir):
        raise DatasetFileNotFoundError(file_path=dataset_dir)

    sample_cnts = dict()
    sample_paths = defaultdict(list)
    im_sizes = defaultdict(Counter)
    tags = ['instance_train', 'instance_val']
    for _, tag in enumerate(tags):
        file_list = osp.join(dataset_dir, f'annotations/{tag}.json')
        if not osp.exists(file_list):
            if tag in ('instance_train', 'instance_val'):
                # train and val file lists must exist
                raise DatasetFileNotFoundError(
                    file_path=file_list,
                    solution=f"Ensure that both `instance_train.json` and `instance_val.json` exist in \
{dataset_dir}/annotations")
            else:
                continue
        else:
            with open(file_list, 'r', encoding='utf-8') as f:
                jsondata = json.load(f)

            datanno = jsondata['annotations']
            sample_cnts[tag] = len(datanno)
            coco = COCO(file_list)
            num_class = len(coco.getCatIds())

            vis_save_dir = osp.join(output_dir, 'tmp')

            image_info = jsondata['images']
            for i in range(sample_num):
                file_name = image_info[i]['file_name']
                img_id = image_info[i]['id']
                img_path = osp.join(dataset_dir, 'images', file_name)
                if not osp.exists(img_path):
                    raise DatasetFileNotFoundError(file_path=img_path)
                img = Image.open(img_path)
                img = ImageOps.exif_transpose(img)
                vis_im = draw_bbox(img, coco, img_id)
                vis_im = draw_mask(vis_im, coco, img_id)
                vis_path = osp.join(vis_save_dir, file_name)
                Path(vis_path).parent.mkdir(parents=True, exist_ok=True)
                vis_im.save(vis_path)
                sample_paths[tag].append(os.path.relpath(vis_path, output_dir))

    attrs = {}
    attrs['num_classes'] = num_class
    attrs['train_samples'] = sample_cnts['instance_train']
    # attrs['train_im_sizes'] = im_sizes['instance_train']
    attrs['train_sample_paths'] = sample_paths['instance_train']

    attrs['val_samples'] = sample_cnts['instance_val']
    # attrs['val_im_sizes'] = im_sizes['instance_val']
    attrs['val_sample_paths'] = sample_paths['instance_val']
    return attrs