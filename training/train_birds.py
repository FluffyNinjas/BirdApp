import sys
import transformers
print("Python executable:", sys.executable)
print("Transformers version:", transformers.__version__)
print("Transformers path:", transformers.__file__)
from datasets import load_dataset
from transformers import AutoImageProcessor, AutoModelForImageClassification, TrainingArguments, Trainer
import numpy as np
from sklearn.metrics import accuracy_score
from PIL import Image

# 1. Load dataset (points to your local dataset folder)
dataset = load_dataset("imagefolder", data_dir="dataset_split")

# Debug: print available splits
print("Available splits:", dataset.keys())
print(dataset["train"].features["label"])

# 2. Load pretrained model + processor
model_name = "google/vit-base-patch16-224"
processor = AutoImageProcessor.from_pretrained(model_name)
labels = dataset["train"].features["label"].names

labels = dataset["train"].features["label"].names
id2label = {i: label for i, label in enumerate(labels)}
label2id = {label: i for i, label in enumerate(labels)}

model = AutoModelForImageClassification.from_pretrained(
    model_name,
    num_labels=len(labels),  # number of bird classes in your dataset
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True
)

# 3. Preprocess function
def preprocess(examples):
    # Ensure every image is RGB
    images = []
    for img in examples["image"]:
        if img.mode != "RGB":
            img = img.convert("RGB")
        images.append(img)
    # Process with the ViT processor
    return processor(images, return_tensors="pt")

# Apply preprocessing
prepared_ds = dataset.map(preprocess, batched=True, remove_columns=["image"])

# 4. Training setup
training_args = TrainingArguments(
    output_dir="bird_model",
    eval_strategy="epoch",  
    save_strategy="epoch",
    num_train_epochs=5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    logging_dir="./logs",
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)

# 5. Metric
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {"accuracy": accuracy_score(labels, preds)}

# 6. Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=prepared_ds["train"],
    eval_dataset=prepared_ds["validation"],
    compute_metrics=compute_metrics,
)

# 7. Train
trainer.train(resume_from_checkpoint=True)

# 8. Save
trainer.save_model("bird_model")
processor.save_pretrained("bird_model")