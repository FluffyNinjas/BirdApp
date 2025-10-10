import os, shutil, random

base_dir = "dataset/CUB_200_2011/images"
output_dir = "dataset_split"
os.makedirs(output_dir, exist_ok=True)

for split in ["train", "valid", "test"]:
    os.makedirs(os.path.join(output_dir, split), exist_ok=True)

for species in os.listdir(base_dir):
    species_path = os.path.join(base_dir, species)
    if not os.path.isdir(species_path):
        continue

    images = [f for f in os.listdir(species_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    random.shuffle(images)

    n = len(images)
    train_split = int(0.8 * n)
    valid_split = int(0.1 * n)

    for i, img in enumerate(images):
        if i < train_split:
            split = "train"
        elif i < train_split + valid_split:
            split = "valid"
        else:
            split = "test"

        dest_dir = os.path.join(output_dir, split, species)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy(os.path.join(species_path, img), os.path.join(dest_dir, img))

print("Done splitting into train/valid/test folders under 'dataset_split/'")
