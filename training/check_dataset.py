import os

for split in ["train", "valid", "test"]:
    path = os.path.join("dataset_split", split)
    print(split, "→", len(os.listdir(path)), "folders")

import torch
print(torch.cuda.is_available())  # True means GPU is detected
print(torch.cuda.get_device_name(0))  # Shows the GPU name

