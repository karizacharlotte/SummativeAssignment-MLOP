from pathlib import Path
import numpy as np
from tensorflow.keras.models import load_model
import src.preprocessing as prep

MODEL_PATH = 'models/model.h5'
CLASSES_FILE = 'models/classes.txt'

_model = None
_classes = None


def load_saved_model(path=MODEL_PATH):
    global _model, _classes
    if Path(path).exists():
        _model = load_model(path)
    else:
        raise FileNotFoundError(f"Model file not found at {path}")
    if Path(CLASSES_FILE).exists():
        _classes = Path(CLASSES_FILE).read_text().splitlines()
    return _model


def predict_image_file(path):
    """Predict label for a single image file (PathMNIST format: 96x96)."""
    global _model, _classes
    if _model is None:
        load_saved_model()
    arr = prep.load_and_preprocess_image(path, target_size=(96, 96))
    arr = np.expand_dims(arr, axis=0)
    preds = _model.predict(arr, verbose=0)
    idx = int(np.argmax(preds, axis=1)[0])
    label = _classes[idx] if _classes else str(idx)
    confidence = float(np.max(preds))
    return {"label": label, "confidence": confidence}
