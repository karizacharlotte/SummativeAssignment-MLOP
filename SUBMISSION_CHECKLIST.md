# Final Submission Checklist - Full Marks Guide

Use this checklist to ensure you meet ALL rubric requirements for maximum marks.

---

## Video Demo (5/5 points)

**Requirement:** Clear, user-friendly demo with camera on showing prediction and retraining

### Pre-Recording Checklist
- [ ] Camera working and positioned correctly
- [ ] Microphone clear (test audio)
- [ ] API running: `uvicorn src.api:app --port 8000`
- [ ] Streamlit UI running: `streamlit run ui/app.py`
- [ ] Screen recording software ready (OBS Studio, QuickTime, etc.)
- [ ] `DEMO_SCRIPT.md` reviewed

### Demo Content (3-5 minutes)
- [ ] **Introduction** with camera on (say your name, project title)
- [ ] **Prediction demonstration:**
  - [ ] Show single image upload via Streamlit UI
  - [ ] Display prediction result with label and confidence
  - [ ] Optionally show API prediction via curl
- [ ] **Retraining demonstration:**
  - [ ] Upload multiple images (5-10) via UI
  - [ ] Click "Start Retraining" button
  - [ ] Explain background task and model saving
- [ ] **Visualizations:** Show data insights page (class distribution, samples)
- [ ] Camera visible throughout recording
- [ ] Clear audio explaining each step

### After Recording
- [ ] Upload to YouTube (unlisted or public)
- [ ] Add YouTube link to `README.md` (replace `[YouTube Demo Link]`)
- [ ] Verify video is accessible and playable

---

## Retraining Process (10/10 points)

**Requirement:** Data upload, preprocessing, and retraining using custom pre-trained model

### Evidence Required
- [ ] **Script present:** `src/model.py` contains `train_model_pathmnist()`
- [ ] **Model file present:** `models/model.h5` exists (trained model)
- [ ] **Classes file:** `models/classes.txt` exists (tissue type labels)

### Functionality Checklist
- [ ] **Data upload endpoint:** `/upload` in `src/api.py` saves files to `data/upload/`
- [ ] **Preprocessing:** `src/preprocessing.py` loads and preprocesses images (resize to 96×96, normalize)
- [ ] **Retraining trigger:** `/retrain` endpoint calls `train_model_pathmnist()` in background
- [ ] **Pre-trained model used:** MobileNetV2 with ImageNet weights (transfer learning)
- [ ] **Model saves after retraining:** Updates `models/model.h5`

### Demo Verification
- [ ] Show file upload in video demo
- [ ] Show "Retraining started" message after clicking button
- [ ] Explain that model is saved to `models/model.h5`

---

## Prediction Process (10/10 points)

**Requirement:** Single data point prediction with CORRECT label display

### Evidence Required
- [ ] **Script present:** `src/prediction.py` with `predict_image_file()`
- [ ] **Model file present:** `models/model.h5` (same as above)

### Functionality Checklist
- [ ] **Prediction endpoint:** `/predict` in `src/api.py` accepts image upload
- [ ] **Single image upload:** UI and API support uploading one image
- [ ] **Correct prediction:** Display matches ground truth (test with known samples)
- [ ] **Confidence score:** Show probability/confidence percentage

### Demo Verification
- [ ] Upload a sample image (e.g., `data/samples/class_0_sample_0.png`)
- [ ] Verify predicted label is correct (e.g., "adipose" for class 0)
- [ ] Show confidence score (e.g., 89.98%)

---

## Evaluation of Models (10/10 points)

**Requirement:** Notebook with preprocessing, optimization, and 4+ metrics

### Evidence Required
- [ ] **Notebook present:** `notebook/pathmnist_classification.ipynb`

### Notebook Content Checklist
- [ ] **Preprocessing steps:**
  - [ ] Data loading from MedMNIST
  - [ ] Image resizing (28×28 → 96×96)
  - [ ] Normalization (MobileNetV2 preprocessing)
  - [ ] Train/val split
- [ ] **Optimization techniques:**
  - [ ] Transfer learning (MobileNetV2 pre-trained on ImageNet)
  - [ ] Early stopping (patience=5, monitor='val_loss')
  - [ ] Model checkpointing (save best model)
  - [ ] Adam optimizer with learning rate 0.001
  - [ ] Dropout layers (0.3, 0.2)
- [ ] **Evaluation metrics (4+ required):**
  - [ ] Accuracy
  - [ ] Precision
  - [ ] Recall
  - [ ] F1-score
  - [ ] Confusion matrix (bonus)
  - [ ] ROC curves (bonus)

### Run Notebook
- [ ] Execute all cells without errors
- [ ] Generate plots (class distribution, sample images, confusion matrix)
- [ ] Save outputs (metrics tables, plots)

---

## Deployment Package (10/10 points)

**Requirement:** UI (web/mobile) with data insights, or API with demo tools

### Evidence Required
- [ ] **Streamlit UI:** `ui/app.py` with multiple pages
- [ ] **Dockerfile:** Present and builds successfully
- [ ] **API running:** Accessible via localhost:8000 or cloud URL

### UI Features Checklist
- [ ] **Prediction page:** Upload single image, display result
- [ ] **Upload page:** Bulk upload multiple images
- [ ] **Retrain page:** Button to trigger retraining
- [ ] **Data insights page:** Visualizations (class distribution, sample images, uptime)
- [ ] **Model uptime:** Show timestamp or status

### Data Insights Visualizations
- [ ] Class distribution bar chart (9 tissue types)
- [ ] Sample images grid (at least 3 classes shown)
- [ ] Additional: pixel intensity distribution, image dimensions, etc.

