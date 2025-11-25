from pathlib import Path
import numpy as np
from PIL import Image
import tensorflow as tf


def save_upload(upload_file, dest_dir='data/upload'):
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    filepath = dest / upload_file.filename
    with filepath.open('wb') as f:
        f.write(upload_file.file.read())
    return str(filepath)


def load_and_preprocess_image(path, target_size=(96, 96)):
    """Load and preprocess a single image for PathMNIST model."""
    img = Image.open(path).convert('RGB').resize(target_size)
    arr = np.array(img).astype('float32') / 255.0
    return arr


def medmnist_to_tf(dataset, batch_size=32, target_size=(96, 96)):
    """Convert MedMNIST dataset to TensorFlow dataset."""
    images = []
    labels = []
    for img, lbl in dataset:
        img_array = np.array(img).astype('float32') / 255.0
        images.append(img_array)
        labels.append(lbl.item())
    images = np.array(images)
    labels = np.array(labels)
    # Resize images
    images_resized = tf.image.resize(images, target_size).numpy()
    # One-hot encode labels
    labels_onehot = tf.keras.utils.to_categorical(labels, num_classes=9)
    ds = tf.data.Dataset.from_tensor_slices((images_resized, labels_onehot))
    ds = ds.shuffle(1000).batch(batch_size).prefetch(tf.data.AUTOTUNE)
    return ds
