# copyright (c) 2024 PaddlePaddle Authors. All Rights Reserve.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict, Optional, Union
import numpy as np
from ...utils.pp_option import PaddlePredictorOption
from ..base import BasePipeline

# [TODO] 待更新models_new到models
from ...models_new.video_detection.result import DetVideoResult


class VideoDetectionPipeline(BasePipeline):
    """Video detection Pipeline"""

    entities = "video_detection"

    def __init__(
        self,
        config: Dict,
        device: str = None,
        pp_option: PaddlePredictorOption = None,
        use_hpip: bool = False,
        hpi_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initializes the class with given configurations and options.

        Args:
            config (Dict): Configuration dictionary containing model and other parameters.
            device (str): The device to run the prediction on. Default is None.
            pp_option (PaddlePredictorOption): Options for PaddlePaddle predictor. Default is None.
            use_hpip (bool): Whether to use high-performance inference (hpip) for prediction. Defaults to False.
            hpi_params (Optional[Dict[str, Any]]): HPIP specific parameters. Default is None.
        """
        super().__init__(
            device=device, pp_option=pp_option, use_hpip=use_hpip, hpi_params=hpi_params
        )

        video_detection_model_config = config["SubModules"]["VideoDetection"]
        self.video_detection_model = self.create_model(video_detection_model_config)

    def predict(
        self, input: str | list[str] | np.ndarray | list[np.ndarray], **kwargs
    ) -> DetVideoResult:
        """Predicts video detection results for the given input.

        Args:
            input (str | list[str] | np.ndarray | list[np.ndarray]): The input image(s) or path(s) to the images.
            **kwargs: Additional keyword arguments that can be passed to the function.

        Returns:
            DetVideoResult: The predicted video detection results.
        """

        yield from self.video_detection_model(input)