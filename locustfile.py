"""
Locust load test script for PathMNIST prediction API.
Usage:
  locust -f locustfile.py --headless -u 50 -r 5 --run-time 1m --host http://localhost:8000
"""
from locust import HttpUser, task, between
import random
from pathlib import Path

class PredictionUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def predict_image(self):
        # Use a sample image from data/samples/ if available
        samples_dir = Path("data/samples")
        if samples_dir.exists():
            sample_files = list(samples_dir.glob("*.png"))
            if sample_files:
                sample_file = random.choice(sample_files)
                with open(sample_file, "rb") as f:
                    files = {"file": (sample_file.name, f, "image/png")}
                    self.client.post("/predict", files=files)
            else:
                # Fallback: create a dummy image
                self.client.get("/health")
        else:
            self.client.get("/health")
