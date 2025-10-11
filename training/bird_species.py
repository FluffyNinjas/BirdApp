import os

# Path to the downloaded dataset’s “images” folder (adjust accordingly)
images_dir = "dataset/CUB_200_2011/images"

# List all subdirectories (these are your species labels)
species = [d for d in os.listdir(images_dir) if os.path.isdir(os.path.join(images_dir, d))]

# Optionally sort them
species.sort()

# Write to a file
with open("birds.txt", "w") as f:
    for label in species:
        f.write(label + "\n")

print(f"Wrote {len(species)} species to birds.txt")
