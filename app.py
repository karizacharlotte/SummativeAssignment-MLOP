"""
PathMNIST Image Classifier - Web Interface
This is my Streamlit dashboard for the MLOps project.
It lets you predict images, view data, and trigger retraining.
"""
import streamlit as st
import requests
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
import time
import os

# API endpoint - change this if deployed to cloud
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="PathMNIST Classifier", layout="wide")

st.title("PathMNIST Tissue Classifier")
st.write("*MLOps Summative Project - Image Classification Dashboard*")

# Navigation sidebar
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Predict", "Data Insights", "Upload Data", "Retrain Model", "About"]
)

# --- PREDICTION PAGE ---
if page == "Predict":
    st.header("Predict Tissue Type")
    st.write("Upload a histology image to classify it into one of 9 tissue types.")
    
    uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Your Image")
            st.image(image, caption="Uploaded Image", use_container_width=True)
        
        with col2:
            st.subheader("Prediction Result")
            if st.button("Classify Image", type="primary"):
                with st.spinner("Analyzing image..."):
                    try:
                        # Send to API
                        response = requests.post(
                            f"{API_URL}/predict", 
                            files={"file": (uploaded_file.name, uploaded_file.getvalue())}
                        )
                        if response.status_code == 200:
                            result = response.json()
                            st.success(f"**Predicted Class:** {result['label']}")
                            st.metric("Confidence", f"{result['confidence']:.1%}")
                            
                            # Show confidence bar
                            st.progress(result['confidence'])
                        else:
                            st.error(f"API Error: {response.status_code}")
                    except Exception as e:
                        st.error(f"Could not connect to API: {e}")
                        st.info("Make sure the API is running: `uvicorn src.api:app --port 8000`")

# --- VISUALIZATIONS PAGE ---
elif page == "Data Insights":
    st.header("Dataset Visualizations")
    st.write("Explore data insights from PathMNIST training set.")
    
    # Load visualizations from data/samples/ if they exist
    class_dist_path = Path("data/samples/class_distribution.png")
    sample_grid_path = Path("data/samples/sample_images_grid.png")
    cm_path = Path("data/samples/confusion_matrix.png")
    
    if class_dist_path.exists():
        st.subheader("Class Distribution")
        st.image(str(class_dist_path), use_container_width=True)
    else:
        st.info("Run the notebook to generate class distribution plot.")
    
    if sample_grid_path.exists():
        st.subheader("Sample Images per Class")
        st.image(str(sample_grid_path), use_container_width=True)
    else:
        st.info("Run the notebook to generate sample images grid.")
    
    if cm_path.exists():
        st.subheader("Confusion Matrix (Test Set)")
        st.image(str(cm_path), use_container_width=True)
    else:
        st.info("Run the notebook to generate confusion matrix.")

# --- PAGE 3: UPLOAD & RETRAIN ---
elif page == "Upload Data":
    st.header("Bulk Data Upload & Retraining")
    st.write("Upload multiple images to add to the training pool, then trigger retraining.")
    
    uploaded_files = st.file_uploader("Upload multiple images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if uploaded_files:
        st.write(f"Uploaded {len(uploaded_files)} files.")
        if st.button("Save Uploaded Files"):
            with st.spinner("Uploading files..."):
                files = [("files", (f.name, f.getvalue())) for f in uploaded_files]
                try:
                    response = requests.post(f"{API_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.success(response.json()["message"])
                    else:
                        st.error(f"Error: {response.status_code}")
                except Exception as e:
                    st.error(f"API connection error: {e}")
    
    st.markdown("---")
    st.subheader("Trigger Retraining")
    st.write("Click the button below to retrain the model with the current dataset (including uploaded files).")
    
    if st.button("Retrain Model"):
        with st.spinner("Retraining in progress... This may take a few minutes."):
            try:
                response = requests.post(f"{API_URL}/retrain")
                if response.status_code == 200:
                    st.success(response.json()["message"])
                    st.balloons()
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"API connection error: {e}")

# --- PAGE 4: MODEL INFO ---
elif page == "About":
    st.header("Model Information & Uptime")
    
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            st.success("API is running")
            uptime_placeholder = st.empty()
            uptime_placeholder.metric("Model Status", "Online", delta="Healthy")
        else:
            st.error("❌ API is not responding")
    except Exception as e:
        st.error(f"❌ API connection error: {e}")
    
    st.markdown("---")
    st.subheader("Model Details")
    st.write("""
    - **Dataset:** PathMNIST (9-class colorectal histology)
    - **Architecture:** MobileNetV2 (transfer learning)
    - **Input size:** 96x96 RGB
    - **Classes:** adipose, background, debris, lymphocytes, mucus, smooth muscle, normal colon mucosa, cancer-associated stroma, colorectal adenocarcinoma epithelium
    - **Metrics:** Accuracy, Precision, Recall, F1-score
    """)
    
    # Show model file size if exists
    model_path = Path("models/model.h5")
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        st.metric("Model File Size", f"{size_mb:.2f} MB")
