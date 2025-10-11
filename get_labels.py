
from transformers import AutoModelForImageClassification
from pathlib import Path

# Path to your trained model
model_dir = Path("training") / "bird_model"

# Load the model
model = AutoModelForImageClassification.from_pretrained(model_dir)

# Get the labels
labels = model.config.id2label.values()

# Print the labels
for label in labels:
    print(label)
