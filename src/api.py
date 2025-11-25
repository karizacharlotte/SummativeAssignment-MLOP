from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
from pathlib import Path
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="PathMNIST Image Classifier API")
UPLOAD_DIR = Path("data/upload")


@app.on_event("startup")
async def startup_event():
    """Create upload directory when app starts"""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health")
async def health():
    """Simple health check endpoint"""
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict tissue type from uploaded image.
    Returns the predicted class and confidence score.
    """
    from src.prediction import predict_image_file
    
    # Save uploaded file temporarily
    temp = Path('temp')
    temp.mkdir(exist_ok=True)
    dest = temp / file.filename
    
    with dest.open('wb') as f:
        f.write(await file.read())
    
    try:
        # Get prediction
        result = predict_image_file(str(dest))
        return JSONResponse(result)
    finally:
        # Clean up temp file
        try:
            dest.unlink()
        except Exception:
            pass  # ignore if file doesn't exist


@app.post("/upload")
async def upload(files: list[UploadFile] = File(...)):
    """
    Upload multiple images for retraining.
    Files are saved to data/upload directory.
    """
    saved = []
    for file in files:
        dest = UPLOAD_DIR / file.filename
        with dest.open('wb') as f:
            f.write(await file.read())
        saved.append(str(dest))
    
    return {
        "saved": saved, 
        "message": f"Successfully uploaded {len(saved)} files. Use /retrain to retrain the model."
    }


@app.post("/retrain")
async def retrain(background_tasks: BackgroundTasks):
    """
    Trigger model retraining in the background.
    This doesn't block the API - training runs asynchronously.
    """
    from src.model import train_model_pathmnist
    
    # Start retraining as background task so API stays responsive
    background_tasks.add_task(train_model_pathmnist, 5, 32)
    
    return {"message": "Retraining started in background. Model will be updated when complete."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
