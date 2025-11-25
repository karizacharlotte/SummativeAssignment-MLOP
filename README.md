# PathMNIST Image Classification - MLOps Summative Assignment

This is my MLOps summative project that demonstrates a complete machine learning pipeline for medical image classification using the PathMNIST dataset.

---

## Video Demo
> **[YouTube Demo Link]** _(Add your YouTube link here after recording)_

## Deployed URL
> **http://localhost:8501** - Streamlit Web UI (Local Deployment)

---

## About This Project

I built an end-to-end MLOps pipeline for classifying histology tissue images using the PathMNIST dataset. The system can:

- **Classify images** into 9 different tissue types (adipose, background, debris, lymphocytes, mucus, smooth muscle, normal colon mucosa, cancer-associated stroma, colorectal adenocarcinoma epithelium)
- **Retrain itself** when new data is uploaded
- **Serve predictions** through both a REST API and web interface
- **Scale automatically** when deployed to the cloud

### What I Used:
- **Dataset:** PathMNIST - 89,996 training images, 10,004 validation images
- **Model:** Transfer learning with MobileNetV2 (pre-trained on ImageNet)
- **Results:** 75.37% validation accuracy, 83.69% precision, 66.69% recall
- **Technology Stack:** 
  - TensorFlow/Keras for deep learning
  - FastAPI for the REST API
  - Streamlit for the web UI
  - Docker for containerization
  - Locust for load testing

---

## What's In This Repo

```
Summative assignment - MLOP/
├── README.md                   # You're reading this!
├── requirements.txt            # All Python packages needed
├── Dockerfile                  # For building the Docker container
├── app.py                      # Streamlit web interface
├── locustfile.py               # Load testing configuration
├── notebook/
│   └── pathmnist_classification.ipynb   # My full analysis and model training
├── src/
│   ├── preprocessing.py        # Functions to prepare images
│   ├── model.py                # Model architecture and training code
│   ├── prediction.py           # Prediction logic
│   └── api.py                  # FastAPI endpoints
├── data/
│   ├── samples/                # Example images
│   └── upload/                 # Where uploaded images go
└── models/
    ├── model.h5                # Trained model (12MB)
    └── classes.txt             # List of tissue types
```
    ├── model.h5                # Trained Keras model
    └── classes.txt             # Class label mapping
```

---

## How to Run This Project

### Step 1: Get the Code

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd "Summative assignment - MLOP"
```

### Step 2: Set Up Python Environment

I used Python 3.10 for this project. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

This will install TensorFlow, FastAPI, Streamlit, and other dependencies.

### Step 4: Get the Dataset

The PathMNIST dataset downloads automatically when you run the training script or notebook. But if you want to download it separately:

```bash
python download_and_eda.py
```

This saves sample images to `data/samples/` and shows the class distribution.

### Step 5: Train the Model

You can either:

**Option A: Use the Jupyter Notebook** (recommended to see my full analysis)
- Open `notebook/pathmnist_classification.ipynb`
- Run all cells to see EDA, training, and evaluation

**Option B: Train via command line**
```bash
python -c "from src.model import train_model_pathmnist; train_model_pathmnist(epochs=10)"
```

The trained model gets saved to `models/model.h5`.

### Step 6: Start the API Server

```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000
```

Now you can test the API:
- Go to `http://localhost:8000/docs` to see the API documentation
- `/predict` - upload an image to get predictions
- `/upload` - upload multiple images for retraining
- `/retrain` - trigger model retraining

### Step 7: Launch the Web Interface

In a new terminal (keep the API running):

```bash
streamlit run app.py
```

UI will open at `http://localhost:8501`. Features:
- **Predict:** Upload single image and get prediction
- **Visualizations:** View class distribution, sample images, confusion matrix
- **Upload & Retrain:** Bulk upload images and trigger retraining
- **Model Info:** Check API uptime and model details

---

## 🐳 Docker Instructions

### Build Docker Image

```bash
docker build -t pathmnist-classifier .
```

### Run Container Locally

```bash
docker run -p 8000:8000 pathmnist-classifier
```

### Test Prediction

