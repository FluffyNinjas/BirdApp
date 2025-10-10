import os

for split in ["train", "valid", "test"]:
    path = os.path.join("dataset_split", split)
    print(split, "→", len(os.listdir(path)), "folders")
