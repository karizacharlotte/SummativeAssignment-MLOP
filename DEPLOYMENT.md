# Deployment Guide - PathMNIST MLOps Project

This guide covers local Docker deployment, cloud deployment (Google Cloud Run), and load testing.

---

## Prerequisites

- Docker installed
- Google Cloud SDK (for cloud deployment)
- Python 3.10+ virtual environment
- At least 2GB free disk space

---

## Local Deployment

### Option 1: Direct Python (Development)

1. **Set up virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Train the model (if not already done):**
```bash
python -c "from src.model import train_model_pathmnist; train_model_pathmnist(epochs=3, batch_size=16, limit_samples=5000)"
```

4. **Run the API:**
```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000
```

5. **Run the UI (separate terminal):**
```bash
streamlit run ui/app.py --server.port 8501
```

6. **Access:**
   - API docs: http://localhost:8000/docs
   - Streamlit UI: http://localhost:8501

---

### Option 2: Docker (Production-like)

1. **Build the Docker image:**
```bash
docker build -t pathmnist-mlops:latest .
```

2. **Run the container:**
```bash
docker run -d \
  --name pathmnist-api \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data:/app/data \
  pathmnist-mlops:latest
```

3. **Test the deployment:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@data/samples/class_0_sample_0.png"
```

4. **View logs:**
```bash
docker logs -f pathmnist-api
```

5. **Stop the container:**
```bash
docker stop pathmnist-api
docker rm pathmnist-api
```

---

## Cloud Deployment (Google Cloud Run)

### Step 1: Prepare Google Cloud Project

1. **Install and authenticate Google Cloud SDK:**
```bash
gcloud init
gcloud auth login
```

2. **Set project ID:**
```bash
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID
```

3. **Enable required APIs:**
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 2: Build and Push Docker Image

1. **Configure Docker for Google Container Registry:**
```bash
gcloud auth configure-docker
```

2. **Build and tag the image:**
```bash
docker build -t gcr.io/$PROJECT_ID/pathmnist-mlops:v1 .
```

3. **Push to Google Container Registry:**
```bash
docker push gcr.io/$PROJECT_ID/pathmnist-mlops:v1
```

### Step 3: Deploy to Cloud Run

1. **Deploy the service:**
```bash
gcloud run deploy pathmnist-api \
  --image gcr.io/$PROJECT_ID/pathmnist-mlops:v1 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10 \
  --min-instances 1 \
  --port 8000
```

2. **Get the service URL:**
```bash
gcloud run services describe pathmnist-api \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

3. **Test the deployed service:**
```bash
SERVICE_URL=$(gcloud run services describe pathmnist-api --platform managed --region us-central1 --format 'value(status.url)')

curl -X POST "$SERVICE_URL/predict" \
  -F "file=@data/samples/class_0_sample_0.png"
```

### Step 4: Scale for Load Testing

1. **Update scaling configuration:**
```bash
gcloud run services update pathmnist-api \
  --min-instances 3 \
  --max-instances 20 \
  --concurrency 80
```

2. **Monitor scaling:**
```bash
gcloud run services list
```

---

## Load Testing with Locust

### Local Load Test

1. **Ensure API is running** (local or cloud)

2. **Run Locust (UI mode):**
```bash
locust -f locustfile.py --host http://localhost:8000
```

3. **Open browser:** http://localhost:8089

4. **Configure test:**
   - Number of users: 100
   - Spawn rate: 10 users/second
   - Host: http://localhost:8000

5. **Start test and monitor:**
   - Requests per second (RPS)
   - Response times (P50, P95, P99)
   - Failure rate

### Headless Load Test (for documentation)

**Test 1: Single Container (baseline)**
```bash
# 50 users, 30 second test
locust -f locustfile.py \
  --headless \
  -u 50 \
  -r 10 \
  --run-time 30s \
  --host http://localhost:8000 \
  --csv results/single_container
```

**Test 2: Scaled Deployment (3 containers)**
```bash
# Update Cloud Run to min 3 instances
gcloud run services update pathmnist-api --min-instances 3

# Run test against cloud URL
locust -f locustfile.py \
  --headless \
  -u 150 \
  -r 20 \
  --run-time 60s \
  --host $SERVICE_URL \
  --csv results/three_containers
```

**Test 3: High Load (10 containers)**
```bash
# Update Cloud Run to min 10 instances
gcloud run services update pathmnist-api --min-instances 10

# Run high-load test
locust -f locustfile.py \
  --headless \
  -u 500 \
  -r 50 \
  --run-time 60s \
  --host $SERVICE_URL \
  --csv results/ten_containers
```

### Analyze Results

**View CSV results:**
```bash
cat results/single_container_stats.csv
cat results/three_containers_stats.csv
cat results/ten_containers_stats.csv
```

**Compare latency and throughput:**
- Note P50, P95, P99 response times
- Calculate requests per second
- Record failure rates

**Expected metrics:**
- Single container: ~10-20 RPS, 100-200ms P95
- 3 containers: ~30-60 RPS, 80-150ms P95
- 10 containers: ~100-200 RPS, 50-100ms P95

---

## Monitoring in Production

### Cloud Run Metrics

1. **View metrics in Console:**
```bash
gcloud run services describe pathmnist-api \
  --platform managed \
  --region us-central1
```

2. **Check logs:**
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=pathmnist-api" \
  --limit 50 \
  --format json
```

### Custom Monitoring

Add to `src/api.py`:
```python
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    start_time = datetime.now()
    # ... existing code ...
    latency = (datetime.now() - start_time).total_seconds()
    logger.info(f"Prediction latency: {latency:.3f}s, result: {result['label']}")
    return JSONResponse(result)
```

---

## Cost Optimization

### Cloud Run Cost Estimates

- **Always-on (1 instance):** ~$15-30/month
- **Auto-scaling (0-10):** Pay per request, ~$0.40 per million requests
- **Recommendation:** Use min-instances=1 for demo, 0 for development

### Reduce costs:

1. **Use smaller instance:**
```bash
gcloud run services update pathmnist-api --memory 1Gi --cpu 1
```

2. **Reduce max instances:**
```bash
gcloud run services update pathmnist-api --max-instances 5
```

3. **Delete when not in use:**
```bash
gcloud run services delete pathmnist-api
```

---

## Troubleshooting

**Container fails to start:**
- Check logs: `docker logs pathmnist-api`
- Verify model exists: `ls -lh models/model.h5`
- Rebuild: `docker build --no-cache -t pathmnist-mlops:latest .`

**Cloud Run timeout:**
- Increase timeout: `--timeout 300`
- Check memory: `--memory 4Gi`

**Locust connection errors:**
- Verify API is accessible
- Check firewall rules for Cloud Run
- Use `--allow-unauthenticated` flag

**High latency:**
- Add more instances: `--min-instances 3`
- Increase CPU: `--cpu 4`
- Use GPU instances (if available)

---

## Cleanup

**Local:**
```bash
docker stop pathmnist-api
docker rm pathmnist-api
docker rmi pathmnist-mlops:latest
```

**Cloud:**
```bash
gcloud run services delete pathmnist-api
gcloud container images delete gcr.io/$PROJECT_ID/pathmnist-mlops:v1
```

---

## Next Steps for Production

- [ ] Add authentication (API keys, OAuth)
- [ ] Implement rate limiting
- [ ] Set up CI/CD pipeline (GitHub Actions, Cloud Build)
- [ ] Add model versioning
- [ ] Implement A/B testing
- [ ] Set up monitoring dashboards (Grafana, Cloud Monitoring)
- [ ] Configure auto-scaling policies
- [ ] Add caching layer (Redis)
