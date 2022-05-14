# coding=utf-8
# Copyright 2022 The HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Convert OpenAI GPT checkpoint."""


import argparse

import torch

from transformers import SmallTransformerConfig, SmallTransformerModel, load_tf_weights_in_small_transformer
from transformers.utils import CONFIG_NAME, WEIGHTS_NAME, logging


logging.set_verbosity_info()


def convert_small_transformer_checkpoint_to_pytorch(small_transformer_checkpoint_path, small_transformer_config_file, pytorch_dump_folder_path):
    # Construct model
    if small_transformer_config_file == "":
        config = SmallTransformerConfig()
    else:
        config = SmallTransformerConfig.from_json_file(small_transformer_config_file)
    model = SmallTransformerModel(config)

    # Load weights from numpy
    load_tf_weights_in_small_transformer(model, config, small_transformer_checkpoint_path)

    # Save pytorch-model
    pytorch_weights_dump_path = pytorch_dump_folder_path + "/" + WEIGHTS_NAME
    pytorch_config_dump_path = pytorch_dump_folder_path + "/" + CONFIG_NAME
    print(f"Save PyTorch model to {pytorch_weights_dump_path}")
    torch.save(model.state_dict(), pytorch_weights_dump_path)
    print(f"Save configuration file to {pytorch_config_dump_path}")
    with open(pytorch_config_dump_path, "w", encoding="utf-8") as f:
        f.write(config.to_json_string())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Required parameters
    parser.add_argument(
        "--small_transformer_checkpoint_path", default=None, type=str, required=True, help="Path to the TensorFlow checkpoint path."
    )
    parser.add_argument(
        "--pytorch_dump_folder_path", default=None, type=str, required=True, help="Path to the output PyTorch model."
    )
    parser.add_argument(
        "--small_transformer_config_file",
        default="",
        type=str,
        help=(
            "An optional config json file corresponding to the pre-trained OpenAI model. \n"
            "This specifies the model architecture."
        ),
    )
    args = parser.parse_args()
    convert_small_transformer_checkpoint_to_pytorch(args.small_transformer_checkpoint_path, args.small_transformer_config_file, args.pytorch_dump_folder_path)