import sys
import transformers
print("Python executable:", sys.executable)
print("Transformers version:", transformers.__version__)
print("Transformers path:", transformers.__file__)
from datasets import load_dataset
from transformers import AutoImageProcessor, AutoModelForImageClassification, TrainingArguments, Trainer
import numpy as np
from sklearn.metrics import accuracy_score

# 1. Load dataset (points to your local dataset folder)
dataset = load_dataset("imagefolder", data_dir="dataset")

# Debug: print available splits
print("Available splits:", dataset.keys())
print(dataset["train"].features["label"])

# 2. Load pretrained model + processor
model_name = "google/vit-base-patch16-224"
processor = AutoImageProcessor.from_pretrained(model_name)
labels = dataset["train"].features["label"].names

model = AutoModelForImageClassification.from_pretrained(
    "google/vit-base-patch16-224",
    num_labels=3,  # number of bird classes in your dataset
    id2label={0: "bluejay", 1: "cardinal", 2: "sparrow"},
    label2id={"bluejay": 0, "cardinal": 1, "sparrow": 2},
    ignore_mismatched_sizes=True  
)

# 3. Preprocess function
def preprocess(examples):
    # Process images
    inputs = processor(examples["image"], return_tensors="pt")
    # Add labels
    inputs["labels"] = examples["label"]
    return inputs

# Apply preprocessing
prepared_ds = dataset.map(preprocess, batched=True, remove_columns=["image"])

# 4. Training setup
training_args = TrainingArguments(
    output_dir="bird_model",
    eval_strategy="epoch",  
    save_strategy="epoch",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    logging_dir="./logs",
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
trainer.train()

# 8. Save
trainer.save_model("bird_model")
processor.save_pretrained("bird_model")