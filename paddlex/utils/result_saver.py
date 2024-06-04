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
import sys
import json
import traceback
from .flags import DEBUG
from .file_interface import custom_open


def try_except_decorator(func):
    """ try-except """

    def wrap(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            if result:
                save_result(
                    True, self.mode, self.output_dir, result_dict=result)
        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            save_result(
                False,
                self.mode,
                self.output_dir,
                err_type=str(exc_type),
                err_msg=str(exc_value))
            traceback.print_exception(exc_type, exc_value, exc_tb)

    return wrap


def save_result(run_pass,
                mode,
                output_dir,
                result_dict=None,
                err_type=None,
                err_msg=None):
    """ format, build and save result """
    json_data = {
        # "model_name": self.args.model_name, 
        "done_flag": run_pass
    }
    if not run_pass:
        assert result_dict is None and err_type is not None and err_msg is not None
        json_data.update({"err_type": err_type, "err_msg": err_msg})
    else:
        assert result_dict is not None and err_type is None and err_msg is None
        json_data.update(result_dict)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with custom_open(os.path.join(output_dir, f"{mode}_result.json"), "w") as f:
        json.dump(json_data, f, indent=2)