```bash
curl -F "file=@data/samples/class_0_sample_0.png" http://localhost:8000/predict
```

---

## Cloud Deployment (Google Cloud Run)

### Prerequisites
- Google Cloud account
- `gcloud` CLI installed and authenticated

### Steps

1. **Build and push to Google Container Registry:**

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/pathmnist-classifier
```

2. **Deploy to Cloud Run:**

```bash
gcloud run deploy pathmnist-classifier \
  --image gcr.io/YOUR_PROJECT_ID/pathmnist-classifier \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2
```

3. **Get the deployed URL:**

```bash
gcloud run services describe pathmnist-classifier --region us-central1 --format 'value(status.url)'
```

4. **Test deployed API:**

```bash
curl -F "file=@data/samples/class_0_sample_0.png" https://YOUR_CLOUD_RUN_URL/predict
```

---

## 🧪 Load Testing with Locust

### Run Locust Locally

```bash
locust -f locustfile.py --headless -u 100 -r 10 --run-time 2m --host http://localhost:8000
```

Parameters:
- `-u 100` → 100 concurrent users
- `-r 10` → Spawn 10 users per second
- `--run-time 2m` → Run for 2 minutes

### Results

Locust will output:
- **Requests per second (RPS)**
- **Average latency**
- **95th percentile latency**
- **Failure rate**

Save results to CSV:

```bash
locust -f locustfile.py --headless -u 100 -r 10 --run-time 2m --host http://localhost:8000 --csv results
```

### Multi-Container Load Testing (Cloud Run)

Cloud Run autoscales based on traffic. Test with different container counts by adjusting `--max-instances`:

```bash
gcloud run services update pathmnist-classifier --max-instances 5
```

Run Locust targeting your Cloud Run URL and compare latency/throughput for 1, 3, 5 instances.

---

## Results from Flood Request Simulation

| Container Count | Users | RPS | Avg Latency (ms) | 95th Percentile (ms) | Failure Rate |
|-----------------|-------|-----|------------------|----------------------|--------------|
| 1               | 50    | 12  | 250              | 450                  | 0%           |
| 3               | 100   | 35  | 180              | 320                  | 0%           |
| 5               | 200   | 68  | 160              | 280                  | 0.1%         |

*(Replace with actual results after running load tests)*

---

## 📓 Notebook Highlights

`notebook/pathmnist_classification.ipynb` includes:

1. **Data Acquisition:** Download PathMNIST dataset
2. **EDA:**
   - Feature 1: Class distribution (bar plot)
   - Feature 2: Sample images per class (grid)
   - Feature 3: Image size and pixel value range
3. **Preprocessing:** Resize 28×28 → 96×96, normalize to [0,1]
4. **Model Training:** MobileNetV2 transfer learning with early stopping, dropout
5. **Evaluation:**
   - Accuracy, Precision, Recall, F1-score
   - Confusion matrix heatmap
   - Training history plots

---
## What I Used

**Machine Learning:**
- TensorFlow/Keras for the deep learning model
- MobileNetV2 (pre-trained on ImageNet) for transfer learning
- scikit-learn for evaluation metrics
- MedMNIST library for the PathMNIST dataset

**Backend & API:**
- FastAPI to create the REST API
- Uvicorn as the ASGI server

**Frontend:**
- Streamlit for the web dashboard

**DevOps:**
- Docker for containerization
- Locust for load testing
- Git for version control

**Visualization:**
- Matplotlib and Seaborn for charts
- PIL for image processing

---

## Acknowledgments

- **MedMNIST Team** for providing the PathMNIST dataset
- **TensorFlow/Keras** documentation and tutorials
- **FastAPI** and **Streamlit** communities for great frameworks

---

## License

This is an educational project for my MLOps summative assignment.  
Feel free to use it as a reference, but please don't copy it directly for your own coursework!

---

**Made with coffee and late nights for MLOps Summative 2025**

## 👤 Author

**Your Name**  
GitHub: [@yourusername](https://github.com/yourusername)

---

## 📚 References

- [MedMNIST](https://medmnist.com/)
- [TensorFlow/Keras](https://www.tensorflow.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [Locust](https://locust.io/)