### Deployment Options
**Option 1: Streamlit UI (recommended for full marks)**
- [ ] Run: `streamlit run ui/app.py`
- [ ] Accessible at http://localhost:8501
- [ ] Show in demo video

**Option 2: API + Swagger UI**
- [ ] FastAPI auto-generated docs at http://localhost:8000/docs
- [ ] Show in demo video (less preferred than custom UI)

**Option 3: Cloud Deployment (bonus)**
- [ ] Deploy to Google Cloud Run / Heroku / AWS
- [ ] Add public URL to `README.md`
- [ ] Demonstrate in video

---

## Additional Documentation Requirements

### README.md
- [ ] YouTube demo link added
- [ ] Cloud URL added (if deployed)
- [ ] Clear setup instructions
- [ ] Dependencies listed (`requirements.txt`)
- [ ] How to run locally (venv, pip install, uvicorn, streamlit)
- [ ] Project description (PathMNIST, 9 classes, MobileNetV2)

### GitHub Repository
- [ ] All code pushed to GitHub
- [ ] `models/model.h5` included (or .gitignore if too large, with download instructions)
- [ ] `data/samples/` included (sample images for demo)
- [ ] Clean commit history
- [ ] No sensitive data (API keys, passwords)

### Locust Load Test Results
- [ ] `LOAD_TEST_RESULTS.md` present
- [ ] Run actual tests and update with real numbers
- [ ] Screenshots of Locust dashboard (optional but impressive)

---

## 🏆 Grading Breakdown Estimate

| Criteria                  | Max Points | Your Score | Status |
|---------------------------|-----------|------------|--------|
| Video Demo                | 5         | ___        | ⬜     |
| Retraining Process        | 10        | ___        | ⬜     |
| Prediction Process        | 10        | ___        | ⬜     |
| Evaluation of Models      | 10        | ___        | ⬜     |
| Deployment Package        | 10        | ___        | ⬜     |
| **Total**                 | **45**    | ___        | ⬜     |

---

## 🚦 Quick Validation Tests

Run these commands to verify everything works before recording demo:

### 1. API Health Check
```bash
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

### 2. Prediction Test
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@data/samples/class_0_sample_0.png"
# Expected: {"label":"adipose","confidence":0.89...}
```

### 3. Upload Test
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "files=@data/samples/class_1_sample_0.png" \
  -F "files=@data/samples/class_2_sample_0.png"
# Expected: {"saved":[...],"message":"..."}
```

### 4. Retrain Test
```bash
curl -X POST "http://localhost:8000/retrain"
# Expected: {"message":"Retraining started in background"}
```

### 5. UI Test
```bash
# Open browser to http://localhost:8501
# Verify all pages load without errors
```

### 6. Model File Check
```bash
ls -lh models/model.h5
# Expected: File exists, ~15-30 MB
```

### 7. Notebook Run
```bash
# Open notebook/pathmnist_classification.ipynb
# Run all cells (Kernel → Restart & Run All)
# Verify no errors
```

---

## 🎯 Final Pre-Submission Checklist

**48 hours before deadline:**
- [ ] All code working locally
- [ ] Model trained and saved
- [ ] Notebook runs without errors
- [ ] API and UI tested

**24 hours before deadline:**
- [ ] Record demo video (camera on)
- [ ] Upload to YouTube
- [ ] Update README with YouTube link
- [ ] Push all code to GitHub

**12 hours before deadline:**
- [ ] Review video (re-record if needed)
- [ ] Verify GitHub repo is public and complete
- [ ] Test clone repo in new directory (verify setup instructions work)
- [ ] Submit GitHub link

**Before final submission:**
- [ ] Double-check YouTube link works
- [ ] Verify all files are pushed
- [ ] Ensure `models/model.h5` is accessible (or documented how to generate)
- [ ] Confirm video shows camera and demonstrates all requirements

---

## Tips for Full Marks

### Video Demo
- **Camera on throughout** - this is explicitly required
- **Clear audio** - use headphones mic if needed
- **Professional** - dress presentably, clear background
- **Rehearse** - practice demo script 2-3 times
- **Confidence** - speak clearly and explain technical details

### Retraining
- **Show the pipeline** - upload → save → preprocess → retrain → save model
- **Explain transfer learning** - mention MobileNetV2 pre-trained weights
- **Point out optimization** - early stopping, checkpointing

### Prediction
- **Use known samples** - ensure prediction is correct for demo
- **Show confidence** - high confidence (>70%) looks better
- **Multiple predictions** - show 2-3 examples if time permits

### Evaluation
- **Run notebook before demo** - ensure all cells execute
- **Save outputs** - include plots in notebook for grader review
- **Interpret metrics** - briefly explain what precision/recall mean

### Deployment
- **Streamlit UI preferred** - more visual than API docs
- **Show visualizations** - data insights are explicitly required
- **Consider cloud deployment** - bonus points for public URL

---

## Common Issues & Fixes

**"Model file not found"**
```bash
python -c "from src.model import train_model_pathmnist; train_model_pathmnist(epochs=3)"
```

**"API not responding"**
```bash
pkill -f uvicorn
uvicorn src.api:app --port 8000
```

**"Streamlit not loading"**
```bash
pip install streamlit
streamlit run ui/app.py --server.port 8501
```

**"Out of memory during training"**
- Already handled with `limit_samples=5000` and `batch_size=16`

**"Docker build fails"**
```bash
docker build --no-cache -t pathmnist-mlops:latest .
```

---

## 📞 Need Help?

- Review `DEMO_SCRIPT.md` for detailed recording guide
- Check `DEPLOYMENT.md` for Docker and cloud deployment
- See `LOAD_TEST_RESULTS.md` for Locust testing examples
- All code is documented with comments

**You have everything needed for full marks!** 🎓

Good luck with your submission!
