import os
from pathlib import Path
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import numpy as np
import pathlib


def build_model(num_classes=9, input_shape=(96, 96, 3)):
    """
    Build a transfer learning model using MobileNetV2.
    I'm using a pre-trained base to speed up training and improve accuracy.
    """
    # Load MobileNetV2 pre-trained on ImageNet
    base = MobileNetV2(weights='imagenet', include_top=False, input_shape=input_shape)
    
    # Freeze the base model layers - we don't want to retrain them
    base.trainable = False
    
    # Add custom classification head
    x = layers.GlobalAveragePooling2D()(base.output)
    x = layers.Dropout(0.3)(x)  # prevent overfitting
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.2)(x)  # additional regularization
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = models.Model(inputs=base.input, outputs=outputs)
    
    # Compile with Adam optimizer - tried different learning rates, 0.001 works best
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )
    return model


def train_model_pathmnist(epochs=3, batch_size=16, model_path='models/model.h5', limit_samples=5000):
    """
    Train the model on PathMNIST dataset.
    Using a subset of data to avoid memory issues on my laptop.
    """
    from medmnist import PathMNIST
    import src.preprocessing as prep
    
    # Make sure models directory exists
    pathlib.Path('models').mkdir(parents=True, exist_ok=True)
    
    # Download and load the dataset
    print("Loading PathMNIST dataset...")
    train_dataset = PathMNIST(split='train', download=True, root='data/')
    val_dataset = PathMNIST(split='val', download=True, root='data/')
    
    # Limit training samples to prevent running out of memory
    # Full dataset is too large for my system
    if limit_samples and len(train_dataset) > limit_samples:
        print(f"Using {limit_samples} samples instead of full {len(train_dataset)} to save memory")
        indices = np.random.choice(len(train_dataset), limit_samples, replace=False)
        train_dataset.imgs = train_dataset.imgs[indices]
        train_dataset.labels = train_dataset.labels[indices]
    
    # Convert to TensorFlow format
    train_tf = prep.medmnist_to_tf(train_dataset, batch_size=batch_size)
    val_tf = prep.medmnist_to_tf(val_dataset, batch_size=batch_size)
    
    # Build the model
    print("Building model...")
    model = build_model()
    
    # Setup callbacks for better training
    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True, monitor='val_loss'),
        ModelCheckpoint(model_path, save_best_only=True, monitor='val_accuracy')
    ]
    
    # Train the model
    print(f"Training for {epochs} epochs...")
    history = model.fit(
        train_tf,
        epochs=epochs,
        validation_data=val_tf,
        callbacks=callbacks
    )
    
    # Save final model
    model.save(model_path)
    print(f"Model saved to {model_path}")
    
    # Save class names for later use in predictions
    import medmnist
    info = medmnist.INFO['pathmnist']
    class_names = list(info['label'].values())
    with open('models/classes.txt', 'w') as f:
        f.write('\n'.join(class_names))
    
    return model, history


def evaluate_model(model, dataset):
    """Evaluate model on a TensorFlow dataset."""
    from sklearn.metrics import classification_report, confusion_matrix
    y_true = []
    y_pred = []
    for x, y in dataset:
        preds = model.predict(x, verbose=0)
        y_pred.extend(np.argmax(preds, axis=1).tolist())
        y_true.extend(np.argmax(y.numpy(), axis=1).tolist())
    report = classification_report(y_true, y_pred, output_dict=True)
    cm = confusion_matrix(y_true, y_pred)
    return report, cm


if __name__ == '__main__':
    train_model_pathmnist(epochs=10)
