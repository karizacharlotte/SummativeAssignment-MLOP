#!/usr/bin/env python3
"""Download PathMNIST and perform quick EDA: save sample images and show class distribution."""
import os
from pathlib import Path
import numpy as np
from PIL import Image
import medmnist
from medmnist import PathMNIST

# Create data directories
Path('data/train').mkdir(parents=True, exist_ok=True)
Path('data/val').mkdir(parents=True, exist_ok=True)
Path('data/samples').mkdir(parents=True, exist_ok=True)

# Download PathMNIST (train and test splits)
print("Downloading PathMNIST dataset...")
train_dataset = PathMNIST(split='train', download=True, root='data/')
val_dataset = PathMNIST(split='val', download=True, root='data/')
test_dataset = PathMNIST(split='test', download=True, root='data/')

print(f"Train samples: {len(train_dataset)}")
print(f"Val samples: {len(val_dataset)}")
print(f"Test samples: {len(test_dataset)}")

# Get class labels
info = medmnist.INFO['pathmnist']
print(f"\nDataset: {info['task']}")
print(f"Number of classes: {info['n_channels']}, {info['label']}")
print(f"Labels: {info['label']}")

# Count class distribution in train
train_labels = [train_dataset[i][1].item() for i in range(len(train_dataset))]
unique, counts = np.unique(train_labels, return_counts=True)
print("\nClass distribution (train):")
for cls, cnt in zip(unique, counts):
    print(f"  Class {cls}: {cnt} samples")

# Save a few sample images per class (first 3 images of each class)
print("\nSaving sample images to data/samples/...")
saved_per_class = {c: 0 for c in unique}
for i in range(len(train_dataset)):
    img, label = train_dataset[i]
    label_int = label.item()
    if saved_per_class[label_int] < 3:
        # img is already a PIL Image
        if isinstance(img, Image.Image):
            img.save(f'data/samples/class_{label_int}_sample_{saved_per_class[label_int]}.png')
        else:
            img_pil = Image.fromarray(np.array(img))
            img_pil.save(f'data/samples/class_{label_int}_sample_{saved_per_class[label_int]}.png')
        saved_per_class[label_int] += 1
    if all(v >= 3 for v in saved_per_class.values()):
        break

print(f"Sample images saved in data/samples/")
print("\nEDA complete!")
