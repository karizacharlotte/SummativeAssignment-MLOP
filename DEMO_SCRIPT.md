# Demo Video Script - Quick Guide

**Length:** 3-5 minutes  
**Remember:** Camera ON, clear audio, be yourself!

---

## Opening (10-15 seconds)
"Hi, I'm [your name] and this is my MLOps summative project. I built an image classification system for medical tissue images using the PathMNIST dataset. It can predict tissue types and retrain itself with new data. Let me show you how it works."

---

## Part 1: Making a Prediction (1-2 minutes)

### Show the Interface
1. Open your browser to `http://localhost:8501`
2. You should see the Streamlit dashboard

### Do a Prediction
1. Click on "Predict" in the sidebar
2. Say: "First, let me show you the prediction feature. I'm going to upload a sample image..."
3. Click "Choose an image file" and select one from `data/samples/`
4. Click "Classify Image"
5. Point out: "As you can see, the model predicted [tissue type] with [X]% confidence. This is correct based on the sample class."

### Alternative Demo (API)
If you want to also show the API:
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@data/samples/class_0_sample_0.png"
```
Say: "I can also call the API directly which returns JSON with the label and confidence."

---

## Part 2: Uploading Data for Retraining (1 minute)

1. Click "Upload Data" in the sidebar
2. Say: "Now I'll show the data upload feature. This is where users can add new training data."
3. Click "Browse files" and select 3-5 images from `data/samples/`
4. Click "Upload Files"
5. Point out: "The files are now saved in the upload directory and ready for retraining."

---

## Part 3: Triggering Retraining (1 minute)

1. Click "Retrain Model" in the sidebar
2. Say: "Now I can retrain the model with the uploaded data. This uses transfer learning with MobileNetV2."
3. Click "Start Retraining" button
4. Point out: "Retraining has started in the background as you can see from the message. The model uses early stopping and saves the best version automatically."
5. Briefly explain: "The retraining pipeline includes data preprocessing, using the pre-trained model as a base, and saving the updated model when complete."

---

## Part 4: Show Data Insights (30 seconds)

1. Click "Data Insights"
2. Say: "Here are some visualizations showing the dataset..."
3. Point out the class distribution chart and sample images
4. Mention: "This helps understand if the data is balanced across the 9 tissue classes."

---

## Closing (10 seconds)
"So that's my project - a complete MLOps pipeline with prediction, retraining, visualizations, and API access. Everything is containerized with Docker and ready to deploy. Thanks for watching!"

---

## Quick Checklist Before Recording

- [ ] API running (check http://localhost:8000/health)
- [ ] Streamlit running (check http://localhost:8501)
- [ ] Camera works and you're visible
- [ ] Audio is clear
- [ ] Sample images ready in `data/samples/`
- [ ] You look presentable

---

## Tips

- **Be natural** - don't memorize this word-for-word, just use it as a guide  
- **Smile** - you've built something cool!  
- **If something goes wrong** - pause, fix it, and keep going  
- **Speak clearly** - pretend you're explaining to a classmate  
- **Keep it simple** - you don't need to explain every technical detail  

Good luck!

---

## Part 1: Prediction Process (1.5 minutes)

### Show the UI
1. Open browser to `http://localhost:8501` (Streamlit UI)
2. Navigate to "🔮 Predict" page

### Single Image Prediction
1. Click "Browse files" and select a sample image from `data/samples/`
2. Upload the image
3. **Point out:** "The model correctly predicts the tissue type with confidence score"
4. **Show result:** Label (e.g., "adipose") and confidence percentage

### Alternative: API Prediction
1. Open terminal
2. Run:
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@data/samples/class_0_sample_0.png"
```
3. **Point out:** "API returns JSON with label and confidence - this is what production clients would use"

---

## Part 2: Data Upload for Retraining (1 minute)

### Bulk Upload
1. Navigate to "📤 Upload Data" page in Streamlit UI
2. Click "Browse files" and select multiple images from `data/samples/` (select 5-10 images)
3. Click "Upload"
4. **Point out:** "These images are saved to `data/upload/` and will be used for retraining"
5. **Show confirmation:** Number of files uploaded

### Alternative: API Upload
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "files=@data/samples/class_1_sample_0.png" \
  -F "files=@data/samples/class_2_sample_0.png"
```

---

## Part 3: Trigger Retraining (1.5 minutes)

### UI Retraining
1. Navigate to "🔄 Retrain Model" page
2. **Explain:** "This triggers retraining using uploaded data and saves a new model"
3. Click "Start Retraining" button
4. **Point out:** Background task starts (FastAPI BackgroundTasks)
5. **Show:** "Retraining started" message

### Monitor Progress
1. Check terminal logs or `api.log`
2. **Explain:** "Model is training with early stopping and checkpoint saving"
3. **Point out:** New model saved to `models/model.h5`

### Alternative: API Retrain
```bash
curl -X POST "http://localhost:8000/retrain"
```

---

## Part 4: Visualizations & Insights (30 seconds)

1. Navigate to "📊 Data Insights" page
2. **Show:**
   - Class distribution bar chart (9 tissue types)
   - Sample images grid
   - Model uptime indicator
3. **Explain:** "These visualizations help understand dataset balance and model performance"

---

## Part 5: Load Testing with Locust (Optional, 30 seconds)

1. Open terminal and run:
```bash
locust -f locustfile.py --headless -u 50 -r 10 --run-time 30s --host http://localhost:8000
```
2. **Point out:** Requests per second, response times, and failure rate
3. **Explain:** "This simulates production load to measure latency and throughput"

---

## Closing (15 seconds)
"This system demonstrates a complete MLOps pipeline: data upload, preprocessing, model training with optimization techniques, prediction API, retraining workflow, and monitoring. Thank you!"

---

## Pre-Recording Checklist

- [ ] API running (`uvicorn src.api:app --port 8000`)
- [ ] Streamlit UI running (`streamlit run ui/app.py`)
- [ ] Sample images available in `data/samples/`
- [ ] Model trained and saved at `models/model.h5`
- [ ] Camera and microphone working
- [ ] Screen recording software ready (OBS, QuickTime, etc.)

---

## Tips for Full Marks

✅ **Camera on** throughout recording  
✅ **Clear audio** - speak clearly and explain each step  
✅ **Show both UI and API** demonstrations  
✅ **Highlight retraining workflow**: upload → preprocess → retrain  
✅ **Point out technical details**: early stopping, transfer learning, background tasks  
✅ **Show visualizations** for data insights  
✅ **Professional presentation** - no errors, smooth flow

---

## Troubleshooting

**API not responding?**
```bash
pkill -f uvicorn
uvicorn src.api:app --port 8000
```

**Streamlit not loading?**
```bash
streamlit run ui/app.py --server.port 8501
```

**Model not found?**
```bash
python -c "from src.model import train_model_pathmnist; train_model_pathmnist(epochs=3)"
```
